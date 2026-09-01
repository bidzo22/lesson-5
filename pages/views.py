from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages
from store.models import Product, Order  # Додаємо Order

# Create your views here.

def home(request):
    """Головна сторінка з новинками"""
    # Статистика
    total_products = Product.objects.count()
    available_products = Product.objects.filter(is_available=True, stock__gt=0).count()
    total_orders = Order.objects.count()
    
    new_products = Product.objects.filter(is_new=True, is_available=True)[:8]
    
    context = {
        'heading': 'Ласкаво просимо до нашого магазину!',
        'totalProducts': total_products,
        'available_products': available_products,
        'total_orders': total_orders,
        'new_products': new_products,
    }
    return render(request, 'pages/home.html', context)

def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            agree = form.cleaned_data['agree']  

            print(name, email, message, agree)

            messages.success(request, "Повідомлення успішно надіслано!")
            return redirect('contacts')
        
        else:
            return render(request, 'pages/contacts.html', {'form': form})

    form = ContactForm()
    return render(request, 'pages/contacts.html', {'form': form})