CREATE TABLE `JUEGO` (
	`ID` INT(11) NOT NULL AUTO_INCREMENT,
	`NOMBRE` VARCHAR(255) NOT NULL COLLATE 'utf8_general_ci',
	`FECHA_SALIDA` DATE NULL DEFAULT NULL,
	PRIMARY KEY (`ID`) USING BTREE,
	UNIQUE INDEX `NOMBRE_SALIDA_JUEGO_UK` (`NOMBRE`, `FECHA_SALIDA`) USING BTREE
);

CREATE TABLE `PLATAFORMA` (
	`ID` INT(11) NOT NULL AUTO_INCREMENT,
	`NOMBRE` VARCHAR(255) NOT NULL COLLATE 'utf8_general_ci',
	`CORTO` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`ID`) USING BTREE,
	UNIQUE INDEX `NOMBRE_PLAT_UK` (`NOMBRE`) USING BTREE
);

CREATE TABLE `JUEGO_X_PLATAFORMA` (
	`JUEGO_ID` INT(11) NOT NULL,
	`PLATAFORMA_ID` INT(11) NOT NULL,
	PRIMARY KEY (`JUEGO_ID`, `PLATAFORMA_ID`) USING BTREE,
	INDEX `PLAT_ID_JXP_FK` (`PLATAFORMA_ID`) USING BTREE,
	CONSTRAINT `JUEGO_ID_JXP_FK` FOREIGN KEY (`JUEGO_ID`) REFERENCES `JUEGO` (`ID`) ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT `PLAT_ID_JXP_FK` FOREIGN KEY (`PLATAFORMA_ID`) REFERENCES `PLATAFORMA` (`ID`) ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE `IDIOMA` (
	`ID` INT(11) NOT NULL AUTO_INCREMENT,
	`DESCRIPCION` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
	`CORTO` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`ID`) USING BTREE,
	UNIQUE INDEX `DESC_CORTO_I_UK` (`DESCRIPCION`, `CORTO`) USING BTREE
);

CREATE TABLE `JUGADO` (
	`ID` INT(11) NOT NULL AUTO_INCREMENT,
	`JUEGO_ID` INT(11) NOT NULL,
	`PLATAFORMA_ID` INT(11) NULL DEFAULT NULL,
	`ESTADO_JUGADO_ID` INT(11) NOT NULL,
	`PORCENTAJE` INT(11) NULL DEFAULT NULL,
	`HORAS` DECIMAL(20,6) NULL DEFAULT NULL,
	`HISTORIA_COMPLETA` BIT(1) NULL DEFAULT NULL,
	`NOTAS` VARCHAR(500) NULL DEFAULT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`ID`) USING BTREE,
	INDEX `JUEGO_ID_J_FK` (`JUEGO_ID`) USING BTREE,
	INDEX `PLAT_ID_J_FK` (`PLATAFORMA_ID`) USING BTREE,
	INDEX `ESTADO_J_FK` (`ESTADO_JUGADO_ID`) USING BTREE,
	CONSTRAINT `ESTADO_J_FK` FOREIGN KEY (`ESTADO_JUGADO_ID`) REFERENCES `ESTADO` (`ID`) ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT `JUEGO_ID_J_FK` FOREIGN KEY (`JUEGO_ID`) REFERENCES `JUEGO` (`ID`) ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT `PLAT_ID_J_FK` FOREIGN KEY (`PLATAFORMA_ID`) REFERENCES `PLATAFORMA` (`ID`) ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE `TIENDA` (
	`ID` INT(11) NOT NULL AUTO_INCREMENT,
	`NOMBRE` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`ID`) USING BTREE
);

CREATE TABLE `TIPO_ROM` (
	`ID` INT(11) NOT NULL AUTO_INCREMENT,
	`EXTENSION` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`ID`) USING BTREE
);

CREATE TABLE `REGION` (
	`ID` INT(11) NOT NULL AUTO_INCREMENT,
	`DESCRIPCION` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
	`CORTO` VARCHAR(50) NOT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`ID`) USING BTREE,
	UNIQUE INDEX `DESC_CORTO_R_UK` (`DESCRIPCION`, `CORTO`) USING BTREE
);

