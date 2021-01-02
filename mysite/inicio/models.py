# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Cheque(models.Model):
    codigo_chequera = models.ForeignKey('Chequera', models.DO_NOTHING, db_column='codigo_chequera')
    fecha_emision = models.DateField(blank=True, null=True)
    nombre_portador = models.CharField(max_length=100, blank=True, null=True)
    monto = models.FloatField(blank=True, null=True)
    autorizado = models.IntegerField(blank=True, null=True)
    cobrado = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cheque'
        unique_together = (('id', 'codigo_chequera'),)


class Chequera(models.Model):
    codigo_monetaria = models.ForeignKey('Cuentamonetaria', models.DO_NOTHING, db_column='codigo_monetaria')
    codigo_ahorro = models.ForeignKey('Cuentaahorro', models.DO_NOTHING, db_column='codigo_ahorro')
    fecha_emision = models.DateField(blank=True, null=True)
    cheques_disponibles = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chequera'
        unique_together = (('id', 'codigo_monetaria', 'codigo_ahorro'),)


class Clienteempresarial(models.Model):
    codigo = models.IntegerField(primary_key=True)
    tipo = models.CharField(max_length=50)
    nombre_comercial = models.CharField(max_length=100)
    nombre_empresa = models.CharField(max_length=100)
    nombre_representante = models.CharField(max_length=150, blank=True, null=True)
    direccion = models.CharField(max_length=300, blank=True, null=True)
    telefono = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clienteempresarial'
        unique_together = (('codigo', 'tipo', 'nombre_comercial', 'nombre_empresa'),)


class Clienteindividual(models.Model):
    codigo = models.IntegerField(primary_key=True)
    cui = models.BigIntegerField()
    nit = models.IntegerField()
    nombre = models.CharField(max_length=100, blank=True, null=True)
    nacimiento = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    telefono = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clienteindividual'
        unique_together = (('codigo', 'cui', 'nit'),)


class Compra(models.Model):
    fecha = models.DateField(blank=True, null=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    monto = models.FloatField(blank=True, null=True)
    codigo_tarjeta = models.ForeignKey('Tarjetacredito', models.DO_NOTHING, db_column='codigo_tarjeta', blank=True, null=True)
    moneda = models.CharField(max_length=1, blank=True, null=True)
    puntos = models.FloatField(blank=True, null=True)
    cashback = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'compra'


class Cuentaahorro(models.Model):
    codigo_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='codigo_usuario')
    fondo = models.FloatField(blank=True, null=True)
    tasa_interes = models.FloatField(blank=True, null=True)
    promocion = models.FloatField(blank=True, null=True)
    moneda = models.CharField(max_length=1, blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)
    pre_auto = models.IntegerField(blank=True, null=True)
    cheques_disponibles = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cuentaahorro'
        unique_together = (('id', 'codigo_usuario'),)


class Cuentafija(models.Model):
    codigo_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='codigo_usuario')
    cuota = models.FloatField(blank=True, null=True)
    capitalizacion = models.IntegerField(blank=True, null=True)
    tasa_interes = models.FloatField(blank=True, null=True)
    fondo_total = models.FloatField(blank=True, null=True)
    moneda = models.CharField(max_length=1, blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cuentafija'
        unique_together = (('id', 'codigo_usuario'),)


class Cuentamonetaria(models.Model):
    id = models.IntegerField(primary_key=True)
    codigo_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='codigo_usuario')
    fondo = models.FloatField(blank=True, null=True)
    monto_manejo = models.FloatField(blank=True, null=True)
    moneda = models.CharField(max_length=1, blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)
    pre_auto = models.IntegerField(blank=True, null=True)
    cheques_disponibles = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cuentamonetaria'
        unique_together = (('id', 'codigo_usuario'),)


class Deposito(models.Model):
    depositante = models.IntegerField(blank=True, null=True)
    receptor = models.IntegerField(blank=True, null=True)
    tipo_receptor = models.IntegerField(blank=True, null=True)
    monto = models.FloatField(blank=True, null=True)
    moneda = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'deposito'


class Pagoadelantado(models.Model):
    codigo_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='codigo_usuario', blank=True, null=True)
    tipo_cuenta = models.IntegerField(blank=True, null=True)
    id_cuenta = models.IntegerField(blank=True, null=True)
    id_prestamo = models.ForeignKey('Prestamo', models.DO_NOTHING, db_column='id_prestamo', blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    cuota = models.FloatField(blank=True, null=True)
    restante = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pagoadelantado'


class Pagoautomatico(models.Model):
    codigo_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='codigo_usuario', blank=True, null=True)
    tipo_cuenta = models.IntegerField(blank=True, null=True)
    id_cuenta = models.IntegerField(blank=True, null=True)
    id_prestamo = models.ForeignKey('Prestamo', models.DO_NOTHING, db_column='id_prestamo', blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    cuota = models.FloatField(blank=True, null=True)
    restante = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pagoautomatico'


class Planilla(models.Model):
    id_empresa = models.ForeignKey(Clienteempresarial, models.DO_NOTHING, db_column='id_empresa', blank=True, null=True)
    tipo_cuenta = models.IntegerField(blank=True, null=True)
    id_cuenta = models.IntegerField(blank=True, null=True)
    periodo = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'planilla'


class Prestamo(models.Model):
    codigo_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='codigo_usuario')
    monto = models.FloatField(blank=True, null=True)
    modalidad_pago = models.IntegerField(blank=True, null=True)
    interes = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    pagado = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prestamo'
        unique_together = (('id', 'codigo_usuario'),)


class Proveedor(models.Model):
    id_cliente = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_cliente', blank=True, null=True)
    id_cuenta_cliente = models.IntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    tipo_cuenta = models.IntegerField(blank=True, null=True)
    id_cuenta = models.IntegerField(blank=True, null=True)
    monto = models.FloatField(blank=True, null=True)
    periodo_pago = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proveedor'


class Solicitudprestamo(models.Model):
    codigo_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='codigo_usuario', blank=True, null=True)
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    monto = models.FloatField(blank=True, null=True)
    tiempo = models.IntegerField(blank=True, null=True)
    estado = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'solicitudprestamo'


class Tarjetacredito(models.Model):
    codigo_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='codigo_usuario', blank=True, null=True)
    marca = models.CharField(max_length=50, blank=True, null=True)
    limite = models.FloatField(blank=True, null=True)
    moneda = models.CharField(max_length=1, blank=True, null=True)
    puntos = models.FloatField(blank=True, null=True)
    porcentaje = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tarjetacredito'


class Tarjetadebito(models.Model):
    codigo_usuario = models.IntegerField()
    fondo = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tarjetadebito'
        unique_together = (('id', 'codigo_usuario'),)


class Usuario(models.Model):
    codigoe = models.ForeignKey(Clienteempresarial, models.DO_NOTHING, db_column='codigoE')  # Field name made lowercase.
    codigoi = models.ForeignKey(Clienteindividual, models.DO_NOTHING, db_column='codigoI')  # Field name made lowercase.
    usuario = models.CharField(max_length=150, blank=True, null=True)
    contrasenia = models.CharField(max_length=100, blank=True, null=True)
    tarjetas = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario'
        unique_together = (('id', 'codigoe', 'codigoi'),)
