from django.urls import path, include
from .views import *
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'user', ProfileViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'records', MedicalRecordViewSet)
router.register(r'feedback', FeedbackViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),


    path('', DepartmentsListAPIView.as_view(), name='Departments_list'),
    path('patients/', PatientListAPIVew.as_view(), name='patients_list'),
    path('patients/<int:pk>/', PatientRetrieveDestroyAPIView.as_view(), name='patients_detail'),
    path('doctors/', DoctorListAPIVew.as_view(), name='doctors_list'),
    path('doctors/<int:pk>/', DoctorRetrieveUpdateAPIView.as_view(), name='doctors_detail'),


]

