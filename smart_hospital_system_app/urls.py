from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('doctors/', views.doctors, name='doctors'),
    path('doctors/filter/', views.doctors_filter_ajax, name='doctors_filter_ajax'),
    path('appointments/create/', views.create_appointment, name='create_appointment'),
    path('ai/', views.ai, name='ai'),
    path('book/', views.book, name='book'),
]