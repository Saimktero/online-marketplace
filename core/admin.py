from django.contrib import admin
from django.core.cache import cache
from .models import Category, Product, Order


# Оптимизированный класс для Order (убираем дубликаты SQL)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'created_at')  # Показываем ключевые поля
    list_select_related = ('user',)  # Убираем дублирующиеся запросы к auth_user
    list_per_page = 50  # Ограничиваем количество записей на странице (уменьшает нагрузку)

    def get_queryset(self, request):
        print('\n get_queryset() вызван в admin.py!')  # Проверяем, вызывается ли этот метод

        cache_key = 'admin_orders_queryset'
        queryset = cache.get(cache_key)

        if queryset is None:
            queryset = super().get_queryset(request).select_related('user')
            cache.set(cache_key, queryset, 60 * 15)

        return queryset


# Регистрация Order с оптимизацией
admin.site.register(Order, OrderAdmin)

# Регистрация категорий
admin.site.register(Category)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category")
    list_filter = ("category",)
    search_fields = ("name",)
