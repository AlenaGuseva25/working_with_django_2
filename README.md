# Django-project.

## Описание:

В рамках изучения курса DRF, на котором будете знакомиться с основными концепциями и инструментами Django REST framework (DRF) 
для разработки мощных и масштабируемых RESTful API. Целью является создание  платформы для онлайн-обучения, на которой
каждый желающий сможет размещать свои полезные материалы или курсы.

## Установка:

1. Клонируйте репозиторий:
```
git@github.com:AlenaGuseva25/working_with_django_2.git
```
2. Создайте файл .env в корне проекта на основе примера `.env.sample`

3. Запустите проект командой:
```
docker-compose up --build
```

4. После запуска выполните миграции:

```
docker-compose exec web python manage.py migrate
```
5. После запуска веб-приложение будет доступно по адресу: http://localhost:8000

## Проверка работоспособности сервисов

1. Django-приложение (web)
Откройте в браузере: http://localhost:8000/admin/

Войдите с данными суперпользователя

Убедитесь, что интерфейс администратора доступен

2. API endpoints
Получение списка курсов:
* Регистрация.(`users/register/`)
* Авторизация.(`users/token/`)
* Список курсов.(`courses/`)

3. Celery worker
Проверьте логи Celery на выполнение задач:
```
docker-compose logs -f celery
```

4. PostgreSQL (db)
Подключитесь к БД для проверки:

```
docker-compose exec db psql -U your_db_user -d your_db_name
```

5. Redis
Проверьте подключение:

```
docker-compose exec redis redis-cli ping
```

Должен вернуться PONG

## Дополнительные команды:

Для просмотра запущенных контейнеров:

`docker-compose ps`

Для просмотра логов всех контейнеров:

`docker-compose logs`

Для остановки сервисов и удаления контейнеров:

`docker-compose down`


## Документация
Доступна по адресу: `/docs/` и `/redoc/`