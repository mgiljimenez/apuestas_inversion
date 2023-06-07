CREATE DATABASE apuestas;
USE apuestas;

CREATE TABLE casas_apuesta (
    id_casa_apuesta INT AUTO_INCREMENT NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(200),
    url VARCHAR(255) NOT NULL,
    id_cuenta_casa INT NOT NULL,
    id_cuenta_apostado INT NOT NULL,
    PRIMARY KEY (id_casa_apuesta)
);

CREATE TABLE inversores (
    id_inversor INT AUTO_INCREMENT NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    fecha_registro DATE NOT NULL,
    id_cuenta INT NOT NULL,
    PRIMARY KEY (id_inversor)
);

CREATE TABLE cuentas (
    id_cuenta INT AUTO_INCREMENT NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    PRIMARY KEY (id_cuenta)
);

CREATE TABLE movimientos (
    id_movimiento INT AUTO_INCREMENT NOT NULL,
    id_diario INT NOT NULL,
    id_cuenta INT NOT NULL,
    entrada DECIMAL,
    salida DECIMAL,
    PRIMARY KEY (id_movimiento)
);

CREATE TABLE diario (
    id INT AUTO_INCREMENT NOT NULL,
    descripcion VARCHAR(255),
    fecha DATE NOT NULL,
	PRIMARY KEY (id)
);

CREATE TABLE apuestas_individuales (
    id_apuesta INT AUTO_INCREMENT NOT NULL,
    fecha_inversion DATE NOT NULL,
    fecha_hora_evento DATETIME NOT NULL,
    id_deporte INT NOT NULL,
    equipo1 VARCHAR(50) NOT NULL,
    equipo2 VARCHAR(50) NOT NULL,
    id_casa_apuesta_1 INT NOT NULL,
    multiplicador_1 DECIMAL NOT NULL,
    inversion_1 DECIMAL NOT NULL,
	id_casa_apuesta_2 INT NOT NULL,
    multiplicador_2 DECIMAL NOT NULL,
    inversion_2 DECIMAL NOT NULL,
    ganador BOOLEAN,
    rentabilidad DECIMAL,
    beneficio DECIMAL,
    PRIMARY KEY (id_apuesta)
);

CREATE TABLE rentabilidad_diaria (
    id_rentabilida_diaria INT AUTO_INCREMENT NOT NULL,
    fecha DATE NOT NULL,
    rentabilidad INT NOT NULL,
    PRIMARY KEY (id_rentabilida_diaria)
);

CREATE TAapuestas_individualesBLE deportes (
    id_deporte INT AUTO_INCREMENT NOT NULL,
    deporte VARCHAR(50) NOT NULL,
    PRIMARY KEY (id_deporte)
);
