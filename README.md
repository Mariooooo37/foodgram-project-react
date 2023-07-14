# Дипломный проект - Foodgram


Foodgram - продуктовый помошник. В нём пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.




## **Стэк технологий**

Django==3.2.3

djangorestframework==3.12.4

djoser==2.2.0

psycopg2-binary==2.9.3

Pillow==9.5.0

Веб-сервер: nginx (контейнер nginx)

Frontend фреймворк: React (контейнер frontend)

Backend фреймворк: Django (контейнер backend)

API фреймворк: Django REST (контейнер backend)

База данных: PostgreSQL (контейнер db)

## Локальный запуск проекта

Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone https://github.com/Mariooooo37/foodgram-project-react
```

В терминале из папки infra выполнить команду:

```
docker compose up
```

После последовательно в терминале выполнить команды для миграций и сбора статики:

```
sudo docker compose -f docker-compose.yml exec backend python manage.py migrate

sudo docker compose -f docker-compose.yml exec backend python manage.py collectstatic
```
Для загрузки ингредиентов в базу данных выполните команду:

```
sudo docker compose -f docker-compose.yml exec backend python manage.py load_ingredients
```
## .env

В корне проекта создайте файл .env и пропишите в него свои данные.

Пример:

```
POSTGRES_USER=user
POSTGRES_PASSWORD=pass
POSTGRES_DB=db
DB_HOST=db
DB_PORT=5432
DEBUG=True
SECRET_KEY = 'secret-key'
ALLOWED_HOSTS = '000.000.00.000, localhost'
GATEWAY_PORT=8000
```

## Автор
Иванов Роман - студент Яндекс Практикума по курсу Python-разработчик.
