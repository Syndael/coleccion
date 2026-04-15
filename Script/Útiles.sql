/*

select b.nombre from COLECCION c
inner join PLATAFORMA p on p.id = c.PLATAFORMA_ID
	and p.NOMBRE in ('Switch', 'Switch 2')
inner join ESTADO ec on ec.ID = c.ESTADO_CAJA_ID
	and ec.tipo = 1 and ec.descripcion <> 'N/A'
inner join ESTADO eg on eg.ID = c.ESTADO_GENERAL_ID
	and eg.tipo = 0 and eg.descripcion not in ('Precintado', 'CIAB', 'Regalado')
inner join BASE b on b.id = c.BASE_ID
inner join TIPO_BASE tb on tb.ID = b.TIPO_ID
	and tb.DESCRIPCION = 'Juego'
order by if(b.saga = 'Pokémon', 1, 0), b.nombre

*/


/* TABLON de IG */
/*
SELECT p.NOMBRE, b.NOMBRE, c.ID, c.IG, c.FECHA_IG_PUBLICACION, eg.DESCRIPCION, c.CODIGO,
    (
        SELECT COUNT(*) 
        FROM FICHERO f 
        WHERE f.COLECCION_ID = c.ID
    ) AS NUM_FICHEROS
FROM COLECCION c
inner join PLATAFORMA p on p.id = c.PLATAFORMA_ID
inner join BASE b on b.id = c.BASE_ID
inner join TIPO_BASE tb on tb.ID = b.TIPO_ID
	and tb.DESCRIPCION = 'Juego'
inner join ESTADO eg on eg.ID = c.ESTADO_GENERAL_ID
	and eg.tipo = 0 and eg.INSTAGRAMEABLE = 1
WHERE c.ACTIVADO = 1
order by IF(c.IG IS NOT NULL, 1, 0), c.FECHA_IG_PUBLICACION DESC, if(b.saga = 'Pokémon', 1, 0), p.NOMBRE, b.NOMBRE
;
*/

/* Revisar fotos para IG */

SELECT p.NOMBRE, b.NOMBRE,
    (
        SELECT COUNT(*) 
        FROM FICHERO f 
        WHERE f.COLECCION_ID = c.ID
    ) AS NUM_FICHEROS, CONCAT(',', c.ID), c.IG, c.FECHA_IG_PUBLICACION, eg.DESCRIPCION, c.CODIGO
FROM COLECCION c
inner join PLATAFORMA p on p.id = c.PLATAFORMA_ID
inner join BASE b on b.id = c.BASE_ID
inner join TIPO_BASE tb on tb.ID = b.TIPO_ID
	and tb.DESCRIPCION = 'Juego'
inner join ESTADO eg on eg.ID = c.ESTADO_GENERAL_ID
	and eg.tipo = 0 and eg.INSTAGRAMEABLE = 1
WHERE c.ACTIVADO = 1 AND IG IS NOT NULL
	AND FOTOS = 1
   
-- ORDER BY IF(c.IG IS NOT NULL, 1, 0), c.FECHA_IG_PUBLICACION DESC, if(b.saga = 'Pokémon', 1, 0), p.NOMBRE, b.NOMBRE
ORDER BY p.NOMBRE, IF(b.saga = 'Pokémon', 1, 0), b.NOMBRE
;

-- UPDATE COLECCION SET FOTOS = IF(IG IS NOT NULL OR FECHA_IG_PUBLICACION IS NOT NULL, 1, 0);
-- UPDATE COLECCION SET FOTOS = 1 WHERE ID IN ();
-- UPDATE COLECCION SET FOTOS = 0 WHERE ID IN (466,359,374,375,387,389,540,528,438,120,125,117,126);

/*


SELECT p.NOMBRE, b.NOMBRE -- , c.ID, c.IG, c.FECHA_IG_PUBLICACION, eg.DESCRIPCION, c.CODIGO
FROM COLECCION c
inner join PLATAFORMA p on p.id = c.PLATAFORMA_ID
inner join BASE b on b.id = c.BASE_ID
inner join TIPO_BASE tb on tb.ID = b.TIPO_ID
	and tb.DESCRIPCION = 'Juego'
inner join ESTADO eg on eg.ID = c.ESTADO_GENERAL_ID
WHERE c.ACTIVADO = 1 AND FOTOS = 0
ORDER BY p.NOMBRE, IF(b.saga = 'Pokémon', 1, 0), b.NOMBRE
*/
