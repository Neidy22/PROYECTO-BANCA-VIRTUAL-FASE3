from django.shortcuts import render, redirect
from django.views.generic import *
from .forms import *

import MySQLdb
import sys

from .models import Usuario, Prestamo, Pagoautomatico


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


class pagoAutomatico(TemplateView):
    template_name = "cuotaAuto.html"

    def pagar(request):
        form =pagoA()
        nombre = "Pagar automáticamente"
        variables = {
            "form": form,
            "mensaje": nombre
        }
        if request.method == "POST":
            form = pagoA(data=request.POST)
            if form.is_valid():
                datos = form.cleaned_data
                tipo=datos.get("tipo_cuenta")
                idCuenta=datos.get("id_cuenta")
                prestamo=datos.get("id_prestamo")
                fecha=datos.get("fecha")
                passw=datos.get("contra")
                diccionarioSesion = request.session['datos']
                usuario = diccionarioSesion.get('codigo')
                contrasenia=diccionarioSesion.get('contrasenia')
                id=0
                tp=int(tipo)


                if passw==contrasenia:
                    pres = Prestamo.objects.get(id=prestamo)
                    total = pres.total
                    tiempo = pres.modalidad_pago
                    cuota = total / tiempo

                    actualizarPrestamo(prestamo, cuota)

                    cancelado = pres.pagado
                    total = total - cancelado



                    if tp == 1:
                        cuenta=Cuentamonetaria.objects.get(id=idCuenta)
                        moneda=cuenta.moneda
                        fondo=cuenta.fondo

                        saldo = calcularSaldo(moneda, fondo, cuota)
                        db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
                        c = db.cursor()
                        consulta = "UPDATE cuentaMonetaria SET fondo= '" + str(saldo) + "'  WHERE id=" + str(idCuenta)
                        c.execute(consulta)
                        db.commit()
                        c.close()
                        print(consulta)
                    elif tp == 2:
                        cuenta = Cuentaahorro.objects.get(id=idCuenta)
                        moneda = cuenta.moneda
                        fondo = cuenta.fondo

                        saldo = calcularSaldo(moneda, fondo, cuota)

                        db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
                        c = db.cursor()
                        consulta = "UPDATE cuentaAhorro SET fondo= '" + str(saldo) + "' WHERE id=" + str(idCuenta)
                        c.execute(consulta)
                        db.commit()
                        c.close()
                        print(consulta)




                    insertarPagoA(id,usuario,tipo,idCuenta,prestamo,fecha,cuota,total)


                    nombre = "Pago automático registrado!"
                    form=pagoA()
                    variables = {
                        "form": form,
                        "mensaje": nombre

                    }
                else:
                    nombre = "La contraseña es incorrecta!"
                    variables = {
                        "form": form,
                        "mensaje": nombre

                    }



            else:
                nombre = "Ocurrión un error"
                variables = {
                    "form": form,
                    "mensaje": nombre

                }
        return render(request, 'cuotaAuto.html', variables)


class pagoAdelantado(TemplateView):
    template_name = "cuotaAdelantada.html"

    def adelantar(request):
        form = pagoAde()
        nombre = "Pagar cuota adelantada"
        variables = {
            "form": form,
            "mensaje": nombre
        }
        if request.method == "POST":
            form = pagoAde(data=request.POST)
            if form.is_valid():
                datos = form.cleaned_data
                idAuto=datos.get("id_pagoAuto")
                fecha=datos.get("fecha")
                passw=datos.get("contra")

                diccionarioSesion = request.session['datos']
                usuario = diccionarioSesion.get('codigo')
                contrasenia=diccionarioSesion.get('contrasenia')
                iden=0

                pago=Pagoautomatico.objects.get(id=idAuto)
                tipo=pago.tipo_cuenta
                idCuenta=pago.id_cuenta
                idPres=pago.id_prestamo.id


                tp=int(tipo)
                print(tp)


                if passw==contrasenia:
                    pres = Prestamo.objects.get(id=idPres)
                    total = pres.total
                    tiempo = pres.modalidad_pago
                    cuota = total / tiempo
                    actualizarPrestamo(idPres, cuota)

                    cancelado = pres.pagado
                    total = total - cancelado
                    solicitado=pres.monto



                    if tp == 1:
                        cuenta = Cuentamonetaria.objects.get(id=idCuenta)
                        moneda = cuenta.moneda
                        fondo = cuenta.fondo
                        cuotaL=solicitado/tiempo
                        saldo = calcularSaldo(moneda, fondo, cuotaL)

                        db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
                        c = db.cursor()
                        consulta = "UPDATE cuentaMonetaria SET fondo= '" + str(saldo) + "'  WHERE id=" + str(idCuenta)
                        c.execute(consulta)
                        db.commit()
                        c.close()
                        print(consulta)

                    elif tp == 2:


                        cuenta = Cuentaahorro.objects.get(id=idCuenta)
                        moneda = cuenta.moneda
                        fondo = cuenta.fondo
                        cuotaL = solicitado / tiempo

                        saldo = calcularSaldo(moneda, fondo, cuotaL)

                        db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
                        c = db.cursor()
                        consulta = "UPDATE cuentaAhorro SET fondo= '" + str(saldo) + "' WHERE id=" + str(idCuenta)
                        c.execute(consulta)
                        db.commit()
                        c.close()
                        print(consulta)


                    #actualizarPrestamo(idPres, cuota)

                    insertarPagoAde(iden,idAuto,fecha,cuotaL,total)


                    nombre = "Pago adelantado registrado!"
                    form=pagoAde()
                    variables = {
                        "form": form,
                        "mensaje": nombre

                    }
                else:
                    nombre = "La contraseña es incorrecta!"
                    variables = {
                        "form": form,
                        "mensaje": nombre

                    }



            else:
                nombre = "Ocurrió un error"
                variables = {
                    "form": form,
                    "mensaje": nombre

                }


        return render(request, 'cuotaAdelantada.html', variables)





