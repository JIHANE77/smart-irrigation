from django import forms
from .models import Parcelle

class ParcelleForm(forms.ModelForm):
    class Meta:
        model = Parcelle
        fields = '__all__'