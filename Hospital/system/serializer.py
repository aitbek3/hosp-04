from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('username', 'email', 'password', 'last_name', 'first_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Profile.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Неверные учетные данные')

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'first_name', 'last_name',  'user_role', 'phone_number', 'profile_picture']


class DoctorListSerializer(serializers.ModelSerializer):
    doctor_profile = ProfileSerializer()

    class Meta:
        model = Doctor
        fields = ['id', 'doctor_profile', 'speciality', 'department',]


class DoctorDetailSerializer(serializers.ModelSerializer):
    doctor_profile = ProfileSerializer()
    shift_start = serializers.TimeField(format='%H:%M')
    shift_end = serializers.TimeField(format='%H:%M')

    class Meta:
        model = Doctor
        fields = ['id', 'doctor_profile', 'speciality', 'department', 'shift_start', 'shift_end',
                  'working_days', 'price']


class DepartmentSerializer(serializers.ModelSerializer):
    shift_start = serializers.TimeField(format='%H:%M')
    shift_end = serializers.TimeField(format='%H:%M')

    class Meta:
        model = Departments
        fields = ['id', 'name', 'description', 'address', 'phone_number', 'shift_start', 'shift_end', 'working_days']


class PatientListSerializer(serializers.ModelSerializer):
    user_profile = ProfileSerializer()

    class Meta:
        model = Patient
        fields = ['id', 'user_profile']


class PatientDetailSerializer(serializers.ModelSerializer):
    user_profile = ProfileSerializer()

    class Meta:
        model = Patient
        fields = ['id', 'user_profile', 'emergency_contact', 'blood_type', 'allergies', 'medical_history']


class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientListSerializer()
    doctor = DoctorListSerializer()
    date_time = serializers.DateTimeField(format='%d-%m-%Y - %H:%M')

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'date_time', 'status']


class FeedbackSerializer(serializers.ModelSerializer):
    doctor = DoctorListSerializer()
    patient = PatientListSerializer()

    class Meta:
        model = Feedback
        fields = ['id', 'doctor', 'patient', 'rating', 'comment', 'created_at']


class MedicalRecordSerializer(serializers.ModelSerializer):
    patient = PatientDetailSerializer()
    doctor = DoctorDetailSerializer()
    created_at = serializers.DateTimeField(format='%d-%m-%Y - %H:%M')

    class Meta:
        model = MedicalRecord
        fields = ['id', 'patient', 'doctor', 'diagnosis', 'treatment', 'prescribed_medication', 'created_at']
