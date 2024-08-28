import os
import re

extensiones = ['mkv', 'mp4', 'ts', 'avi']
rutas_pelis = ['/volume1/Media/Movies', '/volumeUSB1/usbshare/Media/Movies/']  # Lista de rutas de películas
rutas_series = ['/volume1/Media/TV Shows', '/volumeUSB1/usbshare/Media/TV Shows/']  # Lista de rutas de series

def limpiar_nombre(nombre):
    # Expresión regular para eliminar la numeración del tipo "01. "
    return re.sub(r'^\d{2}\. ', '', nombre)

def main():
    pelis = []
    for ruta_pelis in rutas_pelis:
        for ruta, carpetas, archivos in os.walk(ruta_pelis):
            for archivo in archivos:
                nombre_archivo, extension_archivo = os.path.splitext(archivo)
                if extension_archivo.replace('.', '').lower() in extensiones:
                    nombre_limpio = limpiar_nombre(nombre_archivo)
                    pelis.append(nombre_limpio)

    with open("/volume1/Media/peliculas.txt", "w") as archivo:
        for item in sorted(pelis):
            archivo.write(item + "\n")

    series = {}
    for ruta_series in rutas_series:
        for serie in os.listdir(ruta_series):
            ruta_serie = os.path.join(ruta_series, serie)
            if os.path.isdir(ruta_serie):
                temporadas = [nombre for nombre in os.listdir(ruta_serie) if
                              os.path.isdir(os.path.join(ruta_serie, nombre))]
                if serie not in series:
                    series[serie] = {'temp': []}
                series[serie]['temp'].extend(temporadas)

    with open("/volume1/Media/series.txt", "w") as archivo:
        for item in sorted(series):
            txt_serie = f'{item} ('
            primera = True
            for temporada in sorted(set(series[item]['temp'])):
                txt_temp = temporada.replace('Season ', 'T')
                if primera:
                    primera = False
                else:
                    txt_serie += ', '
                txt_serie += f'{txt_temp}'
            txt_serie += f')'
            archivo.write(txt_serie + "\n")


if __name__ == '__main__':
    main()