CREATE TABLE `ROMS` (
	`ID` INT(11) NOT NULL AUTO_INCREMENT,
	`JUEGO_ID` INT(11) NOT NULL,
	`PLATAFORMA_ID` INT(11) NULL DEFAULT NULL,
	`NOMBRE_ROM` VARCHAR(255) NOT NULL COLLATE 'utf8_general_ci',
	`IDIOMA_ID` INT(11) NULL DEFAULT NULL,
	`REGION_ID` INT(11) NULL DEFAULT NULL,
	`TIPO_ROM_ID` INT(11) NULL DEFAULT NULL,
	PRIMARY KEY (`ID`) USING BTREE,
	INDEX `JUEGO_ID_R_FK` (`JUEGO_ID`) USING BTREE,
	INDEX `PLAT_ID_R_FK` (`PLATAFORMA_ID`) USING BTREE,
	INDEX `IDIOMA_ID_R_FK` (`IDIOMA_ID`) USING BTREE,
	INDEX `REGION_ID_R_FK` (`REGION_ID`) USING BTREE,
	INDEX `TIPO_ROM_ID_R_FK` (`TIPO_ROM_ID`) USING BTREE,
	CONSTRAINT `IDIOMA_ID_R_FK` FOREIGN KEY (`IDIOMA_ID`) REFERENCES `IDIOMA` (`ID`) ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT `JUEGO_ID_R_FK` FOREIGN KEY (`JUEGO_ID`) REFERENCES `JUEGO` (`ID`) ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT `PLAT_ID_R_FK` FOREIGN KEY (`PLATAFORMA_ID`) REFERENCES `PLATAFORMA` (`ID`) ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT `REGION_ID_R_FK` FOREIGN KEY (`REGION_ID`) REFERENCES `REGION` (`ID`) ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT `TIPO_ROM_ID_R_FK` FOREIGN KEY (`TIPO_ROM_ID`) REFERENCES `TIPO_ROM` (`ID`) ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE `COLECCION` (
	`ID` INT(11) NOT NULL AUTO_INCREMENT,
	`JUEGO_ID` INT(11) NULL DEFAULT NULL,
	`PLATAFORMA_ID` INT(11) NULL DEFAULT NULL,
	`IDIOMA_ID` INT(11) NOT NULL,
	`REGION_ID` INT(11) NOT NULL,
	`ESTADO_GENERAL_ID` INT(11) NULL DEFAULT NULL,
	`ESTADO_CAJA_ID` INT(11) NULL DEFAULT NULL,
	`FECHA_COMPRA` DATE NOT NULL,
	`FECHA_RECIBO` DATE NOT NULL,
	`COSTE` DECIMAL(20,6) NOT NULL,
	`TIENDA_ID` INT(11) NOT NULL,
	`NOTAS` VARCHAR(500) NOT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`ID`) USING BTREE,
	INDEX `JUEGO_ID_C_FK` (`JUEGO_ID`) USING BTREE,
	INDEX `PLATAFORMA_ID_C_FK` (`PLATAFORMA_ID`) USING BTREE,
	INDEX `IDIOMA_ID_C_FK` (`IDIOMA_ID`) USING BTREE,
	INDEX `REGION_ID_C_FK` (`REGION_ID`) USING BTREE,
	INDEX `ESTADO_GEN_ID_C_FK` (`ESTADO_GENERAL_ID`) USING BTREE,
	INDEX `TIENDA_ID_C_FK` (`TIENDA_ID`) USING BTREE,
	INDEX `ESTADO_CAJ_ID_C_FK` (`ESTADO_CAJA_ID`) USING BTREE,
	CONSTRAINT `ESTADO_CAJ_ID_C_FK` FOREIGN KEY (`ESTADO_CAJA_ID`) REFERENCES `ESTADO` (`ID`) ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT `ESTADO_GEN_ID_C_FK` FOREIGN KEY (`ESTADO_GENERAL_ID`) REFERENCES `ESTADO` (`ID`) ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT `IDIOMA_ID_C_FK` FOREIGN KEY (`IDIOMA_ID`) REFERENCES `IDIOMA` (`ID`) ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT `JUEGO_ID_C_FK` FOREIGN KEY (`JUEGO_ID`) REFERENCES `JUEGO` (`ID`) ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT `PLATAFORMA_ID_C_FK` FOREIGN KEY (`PLATAFORMA_ID`) REFERENCES `PLATAFORMA` (`ID`) ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT `REGION_ID_C_FK` FOREIGN KEY (`REGION_ID`) REFERENCES `REGION` (`ID`) ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT `TIENDA_ID_C_FK` FOREIGN KEY (`TIENDA_ID`) REFERENCES `TIENDA` (`ID`) ON UPDATE NO ACTION ON DELETE NO ACTION
);

