from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('doctors/', views.doctors, name='doctors'),
    path('doctors/filter/', views.doctors_filter_ajax, name='doctors_filter_ajax'),
    path('appointments/create/', views.create_appointment, name='create_appointment'),
    path('about-us/', views.about_us, name='about_us'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('ai/', views.ai, name='ai'),
    path('book/', views.book, name='book'),
    path('appointments/', views.doctor_appointments, name="appointments"),
    path('doctor/dashboard/', views.doctor_dashboard, name="doctor_dashboard"),
    path('patients/', views.doctor_patients, name="patients"),
    path('patients/<int:id>/', views.patient_detail, name="patient_detail"),
    path('patient/appointments/', views.patient_appointments, name="patient_appointments"),
    path('accept/<int:id>/', views.accept_appointment, name="accept_appointment"),
    path('cancel/<int:id>/', views.cancel_appointment, name="cancel_appointment"),
]