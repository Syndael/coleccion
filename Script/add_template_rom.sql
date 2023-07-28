/*
	SELECT * FROM JUEGO WHERE NOMBRE LIKE '%Pikmin%'
*/
SET @n_juego = 'Pikmin4'; SELECT * FROM JUEGO WHERE CODIGO = @n_juego;
SET @plata = 'Switch'; SELECT * FROM PLATAFORMA WHERE COALESCE(CORTO, NOMBRE) = @plata;
SET @d_idioma = NULL; SELECT * FROM IDIOMA WHERE CORTO = @d_idioma;
SET @d_region = 'EU'; SELECT * FROM REGION WHERE CORTO = @d_region;
SET @t_rom = 'xci'; SELECT * FROM TIPO_ROM WHERE EXTENSION = @t_rom;

INSERT INTO ROM (JUEGO_ID, PLATAFORMA_ID, IDIOMA_ID, REGION_ID, TIPO_ROM_ID
) SELECT 
    (SELECT ID FROM JUEGO WHERE CODIGO = @n_juego),
    (SELECT ID FROM PLATAFORMA WHERE COALESCE(CORTO, NOMBRE) = @plata),
    (SELECT ID FROM IDIOMA WHERE DESCRIPCION = @d_idioma),
    (SELECT ID FROM REGION WHERE CORTO = @d_region),    
    (SELECT ID FROM TIPO_ROM WHERE EXTENSION = @t_rom)
FROM DUAL;

SELECT * FROM ROM ORDER BY ID DESC LIMIT 10;