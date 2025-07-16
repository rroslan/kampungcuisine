from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('order/<str:order_number>/', views.order_detail_view, name='order_detail'),
    path('orders/', views.order_list_view, name='order_list'),
    path('cancel/<str:order_number>/', views.cancel_order_view, name='cancel_order'),
]
