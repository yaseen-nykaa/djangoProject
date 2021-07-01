from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'inventory'
urlpatterns = [
    path('', views.get_products, name='products'),
    path('all/',views.product_view,name='product_view'),
    path('detail/', views.prod_detail_view, name='detail'),
    path('add/', views.prod_add_view, name='add'),
    path('delete/<int:sku_id>', views.prod_delete, name='delete'),
    path('updateView/<int:sku_id>', views.prod_update_view, name='update_view'),
    path('update/<int:sku_id>', views.prod_update, name='update'),
]