 ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=red)
 ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=red)

# Платформа для обмена вещами (бартерная система)

## Описание
Веб-приложение на Django для организации обмена вещами между пользователями.

## Установка
1. Клонировать репозиторий и перейти в папку:
```Python
git clone git@github.com:GagarinRu/BarterSystem.git
cd BarterSystem
```
2. Создать и активировать виртуальное окружение:

```Python
python -m venv venv
source venv/bin/activate
```
3. Установить зависимости:

```Python
pip install -r requirements.txt
```
4. Применить миграции:

```Python
python manage.py migrate
```
5. Создать суперпользователя:

```Python
python manage.py createsuperuser
```
6. Запустить сервер:

```Python
python manage.py runserver
```

## Дополнительная информация:

### Аутентификация
Пользователей можно создать черед админ панель суперпользователя.

### Использование API
API доступно по адресу http://localhost:8000/api/

### Эндпоинты:
1. Объявления

GET /api/ads/ - список объявлений

POST /api/ads/ - создать объявление

GET /api/ads/<id>/ - получить объявление

PATCH /api/ads/<id>/ - обновить объявление

DELETE /api/ads/<id>/ - деактивировать объявление

2. Предложения обмена

POST /api/proposals/ - создать предложение обмена

PATCH /api/proposals/<id>/ - обновить статус предложения

GET /api/my-proposals/ - получить предложения текущего пользователя


### Документация API
Доступна по адресам:

Swagger UI: http://localhost:8000/swagger/

ReDoc: http://localhost:8000/redoc/

## Тестирование
Запустить тесты:

```Python
python manage.py test
```

### Автор
Evgeny Kudryashov: https://github.com/GagarinRu