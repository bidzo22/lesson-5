from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.contacts, name='contacts'),  # Це буде /contacts/
]