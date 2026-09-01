from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('order/<int:product_id>', views.order_views, name='order_views'),
    path('orders/', views.order_list, name='order_list'),
    path('search/', views.search, name='search'),


    path('category/<str:category>/', views.category_view, name='category_view'),
    path('old-catalog/', views.old_catalog, name='old_catalog'),
]