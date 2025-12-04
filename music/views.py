
import os
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Album  # импортируем нашу модель

# главная страница
def home(request):
    return render(request, 'home.html')

# добавление альбома с выбором сохранения
@csrf_exempt
def add_album(request):
    error = ""
    success = ""
    
    if request.method == 'POST':
        # получаем данные из формы
        title = request.POST.get('title', '').strip()
        artist = request.POST.get('artist', '').strip()
        year = request.POST.get('year', '').strip()
        songs = request.POST.get('songs', '').strip()
        save_to = request.POST.get('save_to', 'json')  # 'json' или 'db'
        
        # проверяем что все заполнено
        if not all([title, artist, year, songs]):
            error = "все поля должны быть заполнены"
        else:
            try:
                year = int(year)
                songs = int(songs)
                
                # проверки
                if year < 1900 or year > 2025:
                    error = "год должен быть между 1900 и 2025"
                elif songs <= 0:
                    error = "количество песен должно быть больше 0"
                    
            except:
                error = "проверьте правильность введенных чисел"
        
        # если нет ошибок - сохраняем
        if not error:
            if save_to == 'json':
                # сохраняем в json файл
                os.makedirs(settings.JSON_DIR, exist_ok=True)
                
                album_data = {
                    'title': title,
                    'artist': artist,
                    'year': year,
                    'songs': songs
                }
                
                # безопасное имя файла
                filename = f"{artist}_{title}.json".replace(' ', '_')
                filepath = os.path.join(settings.JSON_DIR, filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(album_data, f, ensure_ascii=False, indent=2)
                
                success = "альбом сохранен в json файл!"
                
            else:  # save_to == 'db'
                # сохраняем в базу данных sqlite
                # проверяем нет ли такого альбома уже
                exists = Album.objects.filter(
                    title=title, 
                    artist=artist, 
                    year=year
                ).exists()
                
                if exists:
                    error = "такой альбом уже есть в базе данных!"
                else:
                    # создаем новую запись в sqlite базе
                    album = Album(
                        title=title,
                        artist=artist,
                        year=year,
                        songs=songs
                    )
                    album.save()
                    success = "альбом сохранен в базу данных!"
    
    return render(request, 'add_album.html', {
        'error': error,
        'success': success
    })

# загрузка json файла
@csrf_exempt
def upload_json(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        
        if file.name.endswith('.json'):
            try:
                content = file.read().decode('utf-8')
                data = json.loads(content)
                
                # проверяем поля
                required = ['title', 'artist', 'year', 'songs']
                if all(field in data for field in required):
                    os.makedirs(settings.JSON_DIR, exist_ok=True)
                    filename = file.name
                    filepath = os.path.join(settings.JSON_DIR, filename)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    
                    return render(request, 'upload_json.html', {
                        'success': 'файл загружен!'
                    })
                else:
                    return render(request, 'upload_json.html', {
                        'error': 'не все нужные поля в файле'
                    })
            except:
                return render(request, 'upload_json.html', {
                    'error': 'ошибка чтения файла'
                })
        else:
            return render(request, 'upload_json.html', {
                'error': 'только json файлы'
            })
    
    return render(request, 'upload_json.html')

# показ всех альбомов с выбором источника
def show_albums(request):
    source = request.GET.get('source', 'db')  # 'db' или 'json'
    
    if source == 'json':
        # читаем из json файлов
        albums = []
        if os.path.exists(settings.JSON_DIR):
            for filename in os.listdir(settings.JSON_DIR):
                if filename.endswith('.json'):
                    filepath = os.path.join(settings.JSON_DIR, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            album_data = json.load(f)
                            albums.append(album_data)
                    except:
                        pass
    else:  # source == 'db'
        # читаем из базы данных sqlite
        # sqlite база находится в файле db.sqlite3 в корне проекта
        albums = Album.objects.all()
    
    return render(request, 'show_albums.html', {
        'albums': albums,
        'source': source
    })

# ajax поиск по базе данных
def search_albums(request):
    query = request.GET.get('q', '')
    
    if query:
        # ищем по названию или исполнителю в sqlite базе
        results = Album.objects.filter(
            title__icontains=query
        ) | Album.objects.filter(
            artist__icontains=query
        )
    else:
        results = Album.objects.all()
    
    # преобразуем в json
    data = []
    for album in results:
        data.append({
            'id': album.id,
            'title': album.title,
            'artist': album.artist,
            'year': album.year,
            'songs': album.songs
        })
    
    return JsonResponse({'albums': data})

# редактирование альбома
@csrf_exempt
def edit_album(request, album_id):
    # получаем альбом из базы данных по id
    album = get_object_or_404(Album, id=album_id)
    
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        artist = request.POST.get('artist', '').strip()
        year = request.POST.get('year', '').strip()
        songs = request.POST.get('songs', '').strip()
        
        if all([title, artist, year, songs]):
            try:
                album.title = title
                album.artist = artist
                album.year = int(year)
                album.songs = int(songs)
                album.save()
                return redirect('show_albums')
            except:
                pass
    
    return render(request, 'edit_album.html', {'album': album})

# удаление альбома
@csrf_exempt
def delete_album(request, album_id):
    # получаем альбом из базы данных по id
    album = get_object_or_404(Album, id=album_id)
    
    if request.method == 'POST':
        album.delete()
        return redirect('show_albums')
    
    return render(request, 'delete_album.html', {'album': album})