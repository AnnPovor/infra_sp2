### API для проекта YaMDB в рамках Яндекс.Практикум

Поддерживаемые методы запросов:

```
GET, POST, PUT, PATCH, DELETE
```
Формат выходных данных:

```
JSON
```


### Как запустить проект, используя Docker (база данных PostgreSQL)::

1. Клонировать репозиторий:

```
git clone git@github.com:AnnPovor/api_yamdb.git
```
2. В директории проекта создайте файл .env и пропишите переменные окружения, пример:

```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```

С помощью Dockerfile и docker-compose.yaml разверните проект:

```
docker-compose up --build
```

В новом окне терминала узнайте id контейнера infra и войдите в контейнер:

```
docker container ls
```

```
docker exec -it <CONTAINER_ID> bash
```
В контейнере выполните миграции, создайте суперпользователя и заполните базу начальными данными:

```
python manage.py migrate

python manage.py createsuperuser

python manage.py loaddata fixtures.json
```
Подробная документация по работе API:
```
По адресу http://127.0.0.1:8000/redoc/ доступна документация для API YaMDB
```