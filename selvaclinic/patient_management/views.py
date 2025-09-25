from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile, Patient, PatientVisit

def welcome_page(request):
    """Welcome page for the hospital website"""
    return render(request, 'patient_management/welcome.html')

def home_redirect(request):
    """Redirect to welcome page - used for root URL"""
    return redirect('welcome_page')

def is_manager(user):
    try:
        return user.userprofile.user_type == 'manager'
    except UserProfile.DoesNotExist:
        return False

def is_doctor(user):
    try:
        return user.userprofile.user_type == 'doctor'
    except UserProfile.DoesNotExist:
        return False

def register(request):
    if request.method == 'POST':
        # Get form data
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        user_type = request.POST['user_type']
        phone = request.POST.get('phone', '')
        
        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords don't match")
            return redirect('register')
        
        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')
        
        # Create user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password1
            )
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                user_type=user_type,
                phone=phone
            )
            
            messages.success(request, "Registration successful! Please login.")
            return redirect('login')
            
        except Exception as e:
            messages.error(request, f"Error creating user: {str(e)}")
            return redirect('register')
    
    return render(request, 'patient_management/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            
            # Redirect based on user type
            try:
                if user.userprofile.user_type == 'manager':
                    return redirect('manager_dashboard')
                else:
                    return redirect('doctor_dashboard')
            except UserProfile.DoesNotExist:
                messages.error(request, 'User profile not found. Please contact administrator.')
                return redirect('login')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'patient_management/login.html')

def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

@login_required
@user_passes_test(is_manager)
def manager_dashboard(request):
    patients = Patient.objects.filter(created_by=request.user)
    total_patients = patients.count()
    
    context = {
        'patients': patients,
        'total_patients': total_patients,
    }
    return render(request, 'patient_management/manager_dashboard.html', context)

@login_required
@user_passes_test(is_manager)
def add_patient(request):
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        gender = request.POST['gender']
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        
        # Create patient
        patient = Patient.objects.create(
            name=name,
            age=age,
            gender=gender,
            phone=phone,
            address=address,
            created_by=request.user
        )
        
        messages.success(request, 'Patient added successfully!')
        return redirect('manager_dashboard')
    
    return render(request, 'patient_management/add_patient.html')

@login_required
@user_passes_test(is_manager)
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id, created_by=request.user)
    visits = patient.visits.all().order_by('-visit_date')
    
    context = {
        'patient': patient,
        'visits': visits,
    }
    return render(request, 'patient_management/patient_detail.html', context)

@login_required
@user_passes_test(is_doctor)
def doctor_dashboard(request):
    patients = Patient.objects.all()
    my_visits = PatientVisit.objects.filter(doctor=request.user).order_by('-visit_date')[:10]
    
    context = {
        'patients': patients,
        'my_visits': my_visits,
    }
    return render(request, 'patient_management/doctor_dashboard.html', context)

@login_required
@user_passes_test(is_doctor)
def add_visit(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        diagnosis = request.POST['diagnosis']
        notes = request.POST.get('notes', '')
        medicine_prescribed = request.POST['medicine_prescribed']
        next_visit_date = request.POST.get('next_visit_date', None)
        
        # Create visit
        visit = PatientVisit.objects.create(
            patient=patient,
            doctor=request.user,
            diagnosis=diagnosis,
            notes=notes,
            medicine_prescribed=medicine_prescribed,
            next_visit_date=next_visit_date
        )
        
        messages.success(request, 'Visit details added successfully!')
        return redirect('doctor_dashboard')
    
    context = {
        'patient': patient,
    }
    return render(request, 'patient_management/add_visit.html', context)

@login_required
@user_passes_test(is_doctor)
def view_patient_history(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    visits = patient.visits.all().order_by('-visit_date')
    
    context = {
        'patient': patient,
        'visits': visits,
    }
    return render(request, 'patient_management/patient_history.html', context)

# NEW VIEWS FOR PATIENT LISTS
@login_required
@user_passes_test(is_manager)
def manager_patient_list(request):
    patients = Patient.objects.filter(created_by=request.user).order_by('-created_at')
    
    context = {
        'patients': patients,
    }
    return render(request, 'patient_management/manager_patient_list.html', context)

@login_required
@user_passes_test(is_doctor)
def doctor_patient_list(request):
    patients = Patient.objects.all().order_by('-created_at')
    
    context = {
        'patients': patients,
    }
    return render(request, 'patient_management/doctor_patient_list.html', context)
# ... existing imports ...

@login_required
@user_passes_test(is_doctor)
def add_visit(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        diagnosis = request.POST['diagnosis']
        notes = request.POST.get('notes', '')
        medicine_prescribed = request.POST['medicine_prescribed']
        next_visit_date = request.POST.get('next_visit_date') or None
        
        # Create visit
        visit = PatientVisit.objects.create(
            patient=patient,
            doctor=request.user,
            diagnosis=diagnosis,
            notes=notes,
            medicine_prescribed=medicine_prescribed,
            next_visit_date=next_visit_date
        )
        
        messages.success(request, 'Visit details added successfully!')
        return redirect('doctor_dashboard')
    
    context = {
        'patient': patient,
    }
    return render(request, 'patient_management/add_visit.html', context)

@login_required
@user_passes_test(is_doctor)
def view_patient_history(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    visits = patient.visits.all().order_by('-visit_date')
    
    context = {
        'patient': patient,
        'visits': visits,
    }
    return render(request, 'patient_management/patient_history.html', context)

@login_required
@user_passes_test(is_manager)
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id, created_by=request.user)
    visits = patient.visits.all().order_by('-visit_date')
    
    context = {
        'patient': patient,
        'visits': visits,
    }
    return render(request, 'patient_management/patient_detail.html', context)