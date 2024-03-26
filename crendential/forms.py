from django import forms
from .models import Crendential


class CrendentialForm(forms.ModelForm):
    class Meta:
        model = Crendential
        exclude = "course","user"