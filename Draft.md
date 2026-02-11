from django.contrib.auth.models import User
user = User.objects.create_user(username="testuser2", password="password123")


order = Order.objects.create(user=user)
order.product.add(product1, product2)


from core.tasks import add
result = add.delay(5, 10)
print(result.get(timeout=5))



from django.core.mail import send_mail
send_mail(
    "Тестовое письмо",
    "Привет! Это тестовое письмо из Django.",
    "priluckijkirill30@gmail.com",
    ["priluckijkirill30@gmail.com"],
    fail_silently=False,
)


# Отправка уведомления при заказе на email
from core.models import Order, User
from core.tasks import send_order_confirmation_email
# Создаём заказ вручную
user = User.objects.first()  # Берём первого пользователя
order = Order.objects.create(user=user)
# Запускаем задачу вручную
send_order_confirmation_email.delay(user.email)


# Проверка почты пользователя
from django.contrib.auth.models import User
user = User.objects.get(id=3)  # Подставь нужный ID
print(f"Email из базы: '{user.email}'")


#Рабочая среда WSL
sudo service redis-server start
redis-cli ping
cd /mnt/c/PycharmProjects/online-marketplace-backend
source ~/venv/bin/activate


print("🔍 API ответ:", response.data)  # Логируем ответ API
print("🔍 Количество категорий в ответе:", len(response.data))


Frontend
import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;



'rest_framework.pagination.PageNumberPagination', 'PAGE_SIZE': 10,
                  'DEFAULT_FILTER_BACKENDS': [
                      'django_filters.rest_framework.DjangoFilterBackend',
                      'rest_framework.filters.SearchFilter',
                  ],
                  'DEFAULT_AUTHENTICATION_CLASSES': [
                      'rest_framework_simplejwt.authentication.JWTAuthentication',
                  ],
                  'DEFAULT_PERMISSION_CLASSES': [
                      'rest_framework.permissions.IsAuthenticated'
                  ],

                  }