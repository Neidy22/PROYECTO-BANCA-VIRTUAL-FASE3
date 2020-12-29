from django.shortcuts import render, redirect
from django.views.generic import *
from .forms import *

import MySQLdb
import sys

from .models import Usuario, Clienteempresarial, Cuentamonetaria, Cuentaahorro, Cuentafija, Clienteindividual

sys.path.append("models.py")



host='localhost'
db_name='django'
user='neidy'
contra='Auntyflores12031206'
puerto=3306

# Create your views here.
class Index(TemplateView):
    template_name = "index.html"

    def render_to_response(self, context, **response_kwargs):

        diccionario = {"form": self.form}
        # context.update(diccionario)

        return super().render_to_response(context, **response_kwargs)

    def indexView(request):
        form = Persona()

        if request.method == 'POST':
            form = Persona(data=request.POST)
            itemsPost = request.POST.items()
            print('este es el itempost')
            diccionarioSesion = {}
            usuario = ''
            contrasenia = ''
            codigo=''
            for key, value in request.POST.items():

                if key == 'usuario':
                    usuario = value
                if key == 'contrasenia':
                    contrasenia = value
                if key== 'codigo':
                    codigo=value

            if usuario=='admin':
                if contrasenia=="admindbs":
                    diccionarioSesion.update(codigo=codigo, usuario=usuario, contrasenia=contrasenia)
                    print(diccionarioSesion)
                    variableSesion = request.session['datos'] = diccionarioSesion
                    form=Persona()

                    return redirect('menuAd')

            else:


                try:
                    per=Usuario.objects.get(id=codigo)
                    p=per.contrasenia
                    u=per.usuario
                    codigoe=per.codigoe
                    print(codigoe)
                    codigoi=per.codigoi

                    if  u==usuario:
                        if p==contrasenia:


                            diccionarioSesion.update(usuario=usuario,contrasenia=contrasenia,codigo=codigo)
                            print(diccionarioSesion)
                            variableSesion = request.session['datos'] = diccionarioSesion
                            form=Persona()

                            return redirect('home')
                        else:
                            return  redirect('index')
                except Usuario.DoesNotExist:
                    return False

        return render(request, 'index.html', {'form': form})


class Home(TemplateView):
    template_name = "inicioCliente.html"

    def decirHola(request):
        diccionarioSesion = request.session['datos']
        codigo=diccionarioSesion.get('codigo')
        usuario = diccionarioSesion.get('usuario')
        contrasenia = diccionarioSesion.get('contrasenia')


        return render(request, 'inicioCliente.html', {'codigo': codigo, 'usuario': usuario, 'contrasenia':contrasenia})

class Admin(TemplateView):
    template_name = "menuAdmin.html"

    def enviar(request):
        diccionarioSesion = request.session['datos']
        codigo = diccionarioSesion.get('codigo')
        usuario = diccionarioSesion.get('usuario')
        contrasenia = diccionarioSesion.get('contrasenia')

        cl = Clienteempresarial.objects.get(id=codigoe)
        nombre = cl.nombre_empresa
        nombrec = cl.nombre_comercial
        tipo = cl.tipo
        representante = cl.nombre_representate
        direccion = cl.direccion
        tel = cl.telefono

        mone = Cuentamonetaria.objects.filter(codigo_usuario=codigo).values_list("id","fondo","monto_manejo","moneda")
        ahor = Cuentaahorro.objects.filter(codigo_usuario=codigo).values_list("id","fondo","tasa_interes","moneda")
        fija = Cuentafija.objects.filter(codigo_usuario=codigo).values_list("id","tasa_interes","fondo_total","moneda")
        variables={
            'Nombre':nombre,
            'Nombrec':nombrec,
            'Tipo':tipo,
            'Representante':representante,
            'Dirección':direccion,
            'Teléfono':tel,
            'Monetarias':mone,
            'Ahorros':ahor,
            'Fijas':fija

        }


        return render(request, 'menuAdmin.html', variables)
