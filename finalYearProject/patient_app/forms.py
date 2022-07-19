from django import forms
from .models import Appointment, Reviews, DocumentUpload

class AppointmentForm(forms.ModelForm):


    p_middle_name = forms.CharField(required=False)
    visit_reason =  forms.CharField(required=False)

    class Meta:
        model = Appointment
        #fields = ['p_first_name', 'p_middle_name', 'p_last_name', 'p_contact_no', 'p_email' , 'p_age', 'a_time', 'visit_reason']
        fields = ['a_time','a_date']


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Reviews
        fields = ['review']

class DocumentUplaodForm(forms.ModelForm):

    class Meta:
        model = DocumentUpload
        fields = ['p_name','document_name','document']




