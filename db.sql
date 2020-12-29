drop database django;
create database django;
use django;
create table clienteIndividual(
	codigo int ,
    cui bigint,
    nit int,
    primary key (codigo,cui,nit),
    primer_nombre varchar(100),
    primer_apellido varchar(100),
    nacimiento date,
    email varchar(150),
    telefono bigint
);

create table clienteEmpresarial(
	codigo int,
    tipo varchar(50),
    nombre_comercial varchar(100),
    nombre_empresa varchar(100),
    nombre_representante varchar(150),
    direccion varchar(300),
    telefono int,
    primary key (codigo,tipo,nombre_comercial,nombre_empresa)
);

create table usuario(
	id int auto_increment ,
	codigoE int,
    codigoI int,
	usuario varchar(150),
	contrasenia varchar(100),
    primary key(id,codigoE, codigoI),
	foreign key(codigoI) references clienteIndividual(codigo),
    foreign key(codigoE) references clienteEmpresarial(codigo)

);

create table cuentaAhorro(
	id int auto_increment,
    codigo_usuario int,
    fondo float,
    tasa_interes float,
    promocion float,
    moneda char,
    estado tinyint,
    pre_auto tinyint,
    cheques_disponibles int,
    primary key (id, codigo_usuario),
    foreign key(codigo_usuario) references usuario(id)
);

create table cuentaMonetaria(
	id int auto_increment,
	codigo_usuario int,
    fondo float,
    monto_manejo float,
    moneda char,
    estado tinyint,
    pre_auto tinyint,
    cheques_disponibles int,
    primary key (id, codigo_usuario),
    foreign key(codigo_usuario) references usuario(id)
   
);

create table cuentaFija(
	id int auto_increment,
	codigo_usuario int,
    cuota float,
    capitalizacion int,
    tasa_interes float,
    fondo_total float,
    moneda char,
    estado tinyint,
	primary key (id, codigo_usuario),
    foreign key(codigo_usuario) references usuario(id)

);

create table prestamo(
	id int auto_increment,
	codigo_usuario int,
    monto float,
    modalidad_pago int,
    interes float,
	primary key (id, codigo_usuario),
    foreign key(codigo_usuario) references usuario(id)
);

create table chequera(
	id int auto_increment ,
    codigo_monetaria int,
    codigo_ahorro int,
    fecha_emision date,
    cheques_disponibles tinyint,
	primary key (id, codigo_monetaria,codigo_ahorro),
    foreign key(codigo_monetaria) references cuentaMonetaria(id),
    foreign key(codigo_ahorro) references cuentaAhorro(id)
);

create table cheque(
	id int auto_increment ,
    codigo_chequera int,
    fecha_emision date,
    nombre_portador varchar(100),
    monto float,
    autorizado tinyint,
    cobrado tinyint,
	primary key (id, codigo_chequera),
    foreign key(codigo_chequera) references Chequera(id)
    
    
);

create table tarjetaDebito(
	id int auto_increment,
    codigo_usuario int,
    fondo float,
    primary key(id,codigo_usuario)
);

create table deposito(
	id int auto_increment,
    depositante int,
    receptor int,
    tipo_receptor int,
    monto float,
    moneda char,
    primary key (id)
);



insert into clienteIndividual values(0,0,0,'0','0','1997-03-03','0',0);
insert into clienteEmpresarial values(0,'0','0','0','0','0',0);
insert into usuario values(0,0,0,'admin','admindbs');
insert into cuentaMonetaria values(0,1,0,0,'n',0,0,0);
insert into cuentaAhorro values(0,1,0,0,0,'n',0,0,0);
insert into cuentaFija values(0,1,0,0,0,0,0,0);




select * from clienteIndividual;
select * from clienteEmpresarial;
select * from usuario;
select * from cuentaMonetaria;
select*from cuentaAhorro;
select * from cuentaFija;
select * from chequera;
select * from deposito;

