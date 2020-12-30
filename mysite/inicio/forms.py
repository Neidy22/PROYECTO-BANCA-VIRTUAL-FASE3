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


class solicitudPrestamo(forms.Form):
    opc=(("0","cotizar"),("12","12 meses"),("24","24 meses"),("36","36 meses"),("48", "48 meses"))
    monto=forms.FloatField(required=True, label="Monto que solicitas:")
    descripcion=forms.CharField(required=True, label="Describe brevemente el uso que le pretendes dar al dinero:")
    tiempo=forms.ChoiceField(required=True, label="Tiempo en meses en el que pretendes pagar:",choices=opc)

    class Meta:
        field=("id","codigo_usuario","descripcion","monto","tiempo")
