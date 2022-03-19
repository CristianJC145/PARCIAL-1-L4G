/*
SQLyog Ultimate v13.1.1 (64 bit)
MySQL - 10.4.22-MariaDB : Database - carta_virtual
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`carta_virtual` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `carta_virtual`;

/*Table structure for table `consumidor` */

DROP TABLE IF EXISTS `consumidor`;

CREATE TABLE `consumidor` (
  `id_consumidor` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_consumidor` varchar(100) NOT NULL,
  `direccion` varchar(50) NOT NULL,
  `celular` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`id_consumidor`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8;

/*Data for the table `consumidor` */

/*Table structure for table `consumidor_empresa` */

DROP TABLE IF EXISTS `consumidor_empresa`;

CREATE TABLE `consumidor_empresa` (
  `id_empresa` int(11) NOT NULL,
  `id_consumidor` int(11) NOT NULL,
  KEY `id_empresa` (`id_empresa`),
  KEY `id_consumidor` (`id_consumidor`),
  CONSTRAINT `consumidor_empresa_ibfk_1` FOREIGN KEY (`id_empresa`) REFERENCES `empresa` (`id_empresa`),
  CONSTRAINT `consumidor_empresa_ibfk_2` FOREIGN KEY (`id_consumidor`) REFERENCES `consumidor` (`id_consumidor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `consumidor_empresa` */

/*Table structure for table `empresa` */

DROP TABLE IF EXISTS `empresa`;

CREATE TABLE `empresa` (
  `id_empresa` int(11) NOT NULL AUTO_INCREMENT,
  `imagen` varchar(300) DEFAULT NULL,
  `nombre_empresa` varchar(30) NOT NULL,
  `contacto` varchar(15) NOT NULL,
  `direccion` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `contraseña` varchar(50) NOT NULL,
  `descripcion` text DEFAULT NULL,
  PRIMARY KEY (`id_empresa`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

/*Data for the table `empresa` */

/*Table structure for table `pedido` */

DROP TABLE IF EXISTS `pedido`;

CREATE TABLE `pedido` (
  `id_pedido` int(11) NOT NULL AUTO_INCREMENT,
  `id_empresa` int(11) NOT NULL,
  `id_consumidor` int(11) NOT NULL,
  PRIMARY KEY (`id_pedido`),
  KEY `id_consumidor` (`id_consumidor`),
  CONSTRAINT `pedido_ibfk_2` FOREIGN KEY (`id_consumidor`) REFERENCES `consumidor` (`id_consumidor`)
) ENGINE=InnoDB AUTO_INCREMENT=401 DEFAULT CHARSET=utf8;

/*Data for the table `pedido` */

/*Table structure for table `pedido_producto` */

DROP TABLE IF EXISTS `pedido_producto`;

CREATE TABLE `pedido_producto` (
  `id_producto` int(11) NOT NULL,
  `id_pedido` int(11) NOT NULL,
  `cantidad` varchar(10) NOT NULL,
  `pago` double NOT NULL,
  KEY `id_pedido` (`id_pedido`),
  KEY `id_producto` (`id_producto`),
  CONSTRAINT `pedido_producto_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedido` (`id_pedido`),
  CONSTRAINT `pedido_producto_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `pedido_producto` */

/*Table structure for table `producto` */

DROP TABLE IF EXISTS `producto`;

CREATE TABLE `producto` (
  `id_producto` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_producto` varchar(50) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `precio` varchar(10) NOT NULL,
  `estado` varchar(10) NOT NULL,
  PRIMARY KEY (`id_producto`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

/*Data for the table `producto` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
