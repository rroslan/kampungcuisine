from django.urls import path
from pages import views

app_name = 'pages'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about_us, name='about'),
    path('contact/', views.contact_us, name='contact'),
    path('contact/success/', views.contact_success, name='contact_success'),
]
