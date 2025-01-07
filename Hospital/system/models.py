from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField

ROLE_CHOICES = (
    ('врач', 'Врач'),
    ('пациент', 'Пациент'),
)


class Profile(AbstractUser):
    user_role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='пациент')
    phone_number = PhoneNumberField(region='KG', null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Departments(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    WORKING_DAYS_CHOICES = (
        ('пн', 'пн'),
        ('вт', 'вт'),
        ('ср', 'ср'),
        ('чт', 'чт'),
        ('пт', 'пт'),
        ('сб', 'сб'),
        ('вс', 'вс'),
        ('круглосуточно', 'круглосуточно')
    )
    phone_number = PhoneNumberField(region='KG', null=True, blank=True)
    shift_start = models.TimeField(null=True, blank=True)
    shift_end = models.TimeField(null=True, blank=True)
    working_days = MultiSelectField(max_length=50, choices=WORKING_DAYS_CHOICES, max_choices=7, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class Doctor(models.Model):
    doctor_profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='doctor_profile')
    department = models.ForeignKey(Departments, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='department_doctor')
    speciality = models.CharField(max_length=50)
    departament = models.CharField(max_length=50)
    qualifications = models.CharField(max_length=25, null=True, blank=True)
    shift_start = models.TimeField()
    shift_end = models.TimeField()
    WORKING_DAYS_CHOICES = (
        ('пн', 'пн'),
        ('вт', 'вт'),
        ('ср', 'ср'),
        ('чт', 'чт'),
        ('пт', 'пт'),
        ('сб', 'сб'),
        ('вс', 'вс'),
    )
    working_days = MultiSelectField(max_length=16, choices=WORKING_DAYS_CHOICES, max_choices=7)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.doctor_profile}'


class Patient(models.Model):
    user_profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='patient_profile')
    emergency_contact = models.CharField(max_length=30, null=True, blank=True)
    blood_type = models.CharField(max_length=10, null=True, blank=True)
    allergies = models.TextField(null=True, blank=True)
    medical_history = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.user_profile}'


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('Запланировано', 'Запланировано'),
        ('Завершено', 'Завершено'),
        ('Отменено', 'Отменено')
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_appointments')
    date_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Запланировано')

    def __str__(self):
        return f'{self.patient}, {self.doctor}'


class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='one_medical_records')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='two_medical_records')
    diagnosis = models.TextField()
    treatment = models.TextField(null=True, blank=True)
    prescribed_medication = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.patient}'


class Feedback(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_feedbacks')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_feedbacks')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.patient}'


class Chat(models.Model):
    person = models.ManyToManyField(Profile)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    chat_text = models.TextField()
    image = models.ImageField(upload_to='chat/image/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

