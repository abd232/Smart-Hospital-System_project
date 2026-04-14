from datetime import date
import email

from django.shortcuts import get_object_or_404, render
from .models import Note, User, Patient, Doctor, Section, Clinic, MedicalRecord, Appointment
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from .models import Patient, Doctor, Clinic, Appointment, Note
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

@login_required
def doctor_dashboard(request):
    if not hasattr(request.user, 'doctor'):
        return redirect('/')

    doctor = request.user.doctor
    appointments = Appointment.objects.filter(doctor=doctor)

    context = {
        "appointments": appointments[:5],
        "today_count": appointments.filter(appointment_date__date=date.today()).count(),
        "patients_count": Patient.objects.filter(appointments__doctor=doctor).distinct().count(),
        "pending_count": appointments.filter(status='pending').count(),
        "confirmed_count": appointments.filter(status='confirmed').count(),
        "cancelled_count": appointments.filter(status='cancelled').count(),
    }

    return render(request, "doctor/dashboard.html", context)
@login_required
def doctor_appointments(request):
    if not hasattr(request.user, 'doctor'):
        return redirect('/')

    doctor = request.user.doctor
    appointments = Appointment.objects.filter(doctor=doctor)

    return render(request, "doctor/appointments.html", {
        "appointments": appointments
    })
@login_required
def accept_appointment(request, id):
    doctor = request.user.doctor
    appointment = get_object_or_404(Appointment, id=id, doctor=doctor)

    appointment.status = "confirmed"
    appointment.save()

    return redirect("appointments")


@login_required
def cancel_appointment(request, id):
    doctor = request.user.doctor
    appointment = get_object_or_404(Appointment, id=id, doctor=doctor)

    appointment.status = "cancelled"
    appointment.save()

    return redirect("appointments")

@login_required
def accept_appointment(request, id):
    doctor = request.user.doctor
    appointment = get_object_or_404(Appointment, id=id, doctor=doctor)

    appointment.status = "confirmed"
    appointment.save()

    return redirect("appointments")


@login_required
def cancel_appointment(request, id):
    doctor = request.user.doctor
    appointment = get_object_or_404(Appointment, id=id, doctor=doctor)

    appointment.status = "cancelled"
    appointment.save()

    return redirect("appointments")
@login_required
def doctor_patients(request):
    if not hasattr(request.user, 'doctor'):
        return redirect('/')

    doctor = request.user.doctor

    patients = Patient.objects.filter(
        appointments__doctor=doctor
    ).distinct()

    return render(request, "doctor/patients.html", {
        "patients": patients
    })
@login_required
def patient_detail(request, id):
    if not hasattr(request.user, 'doctor'):
        return redirect('/')

    doctor = request.user.doctor
    patient = get_object_or_404(Patient, id=id)

    appointments = Appointment.objects.filter(
        patient=patient,
        doctor=doctor
    )

    if request.method == "POST":
        Note.objects.create(
            doctor=doctor,
            patient=patient,
            content=request.POST.get("note")
        )

    return render(request, "doctor/patient_detail.html", {
        "patient": patient,
        "appointments": appointments
    })

def ai(request):
    # Implement AI-related logic here
    return render(request, 'patient/ai.html')

def book(request):
    if request.method == 'POST':
        # Handle booking logic here
        pass
    return render(request, 'patient/booking.html')

# ------------------ Dashboard ------------------
def doctor_dashboard(request):
    doctor = Doctor.objects.filter(user=request.user).first()

    appointments = Appointment.objects.filter(doctor=doctor)

    context = {
        "appointments": appointments[:5],
        "today_count": appointments.filter(appointment_date__date=date.today()).count(),
        "patients_count": Patient.objects.count(),
        "pending_count": appointments.filter(status='pending').count(),
        "confirmed_count": appointments.filter(status='confirmed').count(),
        "cancelled_count": appointments.filter(status='cancelled').count(),
    }

    return render(request, "doctor/dashboard.html", context)


# ------------------ Appointments ------------------
def doctor_appointments(request):
    doctor = Doctor.objects.filter(user=request.user).first()
    appointments = Appointment.objects.filter(doctor=doctor)

    return render(request, "doctor/appointments.html", {
        "appointments": appointments
    })


# ------------------ Accept Appointment ------------------
def accept_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    appointment.status = "confirmed"
    appointment.save()
    return redirect("appointments")


# ------------------ Cancel Appointment ------------------
def cancel_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    appointment.status = "cancelled"
    appointment.save()
    return redirect("appointments")


# ------------------ Patients ------------------
def doctor_patients(request):
    doctor = Doctor.objects.filter(user=request.user).first()
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
            doctor=Doctor.objects.filter(user=request.user).first(),
            patient=patient,
            content=request.POST.get("note")
        )

    return render(request, "doctor/patient_detail.html", {
        "patient": patient,
        "appointments": appointments
    })

def sections(request):
    sections = Section.objects.all()
    return render(request, "patient/sections.html", {"sections": sections})


def clinics(request, section_id):
    clinics = Clinic.objects.filter(section_id=section_id)
    return render(request, "patient/clinics.html", {"clinics": clinics})


def doctors_by_clinic(request, clinic_id):
    doctors = Doctor.objects.filter(clinic_id=clinic_id)
    return render(request, "patient/doctors.html", {"doctors": doctors})


def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == "POST":
        Appointment.objects.create(
            patient=request.user.patient,
            doctor=doctor,
            clinic=doctor.clinic,
            appointment_date=request.POST.get("appointment_date")
        )
        return redirect("/")

    return render(request, "patient/booking.html", {"doctor": doctor})