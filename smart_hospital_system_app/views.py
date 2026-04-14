import email

from django.shortcuts import render
from .models import User, Patient, Doctor, Section, Clinic, MedicalRecord, Appointment
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
# Create your views here.

def index(request):
    return render(request, 'patient/index.html')

def login(request):
    if request.method == 'POST':
        errors = Patient.objects.validate_login(request.POST)
        if errors:
            context={
                'errors' : errors,
            }
            return render(request , 'account/login.html' , context=context)            
        else:
            user = User.objects.filter(email=request.POST.get('email')).first()     
            auth_login(request, user)
            return redirect("/")
    return render(request, 'account/login.html')

def register(request):
    if request.method == 'POST':
        errors = Patient.objects.validate_registration(request.POST)
        if errors:
            context={
                'errors' : errors,
            }
            return render(request , 'account/register.html' , context=context)
        else:
            Patient.objects.create_patient(request.POST)
            return redirect('/login/')
    return render(request, 'account/register.html')

def doctors(request):
    # Fetch doctor data from the database and pass it to the template
    doctors = []  # Replace with actual doctor data
    return render(request, 'patient/doctors.html', {'doctors': doctors})

def ai(request):
    # Implement AI-related logic here
    return render(request, 'patient/ai.html')

def about_us(request):
    return render(request, 'patient/about_us.html')

def book(request):
    if request.method == 'POST':
        # Handle booking logic here
        pass
    return render(request, 'patient/booking.html')