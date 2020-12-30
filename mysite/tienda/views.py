from django.shortcuts import render, redirect
from django.views.generic import *
from .forms import *

import MySQLdb
import sys

from administracion.models import Usuario

from administracion.models import Tarjetacredito

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
        nombre = "Comprar con tarjeta de crédito"
        variables = {
            "form": form,
            "mensaje": nombre
        }
        if request.method == "POST":
            form = compra(data=request.POST)
            if form.is_valid():
                datos = form.cleaned_data
                fecha = datos.get("fecha")
                desc = datos.get("descripcion")
                monto = datos.get("monto")
                cod_tarjeta = datos.get("codigo_tarjeta")
                moneda = datos.get("moneda")
                pts = 0
                prc = 0
                id = 0

                diccionarioSesion = request.session['datos']
                user = diccionarioSesion.get('codigo')

                print(user)

                print(type(user))
                tarjetaU=Tarjetacredito.objects.get(id=cod_tarjeta)
                us=tarjetaU.codigo_usuario.id
                ficha=tarjetaU.moneda
                marca=tarjetaU.marca
                punt=tarjetaU.puntos
                porc=tarjetaU.porcentaje
                print(us)
                print(type(us))
                usuT=str(us)
                print("Este es: "+usuT)
                print(type(usuT))
                per=verificarPertenencia(user,usuT)
                if per==1:
                    print("pertenece")
                    alc,total=verificarFondo(monto,moneda,cod_tarjeta)
                    if alc==1:
                        pts,prc=calculos(marca,monto,moneda,ficha)
                        print(pts,prc)
                        insertarCompra(id,fecha,desc,monto,cod_tarjeta,moneda,pts,prc)
                        punt=punt+pts
                        porc=porc+prc
                        actualizarTarjeta(cod_tarjeta,punt,porc)

                        nombre = "Compra exitosa"
                        form=compra()
                        variables = {
                            "form": form,
                            "mensaje": nombre

                        }
                    else:
                        nombre = "El total de la compra excede el límite de tu tarjeta!"

                        variables = {
                            "form": form,
                            "mensaje": nombre
                        }

                else:
                    print("no pertenece")
                    nombre = "No tienes tarjeta de crédito con ese código!"

                    variables = {
                        "form": form,
                        "mensaje": nombre
                    }






            else:
                nombre = "Ya existe una  con los mismos datos"
                variables = {
                    "form": form,
                    "mensaje": nombre

                }
        return render(request, 'comprar.html', variables)



def calculos(marca,monto,moneda,ficha):
    puntos=0
    porcentajes=0
    if marca=="PREFEPUNTOS":
        puntos=calcularPuntos(monto,moneda,ficha)
    elif marca=="CASHBACK":
        porcentajes=calcularPorcentajes(monto,moneda,ficha)

    return puntos,porcentajes

def verificarPertenencia(usuarioS,usuarioT):
    pertenece=0
    if usuarioS==usuarioT:
        pertenece=1
    else:
        pertenece=0
    return pertenece

def verificarFondo(monto,moneda,id):
    alcanza=0
    tarj=Tarjetacredito.objects.get(id=id)
    ficha=tarj.moneda
    fondo=tarj.limite
    marca=tarj.marca
    gasto=tipoCambio(monto,ficha,moneda,marca)
    if gasto<=fondo:
        alcanza=1
    else:
        alcanza=0
    return alcanza,gasto

def tipoCambio(monto,ficha,moneda,marca):
    cambio=0
    if ficha=="Q" and moneda=="Q":
        cambio=monto
    elif ficha=="$" and moneda=="Q":
        if marca=="PREFEPUNTOS":
            cambio=monto/7.63
        elif marca=="CASHBACK":
            cambio=monto/7.87
    elif ficha=="Q" and moneda=="$":
        if marca=="PREFEPUNTOS":
            cambio=monto*7.63
        elif marca=="CASHBACK":
            cambio=monto*7.87
    elif ficha=="$" and moneda=="$":
        cambio=monto

    return cambio

