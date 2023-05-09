# Django сервис друзей
Доступные возможности:
- Регистрация пользователей
- Получение/поиск пользователей
- Отправление/принятие/отклонение заявок в друзья
- Получение списка заявок, статуса дружбы с пользователем
- Удаление пользователя из друзей

API схема доступна [здесь](./api-schema.yaml)

# Установка и запуск
Убедитесь, что у вас установлен [Docker](https://www.docker.com/). Склонируйте
данный репозиторий:
```shell
git clone https://github.com/arsuhinars/django-friends
```

Создайте `.env` файл в директории репозитория. Пример содержимого указан ниже.
```text
BACKEND_PORT = 8000
BACKEND_SECRET_KEY = super_secret_key

DB_NAME = django_friends
DB_USERNAME = user
DB_PASSWORD = qwerty12
```

Введите следующую команду для запуска сервиса:
```shell
docker compose up -d
```

Для остановки сервиса выполните следующую команду:
```shell
docker compose down
```

# Пример работы с сервисом
> TODO
