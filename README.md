# yamdb_final

![example workflow](https://github.com/grigoryAkao/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

api_yamdb - это Application Programming Interface для социальной сети Yamdb_v1. Предусмотрена обработка как GET-запросов так и POST, PUT, PATCH запросов. В проекте используется Python версии 3.7

# Используемые технологии 
```
Python 3.X
Django 2.2.19
Docker 20.10.17
```


# Шаблон наполнения env-файла

```
SECRET_KEY = 'p&l%385148kslhtyn^##a1)ilz@4zqj=rq&agdol^##zgl9(vs'
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

# Клонирование репозитория

```
git clone git@github.com:grigoryAkao/yamdb_final.git
```

# Описание команд для запуска приложения в контейнерах

```
cd infra/
docker compose up -d

docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py collectstatic --no-input
```

# Описание команды для заполнения базы данными и создания дампа базы данных.

```
docker compose exec web python manage.py dbfile
docker compose exec web python manage.py dumpdata > dumpPostrgeSQL.json 
```

# Останавливаем контейнеры:

```
docker compose down -v 
```

# В проекте доступны следующие ресурсы:

```
auth - аутентификация;
users - пользователи;
titles - произведения, к которым пишут отзывы;
categories - категории (типы) произведений;
genres - жанры произведений;
reviews - отзывы на произведения;
comments - комментарии к отзывам.
```

# Документация по работе сервиса

```
/redoc/
```

# Пример POST-запроса на /api/v1/auth/signup/:

```
{
    "email": "string",
    "username": "string"
}
```

# Получение JWT-токена:
## пример POST-запроса на /api/v1/auth/token/:

```
{
    "username": "string",
    "confirmation_code": "string"
}
```

## пример ответа:

```
{
    "token": "string"
}
```

# Получение списка всех произведений (при указании номер страницы в параметре page выдача работает с пагинацией):
## GET-запрос на /api/v1/titles/:
## пример ответа:

```
    [
        {
            "count": 0,
            "next": "string",
            "previous": "string",
            "results": [
            {
                "id": 0,
                "name": "string",
                "year": 0,
                "rating": 0,
                "description": "string",
                "genre": [
                {
                    "name": "string",
                    "slug": "string"
                }
                ],
                "category": {
                "name": "string",
                "slug": "string"
                }
            }
            ]
        }
    ]
```

# Лицензия

MIT

# Автор

Grigory
[![N|Solid](https://img.icons8.com/color/48/000000/telegram-app--v1.png)](https://t.me/grigoryAkao)