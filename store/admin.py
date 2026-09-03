from django.contrib import admin
from .models import Category, Product, Order, Comment, Attribute, AttributeValue, ProductAttribute

admin.site.register(Category)
admin.site.register(Product)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'product_name', 'quantity', 'total_price', 'phone', 'created_at']
    list_filter = ['created_at', 'customer_name']
    search_fields = ['customer_name', 'product_name', 'phone']
    readonly_fields = ['created_at']
    fields = ['product_id', 'product_name', 'quantity', 'total_price', 'customer_name', 'phone', 'created_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'author', 'comment', 'created_at']
    list_filter = ['created_at', 'product']
    search_fields = ['comment', 'author__username', 'product__name']
    readonly_fields = ['created_at']

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ['id', 'attribute', 'value']
    list_filter = ['attribute']
    search_fields = ['value']


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'attribute_value']
    list_filter = ['attribute_value__attribute']
    search_fields = ['product__name']
