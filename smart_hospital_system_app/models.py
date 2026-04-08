import bcrypt
from django.contrib.auth.models import User
from django.db import models
# Create your models here.

class UserManager(models.Manager):
    def create_customer(self,post_data):
        user = User.objects.create_user(username=post_data['username'], email=post_data['email'], password=post_data['password'])
        patient = Patient.objects.create(user=user, phone=post_data['phone'], address=post_data['address'])
        return patient
    
    def validate_login(self,post_data):
        errors={}
        email = post_data.get('email' , '')
        password = post_data.get('password' , '')
        user = User.objects.filter(email=email).first()
        if user:
            if not user.check_password(password):
                errors['user'] = 'Email or password not valid'
        else:
            errors['user'] = 'Email or password not valid'
        return errors
    def validate_registration(self,post_data):
        errors={}
        if len(post_data['username']) < 3:
            errors['username'] = 'Username must be at least 3 characters long'
        if len(post_data['email']) < 5:
            errors['email'] = 'Email must be at least 5 characters long'
        if len(post_data['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters long'
        if post_data['password'] != post_data['confirm_password']:
            errors['confirm_password'] = 'Passwords do not match'
        if User.objects.filter(email=post_data['email']).exists():
            errors['email'] = 'Email already exists'
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

    def __str__(self):
        return self.user.username

    
class Section(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Clinic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE , related_name='clinics')
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
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE , related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE , related_name='appointments')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE , related_name='appointments')
    appointment_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient.user.username} - {self.doctor.user.username} - {self.clinic.name} - {self.appointment_date}"