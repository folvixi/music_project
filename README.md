## Музыкальные альбомы - Django приложение
## Простое веб-приложение для управления информацией о музыкальных альбомах с поддержкой сохранения данных в JSON файлы и PostgreSQL базу данных.

# Функциональность
Добавление информации об альбомах через веб-форму

Выбор сохранения: в JSON файл или PostgreSQL базу данных

Проверка на дубликаты при сохранении в БД

Загрузка JSON файлов с информацией об альбомах

Просмотр альбомов из обоих источников (JSON файлы и БД)

AJAX-поиск по базе данных

Редактирование и удаление записей из БД

Интерфейс на Bootstrap 5

Docker контейнеризация

## Быстрый старт
# Предварительные требования:
Установите Docker Desktop для Windows: https://www.docker.com/products/docker-desktop/

## Запуск приложения:
# Клонируйте репозиторий:
git clone https://github.com/folvixi/music_project
cd music-project

# Соберите и запустите контейнеры:
docker-compose up --build

# Откройте в браузере:
http://localhost:8000

## Структура проекта

music-project/
──docker-compose.yml      # конфигурация Docker
── Dockerfile              # образ Django приложения
── .dockerignore          # игнорируемые файлы
── .env.example           # пример переменных окружения
── requirements.txt       # зависимости Python
── db.sqlite3            # старая база данных SQLite
── json_files/           # папка с JSON файлами
── static/              # статические файлы (CSS)
── migrate_sqlite_to_postgres.py  # скрипт миграции
── music/               # Django приложение
── music_project/       # настройки проекта
── README.md           # эта документация

## Работа с Docker
# Основные команды:
docker-compose up - Запуск приложения
docker-compose up -d - Запуск в фоновом режиме
docker-compose down - Остановка приложения
docker-compose down -v - Остановка с удалением данных БД
docker-compose logs - Просмотр логов
docker-compose logs -f - Просмотр логов в реальном времени
docker-compose exec web python manage.py migrate - Выполнение миграций
docker-compose exec web python manage.py createsuperuser - Создание суперпользователя

# Компоненты Docker:
web - Django приложение на порту 8000

db - PostgreSQL база данных на порту 5432

# Миграция данных из SQLite в PostgreSQL
Если у вас есть данные в старой SQLite базе (db.sqlite3):

Поместите файл db.sqlite3 в корень проекта

Выполните миграцию: docker-compose exec web python migrate_sqlite_to_postgres.py

Проверьте перенос данных: docker-compose exec db psql -U musicuser -d musicdb -c "SELECT COUNT(*) FROM music_album;"

# Работа с базой данных
PostgreSQL (новая база):
# Данные для подключения:

Хост: db (внутри Docker) или localhost (снаружи)

Порт: 5432

База данных: musicdb

Пользователь: musicuser

Пароль: musicpassword

## Просмотр базы данных:
# Через командную строку
docker-compose exec db psql -U musicuser -d musicdb - Подключиться к PostgreSQL
Команды в PostgreSQL:
\dt - показать все таблицы
SELECT * FROM music_album; - показать все альбомы
\q - выйти


## Веб-интерфейс
# Основные страницы:
Главная (/) - описание приложения

Добавить альбом (/add/) - форма для добавления новых альбомов

Выбор сохранения: JSON файл или PostgreSQL

Проверка на дубликаты при сохранении в БД

Валидация данных (год 1900-2025, песни > 0)

Загрузить JSON (/upload/) - загрузка файлов с данными

Все альбомы (/albums/) - просмотр альбомов

Переключение между JSON файлами и БД

AJAX-поиск по БД

Редактирование и удаление (только для БД)

Просмотр данных (/data/) - статистика и экспорт данных

## Функции:
Поиск в реальном времени по названию и исполнителю

Редактирование существующих записей

Удаление записей с подтверждением

Экспорт данных в JSON, CSV форматы

## Разработка
# Переменные окружения:
Создайте файл .env на основе .env.example:


SECRET_KEY=ваш-секретный-ключ
DEBUG=True
DATABASE_URL=postgresql://musicuser:musicpassword@db:5432/musicdb
JSON_DIR=/app/json_files
Установка зависимостей:
docker-compose exec web pip install -r requirements.txt - Внутри контейнера
pip install -r requirements.txt - Или локально

## Миграции базы данных:
docker-compose exec web python manage.py makemigrations - Создать миграции
docker-compose exec web python manage.py migrate - Применить миграции

## Технические детали
# Технологии:
Backend: Django 5.2, Python 3.10

База данных: PostgreSQL 15

Frontend: HTML, CSS, JavaScript, Bootstrap 5, jQuery

Контейнеризация: Docker, Docker Compose



## Устранение неполадок
Проблема: "PostgreSQL 14 or later is required"
Решение: Используется PostgreSQL 15 в docker-compose.yml

Проблема: "Файл db.sqlite3 не найден"
Решение: Скопируйте файл в контейнер: docker cp db.sqlite3 music_web:/app/db.sqlite3

Проблема: "Не удается подключиться к базе данных"
Решение: Убедитесь, что контейнер с БД запущен: docker-compose ps (должны быть запущены music_db и music_web)

Проблема: Статические файлы не загружаются
Решение: Пересоберите контейнеры: docker-compose down и docker-compose up --build

