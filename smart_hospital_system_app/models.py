from datetime import date, datetime
from email import errors

import bcrypt
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django import forms



class UserManager(models.Manager):
    def create_patient(self,post_data):
        first_name = post_data['first_name']
        last_name = post_data['last_name']
        email = post_data['email']
        password = post_data['password']
        password_hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(first_name=first_name , last_name=last_name , username=email, email=email , password=password_hashed)
        patient = Patient.objects.create(user=user, date_of_birth=post_data['date_of_birth'], phone=post_data['phone'], address=post_data['address'])
        return patient
    
    def validate_login(self,post_data):
        errors={}
        email = post_data.get('email' , '')
        password = post_data.get('password' , '')
        user = User.objects.filter(email=email).first()
        if user:
            if not bcrypt.checkpw(password.encode(), user.password.encode()):
                errors['user'] = 'Email or password not valid'
        else:
            errors['user'] = 'Email or password not valid'
        return errors
    def validate_registration(self,post_data):
        errors={}
        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'First name must be at least 2 characters long'
        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 characters long'
        if len(post_data['email']) < 5:
            errors['email'] = 'Email must be at least 5 characters long'
        if User.objects.filter(email=post_data['email']).exists():
            errors['email'] = 'Email already exists'
        if len(post_data['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters long'
        if post_data['password'] != post_data['confirm_password']:
            errors['confirm_password'] = 'Passwords do not match'
        dob = post_data.get('date_of_birth', '')
        if not dob:
            errors['date_of_birth'] = 'Date of birth is required'
        else:
            try:
                dob_date = datetime.strptime(dob, '%Y-%m-%d').date()
                if dob_date > date.today():
                    errors['date_of_birth'] = 'Date of birth cannot be in the future'
            except ValueError:
                errors['date_of_birth'] = 'Invalid date format'
        if post_data['phone'] and len(post_data['phone']) < 4:
            errors['phone'] = 'Phone number must be at least 4 characters long'
        if post_data['address'] and len(post_data['address']) < 10:
            errors['address'] = 'Address must be at least 10 characters long'
        return errors

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.user.username
    
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    clinic = models.ForeignKey('Clinic', on_delete=models.CASCADE, related_name='doctors')
    def __str__(self):
        return self.user.username


class Clinic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    section = models.ForeignKey('Section', on_delete=models.CASCADE, related_name='clinics')
    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class MedicalRecord(models.Model):
    option = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE , related_name='medical_records')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE , related_name='medical_records')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE , related_name='medical_records')
    diagnosis = models.TextField()
    treatment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=option, default='active')

    def __str__(self):
        return f"{self.patient.user.username} - {self.doctor.user.username} - {self.clinic.name} - {self.created_at}"

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE , related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE , related_name='appointments')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE , related_name='appointments')
    appointment_date = models.DateTimeField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    def __str__(self):
        return f"{self.patient.user.username} - {self.doctor.user.username} - {self.clinic.name} - {self.appointment_date}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    experience = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.username
@receiver(post_save, sender=User) 
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['specialization', 'phone', 'experience', 'location', 'image']
    
class AIChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_chat_sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return "Chat {} - {}".format(self.id, self.user.username)


class AIChatMessage(models.Model):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('assistant', 'Assistant'),
    )

    session = models.ForeignKey(AIChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.role, self.session.id)