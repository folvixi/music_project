
from django.db import models

# таблица в базе  sqlite
class Album(models.Model):
    title = models.CharField(max_length=200)  # название альбома
    artist = models.CharField(max_length=200)  # исполнитель
    year = models.IntegerField()  # год выпуска
    songs = models.IntegerField()  # количество песен
    # автоматически добавляет дату создания записи
    created_at = models.DateTimeField(auto_now_add=True)
    
    # метод для отображения в админке
    def __str__(self):
        return f"{self.title} - {self.artist}"
    
    # проверка на дубликат по названию и исполнителю
    def is_duplicate(self):
        return Album.objects.filter(title=self.title, artist=self.artist, year=self.year).exists()