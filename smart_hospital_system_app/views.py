import email

from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import ProfileForm, User, Patient, Doctor, Section,Clinic, MedicalRecord, Appointment
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Section, Clinic, Doctor
from django.contrib.auth.decorators import login_required

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
            is_doctor = hasattr(user, 'doctor')
            if is_doctor:
                return redirect('/doctor/dashboard/')
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
def logout_view(request):
    logout(request)
    return redirect('index') 

def signout(request):
    logout(request)
    return redirect('/login/')

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

        doctor = get_object_or_404(Doctor, id=doctor_id)
        patient = get_object_or_404(Patient, user=request.user)

        appointment_date = datetime.strptime(date_str, "%Y-%m-%d").date()

        notes = request.POST.get('notes', '')

        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            clinic=doctor.clinic,
            appointment_date=appointment_date,
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
@login_required
def profile(request):
    return render(request, 'profile.html')
@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})

def doctor_dashboard(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    print(doctor)
    appointments = Appointment.objects.filter(doctor=doctor)
    print(appointments)
    if appointments is not None:
        context = {
            "appointments": appointments[:5],
            "today_count": appointments.filter(appointment_date__date=datetime.today()).count(),
            "patients_count": Patient.objects.count(),
            "pending_count": appointments.filter(status='pending').count(),
            "confirmed_count": appointments.filter(status='confirmed').count(),
            "cancelled_count": appointments.filter(status='cancelled').count(),
        }

        return render(request, "doctor/index.html", context=context)
    else:
        context = {
            "appointments": [],
            "today_count": 0,
            "patients_count": Patient.objects.count(),
            "pending_count": 0,
            "confirmed_count": 0,
            "cancelled_count": 0,
        }
        return render(request, "doctor/index.html", context=context)


# ------------------ Appointments ------------------
def doctor_appointments(request):
    doctor = request.user.doctor
    appointments = Appointment.objects.filter(doctor=doctor)

    return render(request, "doctor/appointments.html", {
        "appointments": appointments
    })


# ------------------ Accept Appointment ------------------
def accept_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    appointment.status = "confirmed"
    appointment.save()
    return redirect("doctor_dashboard")


# ------------------ Cancel Appointment ------------------
def cancel_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    appointment.status = "cancelled"
    appointment.save()
    return redirect("doctor_dashboard")


# ------------------ Patients ------------------
def doctor_patients(request):
    doctor = request.user.doctor
    patients = Patient.objects.filter(appointments__doctor=doctor).distinct()

    return render(request, "doctor/patients.html", {
        "patients": patients
    })


# ------------------ Patient Detail ------------------
def patient_detail(request, id):
    patient = get_object_or_404(Patient, id=id)
    appointments = Appointment.objects.filter(patient=patient)

    if request.method == "POST":
        Note.objects.create(
            doctor=request.user.doctor,
            patient=patient,
            content=request.POST.get("note")
        )

    return render(request, "doctor/patient_detail.html", {
        "patient": patient,
        "appointments": appointments
    })

def patient_appointments(request):
    patient = Patient.objects.get(user=request.user)

    scheduled_appointments = Appointment.objects.filter(
        patient=patient,
        status='confirmed'
    ).order_by('appointment_date')

    pending_appointments = Appointment.objects.filter(
        patient=patient,
        status='pending'
    ).order_by('appointment_date')

    cancelled_appointments = Appointment.objects.filter(
        patient=patient,
        status='cancelled'
    ).order_by('-appointment_date')

    context = {
        'scheduled_appointments': scheduled_appointments,
        'pending_appointments': pending_appointments,
        'cancelled_appointments': cancelled_appointments,
    }
    return render(request, 'patient/appointments.html', context)