INSERT INTO IDIOMA (DESCRIPCION, CORTO) VALUES ('Español', 'ES');
INSERT INTO IDIOMA (DESCRIPCION, CORTO) VALUES ('Inglés', 'EN');
INSERT INTO IDIOMA (DESCRIPCION, CORTO) VALUES ('Francés', 'FR');
INSERT INTO IDIOMA (DESCRIPCION, CORTO) VALUES ('Alemán', 'DE');
INSERT INTO IDIOMA (DESCRIPCION, CORTO) VALUES ('Italiano', 'IT');
INSERT INTO IDIOMA (DESCRIPCION, CORTO) VALUES ('Japonés', 'JP');
INSERT INTO IDIOMA (DESCRIPCION, CORTO) VALUES ('Chino', 'ZH');
INSERT INTO IDIOMA (DESCRIPCION, CORTO) VALUES ('Ruso', 'RU');
INSERT INTO IDIOMA (DESCRIPCION, CORTO) VALUES ('Portugués', 'PT');
INSERT INTO IDIOMA (DESCRIPCION, CORTO) VALUES ('Coreano', 'KO');

INSERT INTO TIPO_ROM (EXTENSION) VALUES ('3ds');
INSERT INTO TIPO_ROM (EXTENSION) VALUES ('bin');
INSERT INTO TIPO_ROM (EXTENSION) VALUES ('chd');
INSERT INTO TIPO_ROM (EXTENSION) VALUES ('cso');
INSERT INTO TIPO_ROM (EXTENSION) VALUES ('gb');
INSERT INTO TIPO_ROM (EXTENSION) VALUES ('gba');
INSERT INTO TIPO_ROM (EXTENSION) VALUES ('gbc');
INSERT INTO TIPO_ROM (EXTENSION) VALUES ('iso');
INSERT INTO TIPO_ROM (EXTENSION) VALUES ('nds');
INSERT INTO TIPO_ROM (EXTENSION) VALUES ('nsp');
INSERT INTO TIPO_ROM (EXTENSION) VALUES ('xci');

INSERT INTO TIENDA	(NOMBRE) VALUES ('Amazon');
INSERT INTO TIENDA	(NOMBRE) VALUES ('Amazon JP');
INSERT INTO TIENDA	(NOMBRE) VALUES ('Carrefour');
INSERT INTO TIENDA	(NOMBRE) VALUES ('eShop');
INSERT INTO TIENDA	(NOMBRE) VALUES ('Game');
INSERT INTO TIENDA	(NOMBRE) VALUES ('Gamemas Santander');
INSERT INTO TIENDA	(NOMBRE) VALUES ('MediaMarkt');
INSERT INTO TIENDA	(NOMBRE) VALUES ('Nintendo Store');
INSERT INTO TIENDA	(NOMBRE) VALUES ('Wakkap');
INSERT INTO TIENDA	(NOMBRE) VALUES ('Worten');
INSERT INTO TIENDA	(NOMBRE) VALUES ('Wallapop');

