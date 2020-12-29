from django import forms
from .models import Usuario, Clienteempresarial, Cuentamonetaria, Cuentaahorro, Cuentafija
class Persona(forms.Form):
    codigo = forms.CharField(max_length=20, required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Introduce tu código de usuario'}))
    usuario = forms.CharField(max_length=20, required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Introduce tu nombre de usuario'}))
    contrasenia = forms.CharField(max_length=20, required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Introduce tu contraseña'}))

    class Meta:
        field = ("id","codigoE","codigoI","usuario","contrasenia")