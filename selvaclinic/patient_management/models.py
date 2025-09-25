from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.age})"

class PatientVisit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_visits')
    visit_date = models.DateTimeField(default=timezone.now)
    diagnosis = models.TextField()
    notes = models.TextField(blank=True, null=True)
    medicine_prescribed = models.TextField()
    next_visit_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Visit for {self.patient.name} by Dr. {self.doctor.username}"

class UserProfile(models.Model):
    USER_TYPES = [
        ('manager', 'Manager'),
        ('doctor', 'Doctor'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"