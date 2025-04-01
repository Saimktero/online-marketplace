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