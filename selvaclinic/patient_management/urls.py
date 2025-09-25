from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome_page, name='welcome_page'),  # Welcome page at /patient/
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Manager URLs
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/patient/add/', views.add_patient, name='add_patient'),
    path('manager/patient/list/', views.manager_patient_list, name='manager_patient_list'),
    path('manager/patient/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    
    # Doctor URLs
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/patient/list/', views.doctor_patient_list, name='doctor_patient_list'),
    path('doctor/patient/<int:patient_id>/add-visit/', views.add_visit, name='add_visit'),
    path('doctor/patient/<int:patient_id>/history/', views.view_patient_history, name='patient_history'),
]