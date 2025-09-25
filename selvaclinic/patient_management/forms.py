from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Patient, PatientVisit, UserProfile

class CustomUserCreationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('manager', 'Manager'),
        ('doctor', 'Doctor'),
    ]
    
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)
    phone = forms.CharField(max_length=15, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'gender', 'phone', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class PatientVisitForm(forms.ModelForm):
    class Meta:
        model = PatientVisit
        fields = ['diagnosis', 'notes', 'medicine_prescribed', 'next_visit_date']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'medicine_prescribed': forms.Textarea(attrs={'rows': 3}),
            'next_visit_date': forms.DateInput(attrs={'type': 'date'}),
        }