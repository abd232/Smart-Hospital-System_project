import email

from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import User, Patient, Doctor, Section,Clinic, MedicalRecord, Appointment
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Section, Clinic, Doctor
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
    sections = Section.objects.all().order_by('name')
    clinics = Clinic.objects.all().order_by('name')

    doctors_qs = Doctor.objects.select_related(
        'user', 'clinic', 'clinic__section'
    ).order_by('user__first_name', 'user__last_name')

    paginator = Paginator(doctors_qs, 9)
    page_obj = paginator.get_page(1)

    context = {
        'sections': sections,
        'clinics': clinics,
        'page_obj': page_obj,
    }
    return render(request, 'patient/doctors.html', context)


def doctors_filter_ajax(request):
    section_id = request.GET.get('section', '').strip()
    clinic_id = request.GET.get('clinic', '').strip()
    search = request.GET.get('search', '').strip()
    page = request.GET.get('page', 1)

    clinics_qs = Clinic.objects.all().order_by('name')
    doctors_qs = Doctor.objects.select_related(
        'user', 'clinic', 'clinic__section'
    ).order_by('user__first_name', 'user__last_name')

    # filter clinics by selected section
    if section_id:
        clinics_qs = clinics_qs.filter(section_id=section_id)
        doctors_qs = doctors_qs.filter(clinic__section_id=section_id)

    # filter doctors by selected clinic
    if clinic_id:
        doctors_qs = doctors_qs.filter(clinic_id=clinic_id)

    # search doctors
    if search:
        doctors_qs = doctors_qs.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(specialty__icontains=search) |
            Q(clinic__name__icontains=search) |
            Q(clinic__section__name__icontains=search)
        )

    paginator = Paginator(doctors_qs, 9)
    page_obj = paginator.get_page(page)

    doctors_html = render(
        request,
        'patient/partials/doctors_cards.html',
        {'page_obj': page_obj}
    ).content.decode('utf-8')

    clinics_data = list(clinics_qs.values('id', 'name'))

    return JsonResponse({
        'clinics': clinics_data,
        'doctors_html': doctors_html,
    })

def create_appointment(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        date_str = request.POST.get('date')
        time_str = request.POST.get('selected_time')

        doctor = get_object_or_404(Doctor, id=doctor_id)
        patient = get_object_or_404(Patient, user=request.user)

        appointment_datetime = datetime.strptime(
            f"{date_str} {time_str}",
            "%Y-%m-%d %I:%M %p"
        )

        notes = request.POST.get('notes', '')

        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            clinic=doctor.clinic,
            appointment_date=appointment_datetime,
            notes=notes
        )

        return redirect('doctors')

    return redirect('doctors')

def ai(request):
    # Implement AI-related logic here
    return render(request, 'patient/ai.html')

def about_us(request):
    return render(request, 'patient/about_us.html')

def contact_us(request):
    return render(request, 'patient/contact_us.html')

def book(request):
    if request.method == 'POST':
        # Handle booking logic here
        pass
    return render(request, 'patient/booking.html')