INSERT INTO PLATAFORMA	(NOMBRE, CORTO) VALUES ('3DS', NULL);
INSERT INTO PLATAFORMA	(NOMBRE, CORTO) VALUES ('Android', NULL);
INSERT INTO PLATAFORMA	(NOMBRE, CORTO) VALUES ('Arcade', NULL);
INSERT INTO PLATAFORMA	(NOMBRE, CORTO) VALUES ('DS', NULL);
INSERT INTO PLATAFORMA	(NOMBRE, CORTO) VALUES ('Game Boy', 'GB');
INSERT INTO PLATAFORMA	(NOMBRE, CORTO) VALUES ('Game Boy Advance', 'GBA');
INSERT INTO PLATAFORMA	(NOMBRE, CORTO) VALUES ('Game Boy Color', 'GBC');
INSERT INTO PLATAFORMA	(NOMBRE, CORTO) VALUES ('Game Cube', 'GC');
INSERT INTO PLATAFORMA	(NOMBRE, CORTO) VALUES ('Nintendo 64', 'N64');
INSERT INTO PLATAFORMA	(NOMBRE, CORTO) VALUES ('Otros', NULL);
INSERT INTO PLATAFORMA	(NOMBRE, CORTO) VALUES ('PC', NULL);
INSERT INTO PLATAFORMA	(NOMBRE, CORTO) VALUES ('Play Station', 'PS1');
INSERT INTO PLATAFORMA	(NOMBRE, CORTO) VALUES ('Play Station 2', 'PS2');
INSERT INTO PLATAFORMA	(NOMBRE, CORTO) VALUES ('Play Station 3', 'PS3');
INSERT INTO PLATAFORMA	(NOMBRE, CORTO) VALUES ('Play Station 4', 'PS4');
INSERT INTO PLATAFORMA	(NOMBRE, CORTO) VALUES ('Play Station 5', 'PS5');
INSERT INTO PLATAFORMA	(NOMBRE, CORTO) VALUES ('Play Station Portable', 'PSP');
INSERT INTO PLATAFORMA	(NOMBRE, CORTO) VALUES ('Switch', NULL);
INSERT INTO PLATAFORMA	(NOMBRE, CORTO) VALUES ('Wii', NULL);
INSERT INTO PLATAFORMA	(NOMBRE, CORTO) VALUES ('Wii U', NULL);
INSERT INTO PLATAFORMA	(NOMBRE, CORTO) VALUES ('Xbox', NULL);
INSERT INTO PLATAFORMA	(NOMBRE, CORTO) VALUES ('Xbox 360', NULL);
INSERT INTO PLATAFORMA	(NOMBRE, CORTO) VALUES ('Xbox One', NULL);
INSERT INTO PLATAFORMA	(NOMBRE, CORTO) VALUES ('Xbox Series', NULL);

INSERT INTO ESTADO	(DESCRIPCION, TIPO) VALUES ('Buscado', 0);
INSERT INTO ESTADO	(DESCRIPCION, TIPO) VALUES ('Cartucho', 0);
INSERT INTO ESTADO	(DESCRIPCION, TIPO) VALUES ('N/A', 0);
INSERT INTO ESTADO	(DESCRIPCION, TIPO) VALUES ('Completo', 0);
INSERT INTO ESTADO	(DESCRIPCION, TIPO) VALUES ('N/A', 1);
INSERT INTO ESTADO	(DESCRIPCION, TIPO) VALUES ('Pedido', 0);
INSERT INTO ESTADO	(DESCRIPCION, TIPO) VALUES ('Precintado', 0);
INSERT INTO ESTADO	(DESCRIPCION, TIPO) VALUES ('Bien', 1);
INSERT INTO ESTADO	(DESCRIPCION, TIPO) VALUES ('Rota', 1);
INSERT INTO ESTADO	(DESCRIPCION, TIPO) VALUES ('Para cambiar', 1);
INSERT INTO ESTADO	(DESCRIPCION, TIPO) VALUES ('Mal', 1);
INSERT INTO ESTADO	(DESCRIPCION, TIPO) VALUES ('Perfecta', 1);
INSERT INTO ESTADO	(DESCRIPCION, TIPO) VALUES ('Jugando', 2);
INSERT INTO ESTADO	(DESCRIPCION, TIPO) VALUES ('Pendiente', 2);
INSERT INTO ESTADO	(DESCRIPCION, TIPO) VALUES ('Terminado', 2);
INSERT INTO ESTADO	(DESCRIPCION, TIPO) VALUES ('Digital', 0);
INSERT INTO ESTADO	(DESCRIPCION, TIPO) VALUES ('Incompleto', 0);

INSERT INTO REGION (DESCRIPCION, CORTO) VALUES ('América', 'USA');
INSERT INTO REGION (DESCRIPCION, CORTO) VALUES ('Europa', 'EU');
INSERT INTO REGION (DESCRIPCION, CORTO) VALUES ('Asia', 'AS');

