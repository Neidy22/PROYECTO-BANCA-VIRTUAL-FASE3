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

            if usuario=='admin':
                if contrasenia=="admindbs":
                    diccionarioSesion.update(codigo=codigo, usuario=usuario, contrasenia=contrasenia)
                    print(diccionarioSesion)
                    variableSesion = request.session['datos'] = diccionarioSesion
                    form=Persona()

                    return redirect('menuAd')

            #else:



            per=Usuario.objects.get(id=codigo)
            p=per.contrasenia
            u=per.usuario
            codigoe=per.codigoe.codigo
            codigoi=per.codigoi.codigo
            print(codigoe,codigoi)
            if  u==usuario:
                if p==contrasenia:
                    diccionarioSesion.update(usuario=usuario,contrasenia=contrasenia,codigo=codigo)
                    print(diccionarioSesion)
                    variableSesion = request.session['datos'] = diccionarioSesion
                    form=Persona()
                    if codigoe>0:
                        return redirect('empresarial')
                    elif codigoi>0:
                        return redirect('individual')


                    else:
                        return  redirect('index')


        return render(request, 'index.html', {'form': form})


class Home(TemplateView):
    template_name = "inicioCliente.html"

    def decirHola(request):
        diccionarioSesion = request.session['datos']
        codigo=diccionarioSesion.get('codigo')
        usuario = diccionarioSesion.get('usuario')
        contrasenia = diccionarioSesion.get('contrasenia')


        return render(request, 'inicioCliente.html', {'codigo': codigo, 'usuario': usuario, 'contrasenia':contrasenia})

class Empre(TemplateView):
    template_name = "menuEmpresarial.html"
    def enviar(request):
        diccionarioSesion = request.session['datos']
        codigo = diccionarioSesion.get('codigo')
        usuario = diccionarioSesion.get('usuario')
        contrasenia = diccionarioSesion.get('contrasenia')

        return render(request, 'menuEmpresarial.html', {'codigo': codigo, 'usuario': usuario, 'contrasenia': contrasenia})


class Admin(TemplateView):
    template_name = "menuAdmin.html"

    def enviar(request):
        diccionarioSesion = request.session['datos']
        codigo = diccionarioSesion.get('codigo')
        usuario = diccionarioSesion.get('usuario')
        contrasenia = diccionarioSesion.get('contrasenia')


        variables={
            'Nombre':codigo,


        }


        return render(request, 'menuAdmin.html', variables)

class soli(TemplateView):
    template_name = "prestamo.html"

    def solicitud(request):
        form = solicitudPrestamo()
        nombre = "Solicitar préstamo"
        variables = {
            "form": form,
            "mensaje": nombre
        }
        if request.method == "POST":
            form = solicitudPrestamo(data=request.POST)
            if form.is_valid():
                datos = form.cleaned_data
                descripcion = datos.get("descripcion")
                monto = datos.get("monto")
                tiempo = datos.get("tiempo")
                id = 0
                estado=0
                print(tiempo, type(tiempo))
                diccionarioSesion = request.session['datos']
                usuario = diccionarioSesion.get('codigo')
                if tiempo != '0':
                    insertarSolicitud(id, usuario, descripcion, monto, tiempo,estado)
                    nombre = "Solicitud enviada"
                    form = solicitudPrestamo()
                    variables = {
                        "form": form,
                        "mensaje": nombre
                    }
                    #return redirect('solicitud')
                else:
                    a = cotizar(monto)
                    print(len(a))
                    print(a)
                    variables = {
                        "form": form,
                        # "mensaje": nombre,
                        "list": a
                    }
                   # return redirect('solicitud')


            else:
                nombre = "Ocurrión un error"
                variables = {
                    "form": form,
                    "mensaje": nombre

                }
        return render(request, 'prestamo.html', variables)



def insertarSolicitud(id,usuario,descripcion,monto,tiempo,estado):
    db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
    c = db.cursor()
    consulta = "INSERT INTO solicitudPrestamo VALUES(" + str(id) + ","+str(usuario)+",'"+str(descripcion)+"',"+str(monto)+","+str(tiempo)+","+str(estado)+")"
    c.execute(consulta)
    db.commit()
    c.close()

def cotizar(monto):
    lista=[]

    if monto>=1000 and monto<=5000:
        sin=monto/12
        con=(monto/12)+((monto/12)*0.05)
        lista.append(sin)
        lista.append(con)
        sin2=monto/24
        con2=(monto/24)+((monto/24)*0.04)
        lista.append(sin2)
        lista.append(con2)
        sin3 = monto / 36
        con3 = (monto / 36) + ((monto / 36) * 0.0335)
        lista.append(sin3)
        lista.append(con3)
        sin4=monto/48
        con4=(monto/48)+((monto/48)*0.025)
        lista.append(sin4)
        lista.append(con4)
    elif monto>=5000.01 and monto<=15000:
        sin=monto/12
        con=(monto/12)+((monto/12)*0.0525)
        lista.append(sin)
        lista.append(con)
        sin2=monto/24
        con2=(monto/24)+((monto/24)*0.0415)
        lista.append(sin2)
        lista.append(con2)
        sin3 = monto / 36
        con3 = (monto / 36) + ((monto / 36) * 0.035)
        lista.append(sin3)
        lista.append(con3)
        sin4=monto/48
        con4=(monto/48)+((monto/48)*0.026)
        lista.append(sin4)
        lista.append(con4)
    elif monto>=15000.01 and monto<=30000:
        sin=monto/12
        con=(monto/12)+((monto/12)*0.053)
        lista.append(sin)
        lista.append(con)
        sin2=monto/24
        con2=(monto/24)+((monto/24)*0.042)
        lista.append(sin2)
        lista.append(con2)
        sin3 = monto / 36
        con3 = (monto / 36) + ((monto / 36) * 0.0355)
        lista.append(sin3)
        lista.append(con3)
        sin4=monto/48
        con4=(monto/48)+((monto/48)*0.0265)
        lista.append(sin4)
        lista.append(con4)
    elif monto>=30000.01 and monto<=60000:
        sin=monto/12
        con=(monto/12)+((monto/12)*0.0535)
        lista.append(sin)
        lista.append(con)
        sin2=monto/24
        con2=(monto/24)+((monto/24)*0.0425)
        lista.append(sin2)
        lista.append(con2)
        sin3 = monto / 36
        con3 = (monto / 36) + ((monto / 36) * 0.036)
        lista.append(sin3)
        lista.append(con3)
        sin4=monto/48
        con4=(monto/48)+((monto/48)*0.027)
        lista.append(sin4)
        lista.append(con4)
    elif monto>=60000.01:
        sin=monto/12
        con=(monto/12)+((monto/12)*0.0545)
        lista.append(sin)
        lista.append(con)
        sin2=monto/24
        con2=(monto/24)+((monto/24)*0.0435)
        lista.append(sin2)
        lista.append(con2)
        sin3 = monto / 36
        con3 = (monto / 36) + ((monto / 36) * 0.037)
        lista.append(sin3)
        lista.append(con3)
        sin4=monto/48
        con4=(monto/48)+((monto)*0.028)
        lista.append(sin4)
        lista.append(con4)

    for i in range(len(lista)):
        lista[i]=round(lista[i],2)

    return lista










