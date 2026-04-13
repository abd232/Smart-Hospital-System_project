from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('doctors/', views.doctors, name='doctors'),
    path('ai/', views.ai, name='ai'),
    path('book/', views.book, name='book'),
    path('appointments/', views.doctor_appointments, name="appointments"),
    path('patients/', views.doctor_patients, name="patients"),
    path('patients/<int:id>/', views.patient_detail, name="patient_detail"),

    path('accept/<int:id>/', views.accept_appointment, name="accept_appointment"),
    path('cancel/<int:id>/', views.cancel_appointment, name="cancel_appointment"),
]