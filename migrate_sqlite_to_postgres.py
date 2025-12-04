"""
скрипт для миграции данных из sqlite в postgresql
использование: python migrate_sqlite_to_postgres.py
"""

import os
import sys
import django
import sqlite3
from pathlib import Path

# добавляем путь к проекту
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# настраиваем django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_project.settings')
django.setup()

from music.models import Album

def migrate_data():
    """перенос данных из sqlite в postgresql"""
    
    # путь к файлу sqlite
    sqlite_db = BASE_DIR / 'db.sqlite3'
    
    if not sqlite_db.exists():
        print("файл db.sqlite3 не найден!")
        return
    
    print("подключаемся к sqlite базе...")
    sqlite_conn = sqlite3.connect(sqlite_db)
    sqlite_conn.row_factory = sqlite3.Row
    cursor = sqlite_conn.cursor()
    
    # получаем все альбомы из sqlite
    cursor.execute("SELECT * FROM music_album")
    albums = cursor.fetchall()
    
    print(f"найдено {len(albums)} альбомов для переноса")
    
    # переносим каждый альбом
    for album_row in albums:
        # проверяем, нет ли уже такого альбома в postgresql
        exists = Album.objects.filter(
            title=album_row['title'],
            artist=album_row['artist'],
            year=album_row['year']
        ).exists()
        
        if not exists:
            # создаем новый альбом в postgresql
            Album.objects.create(
                title=album_row['title'],
                artist=album_row['artist'],
                year=album_row['year'],
                songs=album_row['songs'],
                created_at=album_row['created_at']
            )
            print(f"перенесен: {album_row['title']} - {album_row['artist']}")
        else:
            print(f"пропущен (уже есть): {album_row['title']}")
    
    sqlite_conn.close()
    print("миграция завершена!")

if __name__ == '__main__':
    migrate_data()