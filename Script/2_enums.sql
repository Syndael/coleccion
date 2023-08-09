-- --------------------------------------------------------
-- Host:                         192.168.1.55
-- Versión del servidor:         10.3.37-MariaDB - Source distribution
-- SO del servidor:              Linux
-- HeidiSQL Versión:             12.5.0.6677
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Volcando datos para la tabla coleccion.ESTADO: ~14 rows (aproximadamente)
INSERT INTO `ESTADO` (`ID`, `DESCRIPCION`, `TIPO`, `ORDEN`) VALUES
	(1, 'Buscado', 0, NULL),
	(2, 'Cartucho', 0, NULL),
	(3, 'N/A', 0, NULL),
	(4, 'Completo', 0, NULL),
	(5, 'N/A', 1, NULL),
	(6, 'Pedido', 0, NULL),
	(7, 'Precintado', 0, NULL),
	(8, 'Bien', 1, NULL),
	(9, 'Rota', 1, NULL),
	(10, 'Para cambiar', 1, NULL),
	(11, 'Mal', 1, NULL),
	(12, 'Perfecta', 1, NULL),
	(13, 'Jugando', 2, 2),
	(14, 'Pendiente', 2, 1),
	(15, 'Terminado', 2, 4),
	(16, 'Digital', 0, NULL),
	(17, 'Incompleto', 0, NULL),
	(18, 'Parado', 2, 3);

-- Volcando datos para la tabla coleccion.IDIOMA: ~10 rows (aproximadamente)
INSERT INTO `IDIOMA` (`ID`, `DESCRIPCION`, `CORTO`) VALUES
	(4, 'Alemán', 'DE'),
	(7, 'Chino', 'ZH'),
	(10, 'Coreano', 'KO'),
	(1, 'Español', 'ES'),
	(3, 'Francés', 'FR'),
	(2, 'Inglés', 'EN'),
	(5, 'Italiano', 'IT'),
	(6, 'Japonés', 'JP'),
	(9, 'Portugués', 'PT'),
	(8, 'Ruso', 'RU');

-- Volcando datos para la tabla coleccion.PLATAFORMA: ~22 rows (aproximadamente)
INSERT INTO `PLATAFORMA` (`ID`, `NOMBRE`, `CORTO`) VALUES
	(1, '3DS', NULL),
	(2, 'Android', NULL),
	(3, 'Arcade', NULL),
	(4, 'DS', NULL),
	(5, 'Game Cube', 'GC'),
	(6, 'Game Boy', 'GB'),
	(7, 'Game Boy Advance', 'GBA'),
	(8, 'Game Boy Color', 'GBC'),
	(9, 'Nintendo 64', 'N64'),
	(10, 'Otros', NULL),
	(11, 'PC', NULL),
	(12, 'Play Station', 'PS1'),
	(13, 'Play Station 2', 'PS2'),
	(14, 'Play Station Portable', 'PSP'),
	(15, 'Switch', NULL),
	(16, 'Wii', NULL),
	(17, 'Wii U', NULL),
	(18, 'Xbox', NULL),
	(19, 'Xbox 360', NULL),
	(20, 'Xbox One', NULL),
	(21, 'Xbox Series', NULL),
	(22, 'Play Station 3', 'PS3'),
	(23, 'Play Station 4', 'PS4'),
	(24, 'Play Station 5', 'PS5');

-- Volcando datos para la tabla coleccion.REGION: ~2 rows (aproximadamente)
INSERT INTO `REGION` (`ID`, `DESCRIPCION`, `CORTO`) VALUES
	(1, 'América', 'USA'),
	(3, 'Asia', 'AS'),
	(2, 'Europa', 'EU');

-- Volcando datos para la tabla coleccion.TIENDA: ~8 rows (aproximadamente)
INSERT INTO `TIENDA` (`ID`, `NOMBRE`) VALUES
	(1, 'Amazon'),
	(2, 'Amazon JP'),
	(3, 'Carrefour'),
	(4, 'eShop'),
	(5, 'Game'),
	(6, 'Gamemas Santander'),
	(7, 'MediaMarkt'),
	(8, 'Nintendo Store'),
	(9, 'Wakkap'),
	(10, 'Worten'),
	(11, 'Wallapop'),
	(12, 'Steam'),
	(13, 'Miravia'),
	(14, 'Impact Game'),
	(15, 'Vinted'),
	(16, 'Xtralife'),
	(17, 'Abacus Cooperativa');

-- Volcando datos para la tabla coleccion.TIPO_BASE: ~4 rows (aproximadamente)
INSERT INTO `TIPO_BASE` (`ID`, `DESCRIPCION`) VALUES
	(1, 'Juego'),
	(2, 'Consola'),
	(3, 'Mando'),
	(4, 'Otros');

-- Volcando datos para la tabla coleccion.TIPO_FICHERO: ~2 rows (aproximadamente)
INSERT INTO `TIPO_FICHERO` (`ID`, `DESCRIPCION`) VALUES
	(1, 'Foto'),
	(2, 'Factura');

-- Volcando datos para la tabla coleccion.TIPO_ROM: ~11 rows (aproximadamente)
INSERT INTO `TIPO_ROM` (`ID`, `EXTENSION`) VALUES
	(1, '3ds'),
	(2, 'bin'),
	(3, 'chd'),
	(4, 'cso'),
	(5, 'gb'),
	(6, 'gba'),
	(7, 'gbc'),
	(8, 'iso'),
	(9, 'nds'),
	(10, 'nsp'),
	(11, 'xci');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
