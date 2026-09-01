from django.contrib import admin
from .models import Category, Product, Order

admin.site.register(Category)
admin.site.register(Product)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'product_name', 'quantity', 'total_price', 'phone', 'created_at']
    list_filter = ['created_at', 'customer_name']
    search_fields = ['customer_name', 'product_name', 'phone']
    readonly_fields = ['created_at']
    fields = ['product_id', 'product_name', 'quantity', 'total_price', 'customer_name', 'phone', 'created_at']