from django.urls import path
from . import views


app_name = 'card'

urlpatterns = [
    path('', views.card_detail, name='card_detail'),
    path('add/<int:product_id>/', views.card_add, name='card_add'),
    path('remove/<int:product_id>/', views.card_remove, name='card_remove'),
]