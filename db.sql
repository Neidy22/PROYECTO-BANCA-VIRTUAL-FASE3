drop database django;
create database django;
use django;
create table clienteIndividual(
	codigo int ,
    cui bigint,
    nit int,
    primary key (codigo,cui,nit),
    nombre varchar(100),
    nacimiento date,
    email varchar(150),
    telefono bigint,
	PRIMARY KEY (codigo,cui,nit)
    
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
	tarjetas int ,
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
	id int,
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


CREATE TABLE tarjetacredito (
  id int AUTO_INCREMENT,
  codigo_usuario int ,
  marca varchar(50) ,
  limite float ,
  moneda char(1) ,
  puntos float ,
  porcentaje float ,
  PRIMARY KEY (id),
  FOREIGN KEY (codigo_usuario) REFERENCES usuario (id)
) ;


CREATE TABLE compra (
  id int auto_increment,
  fecha date ,
  descripcion varchar(200) ,
  monto float ,
  codigo_tarjeta int,
  moneda char(1) ,
  puntos float ,
  cashback float ,
  PRIMARY KEY (id),
  FOREIGN KEY (codigo_tarjeta) REFERENCES tarjetacredito (id)
  );
  
CREATE TABLE solicitudprestamo (
  id int  AUTO_INCREMENT,
  codigo_usuario int ,
  descripcion varchar(250) ,
  monto float ,
  tiempo int ,
  estado tinyint ,
  PRIMARY KEY (id),
  FOREIGN KEY (codigo_usuario) REFERENCES usuario (id)
) ;

 CREATE TABLE prestamo (
  id int  AUTO_INCREMENT,
  codigo_usuario int ,
  monto float ,
  modalidad_pago int ,
  interes float ,
  total float ,
  pagado float ,
  PRIMARY KEY (id,codigo_usuario),
  FOREIGN KEY (codigo_usuario) REFERENCES usuario (id)
) ;

CREATE TABLE pagoautomatico (
  id int  AUTO_INCREMENT,
  codigo_usuario int ,
  tipo_cuenta int ,
  id_cuenta int ,
  id_prestamo int ,
  fecha date ,
  cuota float ,
  restante float ,
  PRIMARY KEY (id),
 FOREIGN KEY (codigo_usuario) REFERENCES usuario (id),
 FOREIGN KEY (id_prestamo) REFERENCES prestamo (id)
);

CREATE TABLE pagoadelantado (
  id int  AUTO_INCREMENT,
  codigo_usuario int ,
  tipo_cuenta int ,
  id_cuenta int ,
  id_prestamo int ,
  fecha date ,
  cuota float ,
  restante float ,
  PRIMARY KEY (id),
  FOREIGN KEY (codigo_usuario) REFERENCES usuario (id),
  FOREIGN KEY (id_prestamo) REFERENCES prestamo (id)
);

  
  CREATE TABLE planilla (
  id int  AUTO_INCREMENT,
  id_empresa int ,
  tipo_cuenta tinyint ,
  id_cuenta int ,
  periodo varchar(50) ,
  PRIMARY KEY (id),
 FOREIGN KEY (id_empresa) REFERENCES clienteempresarial (codigo)
  
  );
 










insert into clienteIndividual values(0,0,0,'0','0','1997-03-03','0',0);
insert into clienteEmpresarial values(0,'0','0','0','0','0',0);
insert into usuario values(0,0,0,'admin','admindbs');
insert into cuentaMonetaria values(0,1,0,0,'n',0,0,0);
insert into cuentaAhorro values(0,1,0,0,0,'n',0,0,0);
insert into cuentaFija values(0,1,0,0,0,0,0,0);

INSERT INTO clienteindividual VALUES (0,0,0,'0','1997-03-03','0',0),
(1,12345678910,1234567,'DIEGO FERNANDO CORTEZ LOPEZ','1997-03-03','diego@gmail.com',12345679),
(2,12345678911,1234568,'KARINA NOHEMI RAMIREZ ORELLANA','1994-02-03','nohemi@gmail.com',12345610),
(3,12345678912,1234569,'ANGEL GEOVANNY ARAGON PEREZ','1998-06-08','geovanny@gmail.com',12345611),
(4,12345678913,1234561,'CARLOS ROBERTO QUIXTAN PEREZ','1999-12-11','roberto@gmail.com',12345612),
(5,12345678914,1234511,'ERICK IVAN MAYORGA RODRIGUEZ','1993-08-15','ivan@gmail.com',12345613),
(6,12345678915,1234512,'BYRON ESTUARDO CAAL CATUN','1992-03-12','estuardo@gmail.com',12345614),
(7,12345678916,1234513,'RONALD RODRIGO MARIN SALAS','1991-11-22','rodrigo@gmail.com',12345615),
(8,12345678917,1234514,'OSCAR DANIEL OLIVA','1990-04-08','daniel@gmail.com',12345616),
(9,12345678918,1234515,'EDUARDO ABRAHAM BARILLAS','1989-07-03','abraham@gmail.com',12345617),
(10,12345678919,1234516,'CARLOS ESTUARDO MONTERROSO SANTOS','1995-05-08','estuardo@gmail.com',12345618);

INSERT INTO clienteempresarial VALUES (0,'0','0','0','0','0',0),
(1,'ANONIMA','MAQXA','MAQUINAS EXACTAS S.A','ARMANDO COFIÑO','Km48. Santa Lucía',45879623),
(2,'ANONIMA','PANTALEÓN','INGENIO PANTALEON S.A','RODRIGO LUJÁN','Km32. SIQUINALÁ',78963133),
(3,'ANONIMA','PEPSICO','EMBOTELLADORA MARIPOSA S.A','CARMEN MARQUEZ','Km12. GUATEMALA',75361220);



select * from clienteIndividual;
select * from clienteEmpresarial;
select * from usuario;
select * from cuentaMonetaria;
select*from cuentaAhorro;
select * from cuentaFija;
select * from chequera;
select * from deposito;

