from django.shortcuts import render, redirect
from django.views.generic import *
from .forms import *

import MySQLdb
import sys

from administracion.models import Usuario

sys.path.append("models.py")



host='localhost'
db_name='django'
user='neidy'
contra='Auntyflores12031206'
puerto=3306

# Create your views here.
class Index(TemplateView):
    template_name = "loginTienda.html"

    def render_to_response(self, context, **response_kwargs):

        diccionario = {"form": self.form}
        # context.update(diccionario)

        return super().render_to_response(context, **response_kwargs)

    def indexView(request):
        form = Persona()

        if request.method == 'POST':
            form = Persona(data=request.POST)
            itemsPost = request.POST.items()
         #   print('este es el itempost')
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


            per=Usuario.objects.get(id=codigo)
            p=per.contrasenia
            u=per.usuario
            codigoe=per.codigoe.codigo
            codigoi=per.codigoi.codigo
            print(codigoe,codigoi)
            if  u==usuario:
                #if p==contrasenia:
                diccionarioSesion.update(usuario=usuario,contrasenia=contrasenia,codigo=codigo)
                print(diccionarioSesion)
                variableSesion = request.session['datos'] = diccionarioSesion
                form=Persona()
                return redirect('homeTienda')


            else:
                return  redirect('indexT/')


        return render(request, 'loginTienda.html', {'form': form})


class Home(TemplateView):
    template_name = "comprar.html"

    def comprar(request):
        form = compra()

        nombre = "Realizar compras con tarjeta de crédito"
        variables = {
            "form": form,
            "mensaje": nombre
        }

        if request.method == "POST":
            form = compra(data=request.POST)

            if form.is_valid():
                datos = form.cleaned_data
                fecha = datos.get("fecha")

                nombre = "Nueva compra registrada"
                form = compra()

                variables = {
                    "form": form,
                    "mensaje": nombre

                }
                # asignarUsuario(0, codigo, 0, nombre_comercial, contrau, tarjetas)
            else:
                nombre = "Ya existe un cliente con los mismos datos"
                variables = {
                    "form": form,

                    "mensaje": nombre

                }

        return render(request, 'comprar.html', variables)






def comprar(request):
    form = compra()

    nombre = "Realizar compras con tarjeta de crédito"
    variables = {
        "form": form,
        "mensaje": nombre
    }

    if request.method == "POST":
        form = compra(data=request.POST)

        if form.is_valid():
            datos = form.cleaned_data
            fecha = datos.get("fecha")


            nombre = "Nuevo cliente registrado"
            form = compra()

            variables = {
                "form": form,
                "mensaje": nombre

            }
            #asignarUsuario(0, codigo, 0, nombre_comercial, contrau, tarjetas)
        else:
            nombre = "Ya existe un cliente con los mismos datos"
            variables = {
                "form": form,

                "mensaje": nombre

            }

    return render(request, 'formCompra.html', variables)

def insertarCompra(id,fecha,desc,monto,codigo,moneda,puntos,cash):
    db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
    c = db.cursor()
    consulta = "INSERT INTO compra VALUES(" + str(id) + ",'"+str(fecha)+"','"+str(desc)+"',"+str(monto)+","+str(codigo)+",'"+str(moneda)+"',"+str(puntos)+","+str(cash) +")"
    db.commit()
    c.close()