def actualizarPrestamo(prestamo,cuota):
    prest=Prestamo.objects.get(id=prestamo)
    pagado=prest.pagado
    pagos=pagado+cuota

    db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
    c = db.cursor()
    consulta = "UPDATE prestamo SET pagado= '" + str(pagos) + "'  WHERE id=" + str(prestamo)
    c.execute(consulta)
    db.commit()
    c.close()

def obtenerCuotayRestante(prestamo):
    pres=Prestamo.objects.get(id=prestamo)
    total=pres.total
    tiempo=pres.modalidad_pago
    cuota=total/tiempo
    restante=total-cuota
    return cuota,restante

def debitarCuota(tipo,cuenta,cuota):
    if tipo==1:
        cuenta=Cuentamonetaria.objects.get(id=cuenta)
        moneda=cuenta.moneda
        fondo=cuenta.fondo
        saldo=calcularSaldo(moneda,fondo,cuota)
        print(saldo)
        if saldo>0:
            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
            c = db.cursor()
            consulta = "UPDATE cuentaMonetaria SET fondo= '" + str(saldo) + "'  WHERE id=" + str(cuenta)
            c.execute(consulta)
            db.commit()
            c.close()

    elif tipo==2:
        cuenta=Cuentaahorro.objects.get(id=cuenta)
        moneda=cuenta.moneda
        fondo=cuenta.fondo
        saldo=calcularSaldo(moneda,fondo,cuota)
        if saldo > 0:
            db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
            c = db.cursor()
            consulta = "UPDATE cuentaAhorro SET fondo= '" + str(saldo) + "' WHERE id=" + str(cuenta)
            c.execute(consulta)
            db.commit()
            c.close()

def calcularSaldo(moneda,fondo,cuota):
    saldo=0
    if moneda=="Q":
        saldo=fondo-cuota
    elif moneda=="$":
        saldo=fondo-(cuota/7.63)
    return saldo

def insertarSolicitud(id,usuario,descripcion,monto,tiempo,estado):
    db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
    c = db.cursor()
    consulta = "INSERT INTO solicitudPrestamo VALUES(" + str(id) + ","+str(usuario)+",'"+str(descripcion)+"',"+str(monto)+","+str(tiempo)+","+str(estado)+")"
    c.execute(consulta)
    db.commit()
    c.close()

def insertarPagoA(id,usuario,tipoC,idC,idPre,fecha,cuota,restante):
    db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
    c = db.cursor()
    consulta = "INSERT INTO pagoAutomatico VALUES(" + str(id) + "," + str(usuario) + ",'" + str(
        tipoC) + "'," + str(idC) + "," + str(idPre) + ",'" + str(fecha) +"',"+str(cuota)+","+str(restante)+ ")"
    c.execute(consulta)
    db.commit()
    c.close()

def insertarPagoAde(id,id_pago,fecha,cuota,restante):
    db = MySQLdb.connect(host=host, user=user, password=contra, db=db_name, connect_timeout=5)
    c = db.cursor()
    consulta = "INSERT INTO pagoAdelantado VALUES(" + str(id) + "," + str(id_pago) + ",'"+ str(fecha) +"',"+str(cuota)+","+str(restante)+ ")"
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










