# API для Yatube
Описание

## Стек технологий
Python 3.7.10, Django 3, 2, 3, Django REST Framework, SQLite3, Simple JWT.

## Инструкция по развёртыванию
Создайте виртуальное окружение:
```bash
python -m venv venv
```
Активируйте его:
```bash
source venv/Scripts/activate
```
Установите зависимости:
```bash
pip install -r requirements.txt
```
Сделайте миграции:
```bash
python manage.py migrate
```
Создайте супер пользователя:
```bash
python manage.py createsuperuser
```
И запускайте сервер:
```bash
python manage.py runserver
```

## Примеры
Примеры

## Документация
Чтобы открыть документацию, запустите сервер и перейдите по ссылке:
```http://127.0.0.1:8000/redoc/```
