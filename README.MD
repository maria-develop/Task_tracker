# Task tracker (Трекер задач)
Проект представляет собой веб-приложение для управления задачами. 
Оно позволяет менеджерам создавать задачи, назначать их сотрудникам, 
отслеживать статус выполнения и управлять активными задачами.

http://127.0.0.1:8000/tasks/ - список главных задач

http://127.0.0.1:8000/tasks/t/ - список задач

http://127.0.0.1:8000/tasks/t/important/ - задачи, которые не взяты в работу, но от которых зависят другие задачи, 
взятые в работу. Реализует поиск по сотрудникам, которые могут взять такие задачи.

http://127.0.0.1:8000/tasks/emp/busy_tasks/ - список сотрудников и их задачи, отсортированный по количеству активных задач.

## Основные функции
1. Создание, редактирование и удаление задач.
2. Назначение задач сотрудникам.
3. Отслеживание статуса выполнения задач.
4. Авторизация и аутентификация пользователей (менеджеров и сотрудников).
5. REST API для интеграции с другими системами.

## Технологии
Backend: Django, Django REST Framework (DRF)
База данных: PostgreSQL
Контейнеризация: Docker
Аутентификация: JWT
Документация API: Swagger/Redoc
Тестирование: Django Test Framework

## Установка и настройка
1. Клонирование репозитория
git clone https://github.com/maria-develop/Task_tracker
cd task_tracker
2. Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Для Linux/MacOS
venv\Scripts\activate     # Для Windows
3. Установка зависимостей
pip install -r requirements.txt
4. Настройка базы данных
Убедитесь, что у вас установлен PostgreSQL.

Создайте базу данных и пользователя:
CREATE DATABASE task_tracker;
CREATE USER task_tracker_user WITH PASSWORD 'ваш_пароль';
GRANT ALL PRIVILEGES ON DATABASE task_tracker TO task_tracker_user;
Настройте подключение к базе данных в .env в соответствии с .venv.

5. Применение миграций
python manage.py migrate
6. Создание суперпользователя
python manage.py csu

## Использование API
Документация API

http://127.0.0.1:8000/swagger/

http://127.0.0.1:8000/redoc/


## Для запуска тестов используйте команду:

python manage.py test

Чтобы проверить покрытие кода тестами, установите coverage:
pip install coverage

Запустите тесты с измерением покрытия:
coverage run --source='.' manage.py test

Просмотрите отчет о покрытии:
coverage report

## Линтеры и форматирование
Flake8 (проверка стиля кода)
flake8 .

## Развертывание

Соберите Docker-образ:
docker-compose build

Запустите контейнеры:
docker-compose up

Примените миграции внутри контейнера:
docker-compose exec web python manage.py migrate
