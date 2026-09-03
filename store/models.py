from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True)
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    
    # Нові поля для Новинок та відображення
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Стара ціна")
    discount = models.IntegerField(default=0, verbose_name="Знижка %")
    is_new = models.BooleanField(default=False, verbose_name="Новинка")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0, verbose_name="Рейтинг")
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="Зображення")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"
        ordering = ['-created_at']

class TimeMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    class Meta:
        abstract = True    

class Order(TimeMixin):
    product_id = models.IntegerField(verbose_name="ID товару")
    product_name = models.CharField(max_length=200, verbose_name="Назва товару")
    quantity = models.PositiveIntegerField(verbose_name="Кількість")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Загальна сума")
    customer_name = models.CharField(max_length=100, verbose_name="Ім'я клієнта")
    phone = models.CharField(max_length=20, verbose_name="Телефон")

    def __str__(self):
        return f"Замовлення #{self.id} - {self.customer_name}"

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(check=models.Q(quantity__gt=0), name='order_quantity_positive'),
            models.CheckConstraint(check=models.Q(total_price__gte=0), name='order_total_price_non_negative'),
        ]

