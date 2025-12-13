-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 11-12-2025 a las 06:15:07
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `controllabs`
--

DELIMITER $$
--
-- Procedimientos
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_resolver_incidente` (IN `p_id_incidente` INT)   BEGIN
    
    UPDATE incidentes 
    SET observaciones = 1 
    WHERE id_incidente = p_id_incidente;
    
    
    SELECT CONCAT('El incidente ', p_id_incidente, ' ha sido marcado como resuelto.') AS Mensaje;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `incidentes`
--

CREATE TABLE `incidentes` (
  `id_incidente` int(11) NOT NULL,
  `fecha` datetime DEFAULT current_timestamp(),
  `id_usuario` int(11) NOT NULL,
  `incidente` text NOT NULL,
  `id_laboratorio` int(11) NOT NULL,
  `observaciones` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `incidentes`
--

INSERT INTO `incidentes` (`id_incidente`, `fecha`, `id_usuario`, `incidente`, `id_laboratorio`, `observaciones`) VALUES
(14, '2025-12-10 20:07:11', 11, 'La computadora 6 no tiene acceso a internet aún teniendo el cable conectado\n', 3, 1),
(15, '2025-12-10 23:00:36', 11, 'Nos sirve\n', 3, 0),
(16, '2025-12-10 23:00:47', 11, 'No prenden las compus', 5, 0);

--
-- Disparadores `incidentes`
--
DELIMITER $$
CREATE TRIGGER `tr_auditoria_borrado` BEFORE DELETE ON `incidentes` FOR EACH ROW BEGIN
    INSERT INTO papelera_incidentes (id_original, descripcion_borrada)
    VALUES (OLD.id_incidente, OLD.incidente);
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `laboratorios`
--

CREATE TABLE `laboratorios` (
  `id_lab` int(11) NOT NULL,
  `nombre` varchar(23) NOT NULL,
  `edificio` varchar(7) DEFAULT NULL,
  `piso` tinyint(3) DEFAULT NULL,
  `cant_pc` tinyint(3) DEFAULT NULL,
  `estatus` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `laboratorios`
--

INSERT INTO `laboratorios` (`id_lab`, `nombre`, `edificio`, `piso`, `cant_pc`, `estatus`) VALUES
(1, 'laboratorioinformatico1', 'c', 1, 25, 1),
(2, 'laboratorioinformatico2', 'c', 2, 25, 0),
(3, 'idiomas', 'c', 1, 15, 1),
(4, 'laboratorioinformatico1', 'A', 1, 20, 1),
(5, 'laboratorioInformatico2', 'A', 1, 20, 1),
(6, 'LenguageLab', 'C', 1, 20, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `papelera_incidentes`
--

CREATE TABLE `papelera_incidentes` (
  `id_historial` int(11) NOT NULL,
  `id_original` int(11) DEFAULT NULL,
  `descripcion_borrada` text DEFAULT NULL,
  `fecha_borrado` datetime DEFAULT current_timestamp(),
  `usuario_responsable` varchar(50) DEFAULT 'Admin'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `papelera_incidentes`
--

INSERT INTO `papelera_incidentes` (`id_historial`, `id_original`, `descripcion_borrada`, `fecha_borrado`, `usuario_responsable`) VALUES
(1, 13, 'No sirven las computadoras 4, 8, 9 y 15', '2025-12-10 22:44:15', 'Admin');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `primer_nombre` varchar(50) NOT NULL,
  `segundo_nombre` varchar(50) DEFAULT NULL,
  `apellido_paterno` varchar(50) NOT NULL,
  `telefono` varchar(10) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `contrasena` varchar(255) NOT NULL,
  `rol` enum('admin','usuario') NOT NULL DEFAULT 'usuario',
  `estatus` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `primer_nombre`, `segundo_nombre`, `apellido_paterno`, `telefono`, `email`, `contrasena`, `rol`, `estatus`) VALUES
(10, 'Víctor', 'Admin', 'Rivera', '6180000000', 'victoriano.rivera@utd.edu.mx', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin', 1),
(11, 'Paulina', 'Ale', 'Breceda', '6182933260', 'pau@utd.edu.mx', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'usuario', 1);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `vista_incidentes`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `vista_incidentes` (
`id_incidente` int(11)
,`fecha` datetime
,`descripcion` text
,`nombre_laboratorio` varchar(23)
,`edificio` varchar(7)
,`estado` tinyint(1)
,`id_usuario` int(11)
,`nombre_completo` varchar(101)
);

-- --------------------------------------------------------

--
-- Estructura para la vista `vista_incidentes`
--
DROP TABLE IF EXISTS `vista_incidentes`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vista_incidentes`  AS SELECT `i`.`id_incidente` AS `id_incidente`, `i`.`fecha` AS `fecha`, `i`.`incidente` AS `descripcion`, `l`.`nombre` AS `nombre_laboratorio`, `l`.`edificio` AS `edificio`, `i`.`observaciones` AS `estado`, `u`.`id_usuario` AS `id_usuario`, concat(`u`.`primer_nombre`,' ',`u`.`apellido_paterno`) AS `nombre_completo` FROM ((`incidentes` `i` join `laboratorios` `l` on(`i`.`id_laboratorio` = `l`.`id_lab`)) join `usuarios` `u` on(`i`.`id_usuario` = `u`.`id_usuario`)) ;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `incidentes`
--
ALTER TABLE `incidentes`
  ADD PRIMARY KEY (`id_incidente`),
  ADD KEY `fk_incidente_usuario` (`id_usuario`),
  ADD KEY `fk_incidente_laboratorio` (`id_laboratorio`);

--
-- Indices de la tabla `laboratorios`
--
ALTER TABLE `laboratorios`
  ADD PRIMARY KEY (`id_lab`);

--
-- Indices de la tabla `papelera_incidentes`
--
ALTER TABLE `papelera_incidentes`
  ADD PRIMARY KEY (`id_historial`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `incidentes`
--
ALTER TABLE `incidentes`
  MODIFY `id_incidente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `laboratorios`
--
ALTER TABLE `laboratorios`
  MODIFY `id_lab` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `papelera_incidentes`
--
ALTER TABLE `papelera_incidentes`
  MODIFY `id_historial` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `incidentes`
--
ALTER TABLE `incidentes`
  ADD CONSTRAINT `fk_incidente_laboratorio` FOREIGN KEY (`id_laboratorio`) REFERENCES `laboratorios` (`id_lab`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_incidente_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
