from django import forms
from django.forms import ModelForm
from .models import Registrado

class RegForm(ModelForm):
    class Meta:
        model = Registrado
        fields = ['email', 'nombre']
    
    #Validaciones sobreescribo clean_email
    def clean_email(self):
        email = self.cleaned_data.get("email")
        email_base, proveedor = email.split("@")
        dominio, extension = proveedor.split(".")
        if extension != "edu":
            raise forms.ValidationError("Ingrese un email con la extension .edu")
        return email

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        return nombre