from django import forms
from .models import Specialization


class AddCategoryForm(forms.ModelForm):
    category = forms.CharField(required=True)

    class Meta:
        model = Specialization
        fields=['category','header_image']