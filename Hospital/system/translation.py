from .models import *
from modeltranslation.translator import TranslationOptions, register


@register(Departments)
class DepartmentsTranslationOp(TranslationOptions):
    fields = ['name', 'address', 'description']


@register(Doctor)
class DoctorTranslationOp(TranslationOptions):
    fields = ['qualifications']


@register(Patient)
class PatientTranslationsOp(TranslationOptions):
    fields = ['allergies', 'medical_history']