def insertarCompra(id,fecha,descripcion,monto,codigo,moneda,puntos,cashback):
    db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
    c = db.cursor()
    consulta = "INSERT INTO compra VALUES(" + str(id) +",'"+str(fecha)+"','"+str(descripcion)+"',"+str(monto)+","+str(codigo)+",'"+str(moneda)+"',"+str(puntos)+","+str(cashback)+")"
    c.execute(consulta)
    db.commit()
    c.close()

def calcularPuntos(monto,moneda,ficha):
    puntos=0
    if moneda=="Q" and ficha=="Q":
        if monto>=0.01 and monto<=100:
            puntos=0
        elif monto>=100.01 and monto<=500:
            puntos=monto*0.02
        elif monto>=500.01 and monto<=2000:
            puntos=monto*0.04
        elif monto>=2000.01:
            puntos=monto*0.05
    elif moneda=="Q" and ficha=="$":
        if monto>=0.01 and monto<=100:
            puntos=0
        elif monto>=100.01 and monto<=500:
            puntos=(monto*0.02)/7.63
        elif monto>=500.01 and monto<=2000:
            puntos=(monto*0.04)/7.63
        elif monto>=2000.01:
            puntos=(monto*0.05)/7.63
    elif moneda=="$" and ficha=="Q":
        monto=monto*7.63
        if monto >= 0.01 and monto <= 100:
            puntos = 0
        elif monto >= 100.01 and monto <= 500:
            puntos = monto * 0.02
        elif monto >= 500.01 and monto <= 2000:
            puntos = monto * 0.04
        elif monto >= 2000.01:
            puntos = monto * 0.05
    elif moneda=="$" and ficha=="$":
        monto = monto * 7.63
        if monto>=0.01 and monto<=100:
            puntos=0
        elif monto>=100.01 and monto<=500:
            puntos=(monto*0.02)/7.63
        elif monto>=500.01 and monto<=2000:
            puntos=(monto*0.04)/7.63
        elif monto>=2000.01:
            puntos=(monto*0.05)/7.63
    return puntos

def calcularPorcentajes(monto,moneda,ficha):
    porcentajes=0
    if moneda=="Q" and ficha=="Q":
        if monto>=0.01 and monto<=200:
            porcentajes=0
        elif monto>=200.01 and monto<=700:
            porcentajes=monto*0.02
        elif monto>=700.01:
            porcentajes=monto*0.05
    elif moneda=="Q" and ficha=="$":
        if monto>=0.01 and monto<=200:
            porcentajes=0
        elif monto>=200.01 and monto<=700:
            porcentajes=(monto*0.02)/7.87
        elif monto>=700.01:
            porcentajes=(monto*0.05)/7.87
    elif moneda=="$" and ficha=="Q":
        monto=monto*7.87
        if monto>=0.01 and monto<=200:
            porcentajes=0
        elif monto>=200.01 and monto<=700:
            porcentajes=monto*0.02
        elif monto>=700.01:
            porcentajes=monto*0.05
    elif moneda=="$" and ficha=="$":
        monto=monto*7.87
        if monto>=0.01 and monto<=200:
            porcentajes=0
        elif monto>=200.01 and monto<=700:
            porcentajes=(monto*0.02)/7.87
        elif monto>=700.01:
            porcentajes=(monto*0.05)/7.87
    return porcentajes

def actualizarTarjeta(tarjeta,puntos,porcentajes):
    porc=int(porcentajes)
    db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
    c = db.cursor()
    consulta = "UPDATE tarjetaCredito SET puntos= '" + str(puntos) + "' WHERE id=" + str(tarjeta)
    c.execute(consulta)
    db.commit()
    c.close()
    db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
    c = db.cursor()
    consulta = "UPDATE tarjetaCredito SET porcentaje= '" + str(porc) + "' WHERE id=" + str(tarjeta)
    c.execute(consulta)
    db.commit()
    c.close()








