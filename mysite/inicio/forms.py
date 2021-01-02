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
        field=("id","codigo_usuario","descripcion","monto","tiempo","estado")

class pagoA(forms.Form):
    opcs = (("1", "Monetaria"), ("2", "Ahorro"))
    tipo_cuenta=forms.ChoiceField(required=True,label="Tipo de cuenta a utilizar:",choices=opcs)
    id_cuenta=forms.IntegerField(required=True,label="Número de cuenta:")
    id_prestamo=forms.IntegerField(required=True,label="Código del prestamo:")
    fecha=forms.DateField(required=True,label="Fecha:")
    contra=forms.CharField(required=True,label="Contraseña")

    class Meta:
        field=("id","codigo_usuario","tipo_cuenta","id_cuenta","id_prestamo","fecha","cuota","restante")

class pagoAde(forms.Form):
    id_pagoAuto=forms.IntegerField(required=True,label="Código del útlimo pago automático: ")
    fecha=forms.DateField(required=True,label="Fecha de transacción:")
    contra=forms.CharField(required=True,label="Contraseña ")

    class Meta:
        field=("id","id_pagoAuto","fecha","cuota","restante")

class pagoAd(forms.Form):
    opcs = (("1", "Monetaria"), ("2", "Ahorro"))
    tipo_cuenta = forms.ChoiceField(required=True, label="Tipo de cuenta a utilizar:", choices=opcs)
    id_cuenta = forms.IntegerField(required=True, label="Número de cuenta:")
    id_prestamo = forms.IntegerField(required=True, label="Código del prestamo:")
    fecha = forms.DateField(required=True, label="Fecha:")
    contra = forms.CharField(required=True, label="Contraseña")
    class Meta:
        field=("id","codigo_usuario","tipo_cuenta","id_cuenta","id_prestamo","fecha","cuota","restante")


class agregarProv(forms.Form):
    opc=(("1","MONETARIA"),("2","AHORRO"))
    opcs=(("QUINCENAL","QUINCENAL"),("MENSUAL","MENSUAL"))
    nombre=forms.CharField(required=True, label="Nombre del proveedor:" )
    tipo_cuenta=forms.ChoiceField(required=True, label="Tipo de cuenta del proveedor:", choices=opc)
    id_cuenta=forms.IntegerField(required=True, label="Número de cuenta del proveedor:")
    id_cuenta_cliente=forms.IntegerField(required=True, label="Número de cuenta con la que se desea pagar:")
    monto=forms.FloatField(required=True, label="Monto a cancelar: ")
    periodo_pago=forms.ChoiceField(required=True, label="Período de pago:",choices=opcs)

    class Meta:
        field=("id","id_cliente","id_cuenta_cliente","nombre","tipo_cuenta","id_cuenta","monto","periodo_pago")

class pagarProv(forms.Form):
    contrasenia=forms.CharField(required=True, label="Introduce la contraseña: ")
    class Meta:
        field=("contrasenia")