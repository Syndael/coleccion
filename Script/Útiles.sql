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
SELECT p.NOMBRE, b.NOMBRE, c.ID, c.FOTOS, c.IG, c.FECHA_IG_PUBLICACION, eg.DESCRIPCION, c.CODIGO,
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
	AND c.FOTOS = 1
-- order by IF(c.IG IS NOT NULL, 1, 0), c.FECHA_IG_PUBLICACION DESC, if(b.saga = 'Pokémon', 1, 0), p.NOMBRE, b.NOMBRE
order by IF(c.IG IS NOT NULL, 1, 0), c.FECHA_IG_PUBLICACION DESC, b.NOMBRE, c.ID
;
*/

/* Revisar fotos para IG */

SELECT p.NOMBRE, b.NOMBRE,
   /* (
        SELECT COUNT(*) 
        FROM FICHERO f 
        WHERE f.COLECCION_ID = c.ID
    ) AS NUM_FICHEROS,*/ -- CONCAT(',', c.ID), 
    c.IG, c.FECHA_IG_PUBLICACION, eg.DESCRIPCION, c.CODIGO
FROM COLECCION c
inner join PLATAFORMA p on p.id = c.PLATAFORMA_ID
inner join BASE b on b.id = c.BASE_ID
inner join TIPO_BASE tb on tb.ID = b.TIPO_ID
	and tb.DESCRIPCION = 'Juego'
inner join ESTADO eg on eg.ID = c.ESTADO_GENERAL_ID
	and eg.tipo = 0 and eg.INSTAGRAMEABLE = 1
WHERE c.ACTIVADO = 1 AND IG IS NOT NULL
	AND FOTOS = 1
   
ORDER BY IF(c.IG IS NOT NULL, 1, 0), c.FECHA_IG_PUBLICACION DESC, if(b.saga = 'Pokémon', 1, 0), p.NOMBRE, b.NOMBRE
-- ORDER BY p.NOMBRE, IF(b.saga = 'Pokémon', 1, 0), b.NOMBRE
;

-- UPDATE COLECCION SET FOTOS = IF(IG IS NOT NULL OR FECHA_IG_PUBLICACION IS NOT NULL, 1, 0);
-- UPDATE COLECCION SET FOTOS = 1 WHERE ID IN ();
-- UPDATE COLECCION SET FOTOS = 0 WHERE ID IN (466,359,374,375,387,389,540,528,438,120,125,117,126);

/*


SELECT p.NOMBRE, b.NOMBRE -- , c.ID -- , c.IG, c.FECHA_IG_PUBLICACION, eg.DESCRIPCION, c.CODIGO
FROM COLECCION c
inner join PLATAFORMA p on p.id = c.PLATAFORMA_ID
inner join BASE b on b.id = c.BASE_ID
inner join TIPO_BASE tb on tb.ID = b.TIPO_ID
	and tb.DESCRIPCION = 'Juego'
inner join ESTADO eg on eg.ID = c.ESTADO_GENERAL_ID
WHERE c.ACTIVADO = 1 AND FOTOS = 0 AND eg.FISICO = 1
ORDER BY p.NOMBRE, IF(b.saga = 'Pokémon', 1, 0), b.NOMBRE
*/


SELECT p.NOMBRE, b.NOMBRE, c.ID, c.IG, c.FECHA_IG_PUBLICACION, c.FOTOS, eg.DESCRIPCION, c.CODIGO,
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
WHERE c.ACTIVADO = 1 AND IG IS NOT NULL
order by c.FECHA_IG_PUBLICACION DESC, if(b.saga = 'Pokémon', 1, 0), p.NOMBRE, b.NOMBRE
;


SELECT IG, LENGTH(IG), RIGHT(IG, 1), LEFT(IG, 39) FROM COLECCION WHERE IG IS NOT NULL ORDER BY LENGTH(IG), RIGHT(IG, 1);
SELECT IG FROM COLECCION WHERE IG IS NOT NULL ORDER BY IG;
SELECT c.IG, CONCAT(b.NOMBRE, ' (', IFNULL(p.NOMBRE, 'NA'), ' | ', IFNULL(r.CORTO, 'NA'), ' | ', IFNULL(i.CORTO, 'NA'), ')')
FROM COLECCION c INNER JOIN BASE b ON b.ID = c.BASE_ID LEFT JOIN PLATAFORMA p ON p.ID = c.PLATAFORMA_ID
LEFT JOIN IDIOMA i ON i.ID = c.IDIOMA_ID LEFT JOIN REGION r ON r.ID = c.REGION_ID
WHERE IG IS NOT NULL ORDER BY b.NOMBRE, p.NOMBRE, r.CORTO, i.CORTO, c.IG;
-- UPDATE COLECCION SET IG = LEFT(IG, 39) WHERE IG IS NOT NULL ORDER BY LENGTH(IG), RIGHT(IG, 1);
