from django import forms
from administracion.models import Usuario
class Persona(forms.Form):
    codigo = forms.CharField(max_length=20, required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Introduce tu código de usuario'}))
    usuario = forms.CharField(max_length=20, required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Introduce tu nombre de usuario'}))

    class Meta:
        field = ("id","codigoE","codigoI","usuario","contrasenia")


class compra(forms.Form):
    opc=(("Q","QUETZALES"),("$","DÓLARES"))
    fecha=forms.DateField(label="Ingresa la fecha de compra en año-mes-día:")
    descripcion=forms.CharField(required=True, label="Descripción de la compra: ")
    monto=forms.FloatField(required=True,label="Monto total de la compra: ")
    codigo_tarjeta=forms.IntegerField(required=True, label="Introduce el código de tarjeta:")
    moneda=forms.ChoiceField(required=True,label="Monto total en:",choices=opc)

    class Meta:
        field=("id","fecha","descripcion","monto","codigo_tarjeta","moneda","puntos","cashback")