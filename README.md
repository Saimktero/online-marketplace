## 🚀 Запуск проекта
1. Клонировать репозиторий
2. Создать виртуальное окружение
3. Установить зависимости
4. Настроить .env
5. Запустить миграции
6. Запустить сервер
7. Запустить Celery


## 📚 Маршруты проекта

| Маршрут                         | Метод | Описание                                            |
|----------------------------------|--------|-----------------------------------------------------|
| `/api/categories/`              | GET    | Список категорий                                    |
| `/api/categories/`              | POST   | Создание категории (только админ)                   |
| `/api/categories/<id>/`         | GET    | Детали категории                                    |
| `/api/categories/<id>/`         | PUT    | Обновление категории (только админ)                 |
| `/api/categories/<id>/`         | DELETE | Удаление категории (только админ)                   |
| `/api/products/`                | GET    | Список товаров                                      |
| `/api/products/`                | POST   | Создание товара (только админ)                      |
| `/api/products/<id>/`           | GET    | Детали товара                                       |
| `/api/products/<id>/`           | PUT    | Обновление товара (только админ)                    |
| `/api/products/<id>/`           | DELETE | Удаление товара (только админ)                      |
| `/api/orders/`                  | GET    | Список заказов (только авторизованный пользователь) |
| `/api/orders/`                  | POST   | Создание заказа                                     |
| `/api/orders/<id>/`             | GET    | Детали заказа                                       |
| `/api/orders/<id>/`             | PUT    | Обновление заказа                                   |
| `/api/orders/<id>/`             | DELETE | Удаление заказа                                     |
| `/api/users/register/`          | POST   | Регистрация пользователя                            |
| `/api/users/login/`             | POST   | Авторизация пользователя                            |
| `/api/users/token/`             | POST   | JWT логин (получение access и refresh токенов)      |
| `/api/users/token/refresh/`     | POST   | Обновление access токена                            |
| `/api/users/`                   | GET    | Список пользователей (только админ)               |
| `/admin/`                       | GET    | Django админка                                      |
| `/`                             | GET    | Главная страница (React frontend)                   |
| `/products`                     | GET    | Каталог товаров на фронте                           |
| `/cart`                         | GET    | Корзина пользователя                                |
| `/my-orders`                    | GET    | Список заказов на фронте                            |
| `/login`                        | GET    | Страница входа                                      |
| `/api/trigger-migrate/`         | GET    | ❗ Временная миграция (закомментировано)             |
| `/api/create-superuser/`        | GET    | ❗ Временное создание админа (закомментировано)      |


## О проекте
REST API для интернет‑магазина: категории, товары, заказы, пользователи, JWT‑авторизация, email‑уведомления через Celery.

## 🛠️ Технологии
- Python 3.x
- Django
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- JWT
- Railway

## Архитектура проекта
online-marketplace/
├─ .venv/                      # локальное виртуальное окружение (не коммитим)
├─ config/                     # проектный модуль Django: настройки, точки входа, Celery
│  ├─ __init__.py              # инициализация пакета (подключение celery app)
│  ├─ asgi.py                  # ASGI-старт (для uvicorn/daphne)
│  ├─ celery.py                # конфигурация Celery (broker, app, autodiscover_tasks)
│  ├─ settings.py              # основные настройки Django/DRF/CORS/DB/EMAIL и т.д.
│  ├─ urls.py                  # корневые URL проекта (подключение core.urls, admin и т.п.)
│  └─ wsgi.py                  # WSGI-старт (gunicorn/uwsgi)
│
├─ core/                       # основное приложение (доменная логика)
│  ├─ migrations/              # миграции БД, генерятся Django
│  ├─ tests/                   # автотесты API/моделей/permission-ов
│  ├─ admin.py                 # регистрация моделей в Django Admin
│  ├─ apps.py                  # конфигурация приложения
│  ├─ filters.py               # фильтрация/поиск (django-filters) для вьюх/qs
│  ├─ models.py                # модели: Category, Product, Order, и т.д.
│  ├─ permissions.py           # кастомные DRF permissions (IsOwnerOrAdmin и пр.)
│  ├─ serializers.py           # DRF-сериализаторы для входа/выхода данных
│  ├─ tasks.py                 # Celery-задачи (e-mail после заказа и т.п.)
│  ├─ urls.py                  # роутинг приложения (подключается в config.urls)
│  └─ views.py                 # DRF-вьюхи/GenericViewSet/APIView
│
├─ scripts/                    # служебные скрипты
│  └─ migrate.sh               # утилита для миграций/сборки (используется на деплое)
│
├─ staticfiles/                # собранная статика (collectstatic) — в репо лучше не хранить
│
├─ .env                        # локальные переменные окружения (не коммитить)
├─ .gitignore                  # исключения Git (venv, .env, staticfiles/build и пр.)
├─ db.sqlite3                  # локальная БД (на проде — PostgreSQL)
├─ Draft                       # черновик
├─ dump.rdb                    # дамп Redis (локальный артефакт — в Git не нужен)
├─ journal.md                  # Dev Journal (краткие дневные записи)
├─ manage.py                   # CLI-утилита Django (миграции, runserver и т.д.)
├─ railway.json                # конфиг Railway (build/run hooks, collectstatic и пр.)
├─ README.md                   # описание бэкенда
└─ requirements.txt            # зависимости Python


Краткие роли ключевых узлов:
config — «скелет» проекта: все точки входа, настройки, подключение Celery.
core — бизнес‑логика: модели, API, сериализация, права, фоновые задачи.
scripts — всё, что помогает автоматизировать рутина (миграции, сборка).
railway.json — как Railway билдит/запускает сервис.
requirements.txt — замораживает версии пакетов для воспроизводимости.
journal.md — быстрый вход в контекст (то, что мы ведём).
.env — чувствительные переменные (в Git не попадают).
staticfiles / db.sqlite3 / dump.rdb — локальные артефакты (в продакшне не нужны; стоит исключить из Git).