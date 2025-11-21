# music/views.py
import os
import json
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# Главная страница
def home(request):
    return render(request, 'home.html')

# Добавление альбома - ОТКЛЮЧАЕМ CSRF
@csrf_exempt
def add_album(request):
    error = ""
    
    if request.method == 'POST':
        # Получаем данные из формы
        title = request.POST.get('title', '').strip()
        artist = request.POST.get('artist', '').strip()
        year = request.POST.get('year', '').strip()
        songs = request.POST.get('songs', '').strip()
        
        # Проверяем что все заполнено
        if not title or not artist or not year or not songs:
            error = "Все поля должны быть заполнены"
        else:
            # Проверяем что год и песни - числа
            try:
                year = int(year)
                songs = int(songs)
            except:
                error = "Год и количество песен должны быть числами"
            
            # Проверяем год
            if not error and (year < 1900 or year > 2025):
                error = "Год должен быть между 1900 и 2025"
            
            # Проверяем песни
            if not error and songs <= 0:
                error = "Количество песен должно быть больше 0"
            
            # Если нет ошибок - сохраняем
            if not error:
                # Создаем папку для JSON если нет
                os.makedirs(settings.JSON_DIR, exist_ok=True)
                
                # Данные альбома
                album_data = {
                    'title': title,
                    'artist': artist,
                    'year': year,
                    'songs': songs
                }
                
                # Создаем имя файла
                filename = f"{artist}_{title}.json".replace(' ', '_')
                filepath = os.path.join(settings.JSON_DIR, filename)
                
                # Сохраняем в JSON
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(album_data, f, ensure_ascii=False, indent=2)
                
                # Показываем успех
                return render(request, 'add_album.html', {
                    'success': 'Альбом успешно сохранен!'
                })
    
    return render(request, 'add_album.html', {'error': error})

# Загрузка JSON файла - ОТКЛЮЧАЕМ CSRF
@csrf_exempt
def upload_json(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        
        # Проверяем что это JSON
        if file.name.endswith('.json'):
            try:
                # Читаем файл
                content = file.read().decode('utf-8')
                data = json.loads(content)
                
                # Проверяем поля
                if 'title' in data and 'artist' in data and 'year' in data and 'songs' in data:
                    # Создаем папку если нет
                    os.makedirs(settings.JSON_DIR, exist_ok=True)
                    
                    # Сохраняем файл
                    filename = file.name
                    filepath = os.path.join(settings.JSON_DIR, filename)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    
                    return render(request, 'upload_json.html', {
                        'success': 'Файл успешно загружен!'
                    })
                else:
                    return render(request, 'upload_json.html', {
                        'error': 'В файле не все нужные поля'
                    })
                    
            except:
                return render(request, 'upload_json.html', {
                    'error': 'Ошибка чтения файла'
                })
        else:
            return render(request, 'upload_json.html', {
                'error': 'Файл должен быть JSON'
            })
    
    return render(request, 'upload_json.html')

# Показ всех альбомов
def show_albums(request):
    # Папка с JSON файлами
    json_dir = settings.JSON_DIR
    
    # Если папки нет или она пустая
    if not os.path.exists(json_dir) or not os.listdir(json_dir):
        return render(request, 'show_albums.html', {
            'message': 'Нет сохраненных альбомов'
        })
    
    # Читаем все JSON файлы
    albums = []
    for filename in os.listdir(json_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(json_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    album_data = json.load(f)
                    albums.append(album_data)
            except:
                pass  # Если файл битый - пропускаем
    
    return render(request, 'show_albums.html', {
        'albums': albums
    })