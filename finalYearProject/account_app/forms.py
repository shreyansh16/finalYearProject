from django import forms
from .models import User, Patient, Doctor
from django.contrib.auth.forms import UserCreationForm



class PatientRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    middle_name = forms.CharField(required=False)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    contact_no = forms.CharField(required=True)
    header_image = forms.ImageField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User

class DoctorRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    middle_name = forms.CharField(required=False)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    contact_no = forms.CharField(required=True)
    fees = forms.IntegerField(required=True)
    experience = forms.IntegerField(required=True)
    degrees = forms.CharField(required=True)
    header_image = forms.ImageField(required=True)
    doctor_reg_id = forms.CharField(required=True)
    degree_certificate = forms.FileField(required=True)
    chamber_address = forms.CharField(widget=forms.Textarea)

    class Meta(UserCreationForm.Meta):
        model = User

class AdminRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    middle_name = forms.CharField(required=False)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    contact_no = forms.CharField(required=True)
    header_image = forms.ImageField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User






