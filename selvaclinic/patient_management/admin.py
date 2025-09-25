from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Patient, PatientVisit, UserProfile

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'gender', 'phone', 'created_by', 'created_at']
    list_filter = ['gender', 'created_at']
    search_fields = ['name', 'phone']

@admin.register(PatientVisit)
class PatientVisitAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'visit_date', 'diagnosis']
    list_filter = ['visit_date', 'doctor']
    search_fields = ['patient__name', 'diagnosis']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'phone']
    list_filter = ['user_type']