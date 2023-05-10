# Django сервис друзей
Доступные возможности:
- Регистрация пользователей
- Получение/поиск пользователей
- Отправление/принятие/отклонение заявок в друзья
- Получение списка заявок, статуса дружбы с пользователем
- Удаление пользователя из друзей

API схема доступна [здесь](./api-schema.yaml)

## Установка и запуск
Убедитесь, что у вас установлен [Docker](https://www.docker.com/). Склонируйте
данный репозиторий:
```shell
git clone https://github.com/arsuhinars/django-friends
```

Создайте `.env` файл в директории репозитория. Пример содержимого файла указан ниже.
```text
BACKEND_PORT = 8000
BACKEND_SECRET_KEY = super_secret_key

SUPERUSER_NAME = admin
SUPERUSER_PASSWORD = 12345678

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

## Unit тестирование
Для запуска автоматического тестирования выполните следующую команду:
```shell
docker compose -f docker-compose.yaml -f docker-compose.test.yaml up backend
```

Для остановки сервиса выполните следующую команду:
```shell
docker compose down
```

## Пример работы с сервисом
Для ручного тестирования работы сервиса воспользуемся утилитой curl. Можно
также протестировать через Swagger Editor или Postman.

Ниже указаны примеры работы с некоторыми из API методов.

### Регистрация пользователя
```shell
curl -X 'POST' \
    http://localhost:8000/registration \
    -H 'Content-Type: application/json' \
    -d '{"name": "Ivan","password": "qwerty12"}'
```

Ответ сервера:
```json
{
  "id": 2,
  "name": "Ivan"
}
```

### Поиск пользователей
```shell
curl http://localhost:8000/users/search?name=va
```

Ответ сервера:
```json
[
  {
    "id": 2,
    "name": "Ivan"
  }
]
```

### Приглашение в друзья
```shell
curl -X 'POST' http://localhost:8000/friend/3/invite -u 'Ivan:qwerty12'
```

### Принятие заявки
```shell
curl -X 'POST' http://localhost:8000/friend/2/accept -u 'Petr:12345678'
```

### Получение списка друзей
```shell
curl http://localhost:8000/friends -u 'Ivan:qwerty12'
```

Ответ сервера:
```json
[
  {
    "id": 3,
    "name": "Petr"
  }
]
```
