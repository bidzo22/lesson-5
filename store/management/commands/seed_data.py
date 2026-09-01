from django.core.management.base import BaseCommand
from store.models import Category, Product, Order


class Command(BaseCommand):
    help = "Заповнює базу даних тестовими даними"

    def handle(self, *args, **kwargs):
        # Видаляємо старі дані
        Product.objects.all().delete()
        Category.objects.all().delete()
        Order.objects.all().delete()

        # Створюємо категорії
        electronics = Category.objects.create(name="Електроніка", slug="electronics")
        clothing = Category.objects.create(name="Одяг", slug="clothing")
        books = Category.objects.create(name="Книги", slug="books")

        # Створюємо товари з новими полями
        products = [
            Product(
                category=electronics,
                name="Ноутбук Lenovo",
                description="Потужний ноутбук для роботи і навчання",
                price=32000,
                old_price=35000,
                discount=8,
                stock=5,
                is_available=True,
                is_new=True,
                rating=4.5,
                slug="noutbuk-lenovo"
            ),
            Product(
                category=electronics,
                name="Смартфон Samsung",
                description="Флагманський смартфон з чудовою камерою",
                price=18000,
                old_price=20000,
                discount=10,
                stock=0,
                is_available=False,
                is_new=False,
                rating=4.8,
                slug="smartfon-samsung"
            ),
            Product(
                category=electronics,
                name="Навушники Sony",
                description="Бездротові навушники з шумозаглушенням",
                price=4500,
                old_price=None,
                discount=0,
                stock=12,
                is_available=True,
                is_new=True,
                rating=4.7,
                slug="navushnyky-sony"
            ),
            Product(
                category=clothing,
                name="Футболка Nike",
                description="Спортивна футболка з дихаючого матеріалу",
                price=800,
                old_price=None,
                discount=0,
                stock=30,
                is_available=True,
                is_new=False,
                rating=4.2,
                slug="futbolka-nike"
            ),
            Product(
                category=clothing,
                name="Джинси Levi's",
                description="Класичні джинси прямого крою",
                price=2200,
                old_price=2500,
                discount=12,
                stock=8,
                is_available=True,
                is_new=False,
                rating=4.6,
                slug="dzhynsy-levis"
            ),
            Product(
                category=books,
                name="Книга 'Clean Code'",
                description="Роберт Мартін про чистий код",
                price=650,
                old_price=None,
                discount=0,
                stock=15,
                is_available=True,
                is_new=False,
                rating=4.9,
                slug="knyha-clean-code"
            ),
            Product(
                category=books,
                name="Книга 'Django для початківців'",
                description="Практичний посібник з Django",
                price=480,
                old_price=None,
                discount=0,
                stock=3,
                is_available=True,
                is_new=True,
                rating=4.4,
                slug="knyha-django-dlya-pochatkivciv"
            ),
        ]
        Product.objects.bulk_create(products)

        # Додаємо замовлення
        self.stdout.write('Додаємо замовлення...')
        
        orders_data = [
            {
                'product_id': 1,
                'product_name': 'Ноутбук Lenovo',
                'quantity': 1,
                'total_price': 32000.00,
                'customer_name': 'Іван Петренко',
                'phone': '+380501234567'
            },
            {
                'product_id': 3,
                'product_name': 'Навушники Sony',
                'quantity': 2,
                'total_price': 9000.00,
                'customer_name': 'Олена Коваленко',
                'phone': '+380671234567'
            },
            {
                'product_id': 6,
                'product_name': "Книга 'Clean Code'",
                'quantity': 3,
                'total_price': 1950.00,
                'customer_name': 'Михайло Шевченко',
                'phone': '+380931234567'
            }
        ]
        
        for order_data in orders_data:
            order, created = Order.objects.get_or_create(
                product_id=order_data['product_id'],
                customer_name=order_data['customer_name'],
                defaults=order_data
            )
            if created:
                self.stdout.write(f"✅ Створено замовлення: {order}")

        self.stdout.write(self.style.SUCCESS(
            f"Створено {Category.objects.count()} категорій, "
            f"{Product.objects.count()} товарів і "
            f"{Order.objects.count()} замовлень"
        ))