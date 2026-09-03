from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .data import PRODUCTS, ORDERS, VALID_CATEGORIES, CATEGORY_NAMES
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from .models import Product, Category, Order

#Допоміжні функції для фільтрації та сортування товарів
def product_to_dict(product_id, product):

    """Перетворює товар у словник для JSON-відповіді."""
    return {
        "id": product_id,
        "name": product["name"],
        "price": product["price"],
        "category": product["category"],
        "stock": product["stock"],
        "available": product["stock"] > 0,
    }

def get_product_source(product_id):
    """Шукає товар спочатку у словнику PRODUCTS, а якщо немає - у базі даних Product."""
    product = PRODUCTS.get(product_id)
    if product is not None:
        return product

    try:
        db_product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return None

    return {
        "name": db_product.name,
        "price": float(db_product.price),
        "category": db_product.category.slug if db_product.category else "",
        "stock": db_product.stock,
    }

def apply_filters(
    products_dict,
    sort=None,
    in_stock=False,
    min_price=None,
    max_price=None,
    categories=None,
):
    items = [product_to_dict(pid, p) for pid, p in products_dict.items()]

    if in_stock:
        items = [p for p in items if p["available"]]

    if min_price:
        items = [p for p in items if p["price"] >= int(min_price)]

    if max_price:
        items = [p for p in items if p["price"] <= int(max_price)]

    if categories:
        items = [p for p in items if p["category"] in categories]

    if sort == "price_asc":
        items.sort(key=lambda x: x["price"])
    elif sort == "price_desc":
        items.sort(key=lambda x: x["price"], reverse=True)
    elif sort == "name":
        items.sort(key=lambda x: x["name"])

    return items


def home(request):
    """Головна сторінка магазину"""
    total_products = Product.objects.count()
    available_products = Product.objects.filter(is_available=True, stock__gt=0).count()
    total_orders = Order.objects.count()  # Тепер Order визначено
    
    # Новинки
    new_products = Product.objects.filter(is_new=True, is_available=True)[:8]
    
    context = {
        'heading': 'Ласкаво просимо до нашого магазину!',
        'totalProducts': total_products,
        'available_products': available_products,
        'total_orders': total_orders,
        'new_products': new_products,
    }
    return render(request, 'store/home.html', context)


def product_list(request):
    sort = request.GET.get("sort", "")
    in_stock = request.GET.get("in_stock",) == "1"
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    categories = request.GET.getlist("category")

    products = apply_filters(
        PRODUCTS,
        sort=sort,
        in_stock=in_stock,
        min_price=min_price,
        max_price=max_price,
        categories=categories
    )

    return render(request, "store/product_list.html", {
    "products": products,
    "sort": sort,
    "in_stock": in_stock,
    "min_price": min_price,
    "max_price": max_price,
    "categories": categories,
    "category_names": CATEGORY_NAMES,
})

def product_detail(request, product_id):
    product = get_product_source(product_id)
    if product is None:
        return JsonResponse(
            {"error": "Товар не знайдено"},
            status=404,
            json_dumps_params={"ensure_ascii": False, "indent": 2})
    return JsonResponse(
        product_to_dict(product_id, product),
        json_dumps_params={"ensure_ascii": False, "indent": 2}   
    )


def category_view(request, category):

    if category not in VALID_CATEGORIES:
        return JsonResponse(
            {"error": "Невідома категорія"},
            status=400,
            json_dumps_params={"ensure_ascii": False, "indent": 2}
        )

    products = [
        product_to_dict(product_id, product)
        for product_id, product in PRODUCTS.items()
        if product["category"] == category
    ]

    return JsonResponse(
        {
            "category": category,
            "category_name": CATEGORY_NAMES[category],
            "count": len(products),
            "products": products
        },
        json_dumps_params={"ensure_ascii": False, "indent": 2}
    )


@csrf_exempt
def order_views(request, product_id):
    product = get_product_source(product_id)

    if product is None:
        return JsonResponse(
            {"error": "Товар не знайдено"},
            status=404,
            json_dumps_params={"ensure_ascii": False, "indent": 2}
        )

    # GET
    if request.method == "GET":
        return JsonResponse(
            {
                "product": product_to_dict(product_id, product),
                "hint": "Надішліть POST-запит з полями: name, quantity, phone"
            },
            json_dumps_params={"ensure_ascii": False, "indent": 2}
        )

    # POST
    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        quantity = request.POST.get("quantity", "").strip()

        errors = {}

        # name
        if not name:
            errors["name"] = "Ім'я є обов'язковим полем"

        # phone
        if not phone:
            errors["phone"] = "Телефон є обов'язковим полем"
        elif len(phone) < 10 or len(phone) > 13:
            errors["phone"] = "Телефон повинен містити від 10 до 13 символів"

        # quantity
        if not quantity:
            errors["quantity"] = "Кількість є обов'язковим полем"
        else:
            try:
                quantity = int(quantity)

                if quantity <= 0:
                    errors["quantity"] = "Кількість повинна бути більше 0"

                elif quantity > product["stock"]:
                    errors["quantity"] = (
                        f"На складі лише {product['stock']} шт."
                    )

            except ValueError:
                errors["quantity"] = "Кількість повинна бути цілим числом"

        # якщо є помилки
        if errors:
            return JsonResponse(
                {"errors": errors},
                status=400,
                json_dumps_params={"ensure_ascii": False, "indent": 2}
            )

        # створення замовлення
        order = {
            "order_id": len(ORDERS) + 1,
            "product_id": product_id,
            "product_name": product["name"],
            "quantity": quantity,
            "total_price": quantity * product["price"],
            "customer_name": name,
            "phone": phone,
        }

        ORDERS.append(order)

        # зменшуємо залишок товару
        product["stock"] -= quantity

        return redirect("order_list")
    
def order_list(request):
    if not ORDERS:
        return JsonResponse(
            {"message": "Замовлень пока немає", "orders": []}, 
            json_dumps_params={"ensure_ascii": False, "indent": 2})
    return JsonResponse(
        {
            "count": len(ORDERS),
            "orders": ORDERS
        },
          json_dumps_params={"ensure_ascii": False, "indent": 2}
    )

def search(request):
    is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"
    query = request.GET.get("q", "").strip()
    products = []

    if query:
        products = [
            product_to_dict(pid, p)
            for pid, p in PRODUCTS.items()
            if query.lower() in p["name"].lower()
        ]


    if is_ajax:
        return JsonResponse(
            {"products": products},
            json_dumps_params={"ensure_ascii": False}
        )

    return render(request, "store/search.html", {
        "query": query,
        "products": products
    })

    
def old_catalog(request):
    response = redirect('products_list', permanent=True)
    response['X-Redirect-Reason'] = 'page-deprecated'
    return response