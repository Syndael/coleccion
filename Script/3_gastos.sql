SELECT
	ROW_NUMBER() OVER () AS ID,
	TIPO,
	PLATAFORMA_NOMBRE,
	PLATAFORMA_CORTO,
	DESCRIPCION,
	CANTIDAD,
	FISICO,
	DIGITAL,
	COSTE,
	ORDEN_DESC,
	ORDEN_ASC
FROM (
	(
		SELECT
			'JUEGOS_MES' TIPO,
			NULL PLATAFORMA_NOMBRE,
			NULL PLATAFORMA_CORTO,
			concat(
				case
					when month(c.FECHA_COMPRA) = 1 then 'Enero'
					when month(c.FECHA_COMPRA) = 2 then 'Febrero'
					when month(c.FECHA_COMPRA) = 3 then 'Marzo'
					when month(c.FECHA_COMPRA) = 4 then 'Abril'
					when month(c.FECHA_COMPRA) = 5 then 'Mayo'
					when month(c.FECHA_COMPRA) = 6 then 'Junio'
					when month(c.FECHA_COMPRA) = 7 then 'Julio'
					when month(c.FECHA_COMPRA) = 8 then 'Agosto'
					when month(c.FECHA_COMPRA) = 9 then 'Septiembre'
					when month(c.FECHA_COMPRA) = 10 then 'Octubre'
					when month(c.FECHA_COMPRA) = 11 then 'Noviembre'
					when month(c.FECHA_COMPRA) = 12 then 'Diciembre'
				end,
				' ', year(c.FECHA_COMPRA)
			) AS DESCRIPCION,
			COUNT(*) CANTIDAD,
			SUM(
				IF(
					e.DESCRIPCION IN (
						'Cartucho', 'Completo', 'Disco', 'Incompleto', 'Precintado', 'Prestado', 'UMD'
					), 1, 0
				)
			) FISICO,
			SUM(
				IF(
					e.DESCRIPCION IN (
						'CIAB', 'Digital'
					), 1, 0
				)
			)  DIGITAL,
			SUM(c.COSTE) COSTE,
			DATE_FORMAT(c.FECHA_COMPRA, '%Y%m') ORDEN_DESC,
			NULL ORDEN_ASC
		FROM COLECCION c
		INNER JOIN PLATAFORMA p ON p.ID = c.PLATAFORMA_ID
		INNER JOIN ESTADO e ON e.ID = c.ESTADO_GENERAL_ID
			AND e.TIPO = 0
			AND e.DESCRIPCION IN (
				'Cartucho', 'Completo', 'Disco', 'Incompleto', 'Precintado', 'Prestado', 'UMD',
				'CIAB', 'Digital'
			)
		INNER JOIN BASE b ON b.ID = c.BASE_ID
		INNER JOIN TIPO_BASE tb ON tb.ID = b.TIPO_ID
			AND tb.DESCRIPCION = 'Juego'
		GROUP BY MONTH(c.FECHA_COMPRA), YEAR(c.FECHA_COMPRA)
	) UNION (
		SELECT
			'JUEGOS_PLATAFORMA' TIPO,
			p.NOMBRE PLATAFORMA_NOMBRE,
			p.CORTO PLATAFORMA_CORTO,
			NULL DESCRIPCION,
			COUNT(*) CANTIDAD,
			SUM(
				IF(e.DESCRIPCION = 'Digital', 0, 1)
			) FISICO,
			SUM(
				IF(e.DESCRIPCION = 'Digital', 1, 0)
			) DIGITAL,
			SUM(c.COSTE) COSTE,
			NULL ORDEN_DESC,
			UPPER(p.NOMBRE) ORDEN_ASC
		FROM COLECCION c
		INNER JOIN PLATAFORMA p ON p.ID = c.PLATAFORMA_ID
		INNER JOIN ESTADO e ON e.ID = c.ESTADO_GENERAL_ID
			AND e.TIPO = 0
			AND e.DESCRIPCION NOT IN ('Buscado', 'N/A', 'Reservado', 'Pedido')
		INNER JOIN BASE b ON b.ID = c.BASE_ID
		INNER JOIN TIPO_BASE tb ON tb.ID = b.TIPO_ID
			AND tb.DESCRIPCION = 'Juego'
		GROUP BY PLATAFORMA_ID
	) UNION (
		SELECT
			'TOTAL' TIPO,
			NULL PLATAFORMA_NOMBRE,
			NULL PLATAFORMA_CORTO,
			'Juego' DESCRIPCION,
			COUNT(*) CANTIDAD,
			SUM(
				IF(e.DESCRIPCION = 'Digital', 0, 1)
			) FISICO,
			SUM(
				IF(e.DESCRIPCION = 'Digital', 1, 0)
			) DIGITAL,
			SUM(c.COSTE) COSTE,
			NULL ORDEN_DESC,
			NULL ORDEN_ASC
		FROM COLECCION c
		INNER JOIN PLATAFORMA p ON p.ID = c.PLATAFORMA_ID
		INNER JOIN ESTADO e ON e.ID = c.ESTADO_GENERAL_ID
			AND e.TIPO = 0
			AND e.DESCRIPCION NOT IN ('Buscado', 'N/A', 'Reservado', 'Pedido')
		INNER JOIN BASE b ON b.ID = c.BASE_ID
		INNER JOIN TIPO_BASE tb ON tb.ID = b.TIPO_ID
			AND tb.DESCRIPCION = 'Juego'
	) UNION (
		SELECT
			'TOTAL' TIPO,
			NULL PLATAFORMA_NOMBRE,
			NULL PLATAFORMA_CORTO,
			'Consola' DESCRIPCION,
			COUNT(*) CANTIDAD,
			SUM(
				IF(e.DESCRIPCION = 'Digital', 0, 1)
			) FISICO,
			SUM(
				IF(e.DESCRIPCION = 'Digital', 1, 0)
			) DIGITAL,
			SUM(c.COSTE) COSTE,
			NULL ORDEN_DESC,
			NULL ORDEN_ASC
		FROM COLECCION c
		INNER JOIN PLATAFORMA p ON p.ID = c.PLATAFORMA_ID
		INNER JOIN ESTADO e ON e.ID = c.ESTADO_GENERAL_ID
			AND e.TIPO = 0
			AND e.DESCRIPCION NOT IN ('Buscado', 'N/A', 'Reservado', 'Pedido')
		INNER JOIN BASE b ON b.ID = c.BASE_ID
		INNER JOIN TIPO_BASE tb ON tb.ID = b.TIPO_ID
			AND tb.DESCRIPCION = 'Consola'
	) UNION (
		SELECT
			'TOTAL' TIPO,
			NULL PLATAFORMA_NOMBRE,
			NULL PLATAFORMA_CORTO,
			'Envíos' DESCRIPCION,
			COUNT(*) CANTIDAD,
			SUM(
				IF(e.DESCRIPCION = 'Digital', 0, 1)
			) FISICO,
			SUM(
				IF(e.DESCRIPCION = 'Digital', 1, 0)
			) DIGITAL,
			SUM(c.ENVIO) COSTE,
			NULL ORDEN_DESC,
			NULL ORDEN_ASC
		FROM COLECCION c
		INNER JOIN ESTADO e ON e.ID = c.ESTADO_GENERAL_ID
			AND e.TIPO = 0
			AND e.DESCRIPCION NOT IN ('Buscado', 'N/A', 'Reservado', 'Pedido')
		WHERE c.ENVIO IS NOT NULL
	) UNION (
		SELECT
			'JUEGOS_TIENDAS' TIPO,
			NULL PLATAFORMA_NOMBRE,
			NULL PLATAFORMA_CORTO,
			t.NOMBRE DESCRIPCION,
			COUNT(*) CANTIDAD,
			SUM(
				IF(e.DESCRIPCION = 'Digital', 0, 1)
			) FISICO,
			SUM(
				IF(e.DESCRIPCION = 'Digital', 1, 0)
			) DIGITAL,
			SUM(c.COSTE) COSTE,
			NULL ORDEN_DESC,
			UPPER(t.NOMBRE) ORDEN_ASC
		FROM COLECCION c
		INNER JOIN ESTADO e ON e.ID = c.ESTADO_GENERAL_ID
			AND e.TIPO = 0
			AND e.DESCRIPCION NOT IN ('Buscado', 'N/A', 'Reservado', 'Pedido')
		INNER JOIN BASE b ON b.ID = c.BASE_ID
		INNER JOIN TIPO_BASE tb ON tb.ID = b.TIPO_ID
			AND tb.DESCRIPCION = 'Juego'
		INNER JOIN TIENDA t ON t.ID = c.TIENDA_ID
		GROUP BY t.NOMBRE
	) UNION (
		SELECT
			'ROMS_PLATAFORMA' TIPO,
			p.NOMBRE PLATAFORMA_NOMBRE,
			p.CORTO PLATAFORMA_CORTO,
			NULL DESCRIPCION,
			COUNT(*) CANTIDAD,
			NULL FISICO,
			NULL DIGITAL,
			NULL COSTE,
			NULL ORDEN_DESC,
			UPPER(p.NOMBRE) ORDEN_ASC
		FROM ROM r
		INNER JOIN PLATAFORMA p ON p.ID = r.PLATAFORMA_ID
		INNER JOIN BASE b ON b.ID = r.BASE_ID
		INNER JOIN TIPO_BASE tb ON tb.ID = b.TIPO_ID
			AND tb.DESCRIPCION = 'Juego'
		GROUP BY PLATAFORMA_ID
	) UNION (
		SELECT
			'JUEGOS_MEDIA_ANUAL_TOTAL' TIPO,
			NULL PLATAFORMA_NOMBRE,
			NULL PLATAFORMA_CORTO,
			YEAR(IFNULL(c.FECHA_COMPRA, c.FECHA_RECIBO)) DESCRIPCION,
			COUNT(*) CANTIDAD,
			SUM(
				IF(
					e.DESCRIPCION IN (
						'Cartucho', 'Completo', 'Disco', 'Incompleto', 'Precintado', 'Prestado', 'UMD'
					), 1, 0
				)
			) FISICO,
			SUM(
				IF(
					e.DESCRIPCION IN (
						'CIAB', 'Digital'
					), 1, 0
				)
			)  DIGITAL,
			ROUND(SUM(c.COSTE) / COUNT(*), 2) COSTE,
			YEAR(IFNULL(c.FECHA_COMPRA, c.FECHA_RECIBO)) ORDEN_DESC,
			NULL ORDEN_ASC
		FROM COLECCION c
		INNER JOIN BASE b ON b.ID = c.BASE_ID
		INNER JOIN TIPO_BASE tb ON tb.ID = b.TIPO_ID
			AND tb.DESCRIPCION = 'Juego'
		INNER JOIN ESTADO e ON e.ID = c.ESTADO_GENERAL_ID
			AND e.TIPO = 0
			AND e.DESCRIPCION IN (
				'Cartucho', 'Completo', 'Disco', 'Incompleto', 'Precintado', 'Prestado', 'UMD',
				'CIAB', 'Digital'
			)
		WHERE
			(
				c.FECHA_COMPRA IS NOT NULL
				OR
				c.FECHA_RECIBO IS NOT NULL
			)
			AND YEAR(IFNULL(c.FECHA_COMPRA, c.FECHA_RECIBO)) >= 2022
		GROUP BY YEAR(IFNULL(c.FECHA_COMPRA, c.FECHA_RECIBO)), tb.DESCRIPCION
	)
) AS SUBQUERY
ORDER BY TIPO, ORDEN_DESC DESC, ORDEN_ASC;