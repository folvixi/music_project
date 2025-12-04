
from django.contrib import admin
from django.urls import path
from music import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_album, name='add_album'),
    path('upload/', views.upload_json, name='upload_json'),
    path('albums/', views.show_albums, name='show_albums'),
    path('search/', views.search_albums, name='search_albums'),  # ajax поиск
    path('edit/<int:album_id>/', views.edit_album, name='edit_album'),  # редактирование
    path('delete/<int:album_id>/', views.delete_album, name='delete_album'),  # удаление
]