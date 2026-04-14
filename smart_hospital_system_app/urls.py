from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('doctors/', views.doctors, name='doctors'),
    path('about-us/', views.about_us, name='about_us'),
    path('ai/', views.ai, name='ai'),
    path('book/', views.book, name='book'),
]