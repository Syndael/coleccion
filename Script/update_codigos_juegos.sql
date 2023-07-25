UPDATE JUEGO SET CODIGO = REGEXP_REPLACE(
	REPLACE(
		REPLACE(
			REPLACE(
				REPLACE(
					REPLACE(
						NOMBRE, 'ú', 'u'
					), 'ó', 'o'
				), 'í', 'i'
			), 'é', 'e'
		), 'á', 'a'
	), '[^a-zA-Z0-9]', ''
);