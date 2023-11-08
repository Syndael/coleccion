import logging, os, requests, zipfile
import shutil
from datetime import date, datetime
from PIL import Image

from telegram import Update, InputFile, InputMediaPhoto, InputMediaDocument
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from utils import constantes
from utils.config_parser_utils import ConfigParser

_config = ConfigParser()

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s: %(message)s', datefmt='%d/%m/%Y %H:%M:%S',
                    level=logging.INFO)
current_date = datetime.now().strftime('%Y%m%d')
log_config_name = _config.get_value(constantes.LOG_FILE)
log_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), f'{log_config_name}_{current_date}.log')
file_handler = logging.FileHandler(log_file, mode='a', encoding='UTF-8')
file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(levelname)s - %(name)s: %(message)s', datefmt='%d/%m/%Y %H:%M:%S'))
logging.getLogger().addHandler(file_handler)
logging.getLogger('httpx').setLevel(logging.WARN)

bot = None
token = None
url = None
usuarios_amigo = None
usuarios_vip = None

directorio_imgs = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'imgs')


def hacer_peticion(modulo, paths=None, params=None):
    if params is None:
        params = []
    try:
        url = get_url() + modulo
        if paths:
            path_string = '/'.join([f'{path}' for path in paths])
            url += '/' + path_string
        if params:
            param_string = '&'.join([f'{param}={valor}' for param, valor in params])
            url += '?' + param_string

        response = requests.get(url, verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            return constantes.ERROR_VACIO

    except requests.exceptions.RequestException as e:
        logging.error(e)
        return constantes.ERROR_SOLICITUD


def get_token():
    global token
    if not token:
        token = _config.get_value(constantes.TOKEN)
    return token


def get_url():
    global url
    if not url:
        url = _config.get_value(constantes.URL)
    return url


def get_usuarios_amigo():
    global usuarios_amigo
    if not usuarios_amigo:
        usuarios_amigo = [f'@{usuario}' for usuario in _config.get_value(constantes.WHITELIST).split(',')]
    return usuarios_amigo


def get_usuarios_vip():
    global usuarios_vip
    if not usuarios_vip:
        usuarios_vip = [f'@{usuario}' for usuario in _config.get_value(constantes.VIPLIST).split(',')]
    return usuarios_vip


def get_ruta(nombre_fichero=None):
    if nombre_fichero:
        return os.path.join(directorio_imgs, nombre_fichero)
    else:
        return directorio_imgs


def log_info(update, param):
    logging.info(f'El usuario {update.effective_user.username} ha consultado {param}: {update.message.text}')


async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log_info(update, 'ayuda')
    usuario = update.message.from_user.name
    mensaje = '<b>Opciones</b>:'
    mensaje = mensaje + '\n' + constantes.SEP + 'Detalles para descargar /descargas'
    mensaje = mensaje + '\n' + constantes.SEP + 'Detalles para subir /subir'
    mensaje = mensaje + '\n' + constantes.SEP + 'Consultar la colección con parámetros:'
    mensaje = mensaje + '\n' + constantes.SEP_DOBLE + 'Resumen con: /colec'
    mensaje = mensaje + '\n' + constantes.SEP_DOBLE + '/colec p Plataforma'
    mensaje = mensaje + '\n' + constantes.SEP_DOBLE + '/colec n Nombre'
    mensaje = mensaje + '\n' + constantes.SEP_DOBLE + '/colec s Saga'
    mensaje = mensaje + '\n' + constantes.SEP_DOBLE + 'Ej.: /colec p switch, n esc, s poke'
    mensaje = mensaje + '\n' + constantes.SEP + 'Consultar la lista de roms con:'
    mensaje = mensaje + '\n' + constantes.SEP_DOBLE + 'Resumen con: /juegos'
    mensaje = mensaje + '\n' + constantes.SEP_DOBLE + '/juegos p Plataforma'
    mensaje = mensaje + '\n' + constantes.SEP_DOBLE + '/juegos n Nombre'
    mensaje = mensaje + '\n' + constantes.SEP_DOBLE + '/juegos s Saga'
    mensaje = mensaje + '\n' + constantes.SEP_DOBLE + 'Ej.: /juegos p switch, n esc, s poke'
    mensaje = mensaje + '\n' + constantes.SEP + 'Consultar plataformas con /plataformas'
    mensaje = mensaje + '\n' + constantes.SEP + 'Consultar estadísticas con:'
    mensaje = mensaje + '\n' + constantes.SEP_DOBLE + 'Completos /stats c'
    if usuario and usuario in get_usuarios_vip():
        mensaje = mensaje + '\n' + constantes.SEP_DOBLE + 'Gastos /stats g'
    mensaje = mensaje + '\n' + constantes.SEP_DOBLE + 'Últimos /stats u'

    await update.message.reply_text(mensaje, parse_mode=ParseMode.HTML)


async def descargas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log_info(update, 'descargas')
    url_descarga = _config.get_value(constantes.SYNNAS_URL_DESCARGA)
    mensaje = f'Descargas en {url_descarga}'
    usuario = update.message.from_user.name
    if usuario and usuario in get_usuarios_amigo():
        contra = _config.get_value(constantes.SYNNAS_CONTRASENA_COMUN)
        mensaje = mensaje + '\n' + constantes.SEP + f'Contraseña (la misma para todo): {contra}'
    await update.message.reply_text(mensaje)


async def subir(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log_info(update, 'subir')
    usuario = update.message.from_user.name
    if usuario and usuario in get_usuarios_amigo():
        url_subida = _config.get_value(constantes.SYNNAS_URL_SUBIDA)
        sftp_subida = _config.get_value(constantes.SYNNAS_SFTP_SUBIDA)
        mensaje = f'<b>Subidas:</b>'
        mensaje = f'{mensaje}\n{constantes.SEP}Servicio:'
        mensaje =f'{mensaje}\n{constantes.SEP_DOBLE}Web: {url_subida}'
        mensaje =f'{mensaje}\n{constantes.SEP_DOBLE}SFTP: {sftp_subida}'

        synnas_usuario = _config.get_value(constantes.SYNNAS_USUARIO_SUBIDA)
        synnas_contra = _config.get_value(constantes.SYNNAS_CONTRASENA_SUBIDA)
        mensaje = f'{mensaje}\n{constantes.SEP}Usuario:'
        mensaje =f'{mensaje}\n{constantes.SEP_DOBLE}Usuario: {synnas_usuario}'
        mensaje =f'{mensaje}\n{constantes.SEP_DOBLE}Contraseña: {synnas_contra}'
    else:
        mensaje = 'No tienes permisos para subir ficheros'

    if mensaje:
        await update.message.reply_text(mensaje, disable_web_page_preview=True, parse_mode=ParseMode.HTML)


def comprimir_imagen(input_path, output_path, calidad=85):
    imagen = Image.open(input_path)
    imagen.save(output_path, optimize=True, quality=calidad)


def obtener_tamanio_imagen(imagen_path):
    return os.path.getsize(imagen_path)


def comprimir_hasta_maximo(input_path, output_path, max_size_mb):
    calidad = 85
    tamanio_maximo_bytes = max_size_mb * 1024 * 1024

    while True:
        comprimir_imagen(input_path, output_path, calidad)
        tamanio_actual_bytes = obtener_tamanio_imagen(output_path)

        if tamanio_actual_bytes <= tamanio_maximo_bytes:
            break
        calidad -= 5


async def coleccion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global bot
    local_bot = bot
    local_bot_chat = update.effective_chat.id

    log_info(update, 'coleccion')
    try:
        usuario = update.message.from_user.name
        mensaje_recibido = update.message.text
        if mensaje_recibido == '/colec' or mensaje_recibido == '/coleccion':
            await update.message.reply_text('Todavía no se hacer eso :(')
        else:
            parametros_encontrados = []
            nombre = None
            saga = None
            contiene_plataforma = False
            contiene_nombre = False
            contiene_saga = False

            parametro_encontrado = get_parametro_mensaje(mensaje_recibido, ' p ', constantes.PARAM_PLATAFORMA)
            if parametro_encontrado:
                contiene_plataforma = True
                parametros_encontrados.append(parametro_encontrado)

            parametro_encontrado = get_parametro_mensaje(mensaje_recibido, ' n ', constantes.PARAM_NOMBRE)
            if parametro_encontrado:
                contiene_nombre = True
                parametro_encontrado_param, parametro_encontrado_nombre = parametro_encontrado
                nombre = parametro_encontrado_nombre
                parametros_encontrados.append(parametro_encontrado)

            parametro_encontrado = get_parametro_mensaje(mensaje_recibido, ' s ', constantes.PARAM_SAGA)
            if parametro_encontrado:
                contiene_saga = True
                parametro_encontrado_param, parametro_encontrado_saga = parametro_encontrado
                saga = parametro_encontrado_saga
                parametros_encontrados.append(parametro_encontrado)

            parametro_encontrado = get_parametro_mensaje(mensaje_recibido, ' i ', constantes.PARAM_ID)
            if parametro_encontrado:
                parametros_encontrados.append(parametro_encontrado)

            if any(parametros_encontrados):
                parametros_encontrados.append((constantes.PARAM_ORDEN, 'telegram'))
                data = hacer_peticion(constantes.COLECCIONES, None, parametros_encontrados)
                if data:
                    pre_mensaje = 'Juegos en la colección'
                    if contiene_plataforma:
                        primer_item = data[0]
                        plataforma = primer_item['plataforma']['nombre']
                        plata_corto = primer_item['plataforma']['corto']
                        if plata_corto:
                            pre_mensaje = f'{pre_mensaje} para <b>{plataforma}</b> ({plata_corto})'
                        else:
                            pre_mensaje = f'{pre_mensaje} para <b>{plataforma}</b>'

                    if contiene_nombre and nombre:
                        pre_mensaje = f'{pre_mensaje} que contengan en el nombre <b>{nombre}</b>'

                    if contiene_saga and saga:
                        pre_mensaje = f'{pre_mensaje} de la saga <b>{saga}</b>'

                    mensaje_colecciones = []
                    for item in data:
                        nombre_base = item['base']['nombre']
                        plataforma = item['plataforma']['corto']
                        if not plataforma:
                            plataforma = item['plataforma']['nombre']
                        edicion = item['edicion']
                        if edicion:
                            edicion = edicion['nombre']
                        idioma = item['idioma']
                        if idioma:
                            idioma = idioma['corto']
                        region = item['region']
                        if region:
                            region = region['corto']
                        estado = item['estado_general']['descripcion']
                        estado_caja = item['estado_caja']['descripcion']
                        coste = item['coste']
                        if coste:
                            coste = str(round(float(coste), 2)) + '€'

                        mensaje_rom = ''
                        if not contiene_plataforma:
                            mensaje_rom = f'({plataforma}) '
                        mensaje_rom = f'{mensaje_rom}{nombre_base}'
                        if edicion:
                            mensaje_rom = f'{mensaje_rom}: {edicion}'
                        if idioma and region:
                            mensaje_rom = f'{mensaje_rom} ({idioma} / {region})'
                        elif idioma:
                            mensaje_rom = f'{mensaje_rom} ({idioma})'
                        elif region:
                            mensaje_rom = f'{mensaje_rom} ({region})'
                        if usuario and usuario in get_usuarios_amigo():
                            mensaje_rom = f'{mensaje_rom} | {item["id"]}'
                        mensaje_rom = f'{mensaje_rom} | {estado} {estado_caja}'
                        if usuario and usuario in get_usuarios_vip() and coste:
                            mensaje_rom = f'{mensaje_rom} | {coste}'

                        if item['base']['tipo_base']['descripcion'] == 'Juego':
                            mensaje_colecciones.append(mensaje_rom)

                    data_ficheros = None
                    if len(data) == 1 and usuario and usuario in get_usuarios_amigo():
                        data_ficheros = hacer_peticion(constantes.DATOS_FICHEROS_COLECCION, [data[0]['id']], None)

                    if data_ficheros:
                        try:
                            data_ficheros = [dato for dato in data_ficheros if dato['tipo_fichero'] == 'Foto' and (
                                        '.jpg' in dato['nombre_original'] or '.png' in dato['nombre_original'])]
                            media_group = []

                            for data_fichero in data_ficheros:
                                url_fichero = f'{get_url()}{constantes.URL_FILES}{data_fichero["id"]}'
                                response = requests.get(url_fichero, verify=False)
                                response.raise_for_status()
                                with open(get_ruta(data_fichero['nombre_final']), 'wb') as imagen_local:
                                        imagen_local.write(response.content)

                                original = get_ruta(data_fichero['nombre_final'])
                                comprimido = get_ruta(data_fichero['nombre_original'])
                                shutil.copy(original, comprimido)
                                comprimir_hasta_maximo(original, comprimido, 1)
                                media_group.append(InputMediaPhoto(media=open(comprimido, 'rb')))

                            mensaje = f'Encontrado un juego de {data[0]["plataforma"]["nombre"]}:\n{constantes.SEP}{mensaje_colecciones[0]}'
                            await update.message.reply_text(mensaje, parse_mode=ParseMode.HTML)

                            imagenes_por_album = 5
                            try:
                                for i in range(0, len(media_group), imagenes_por_album):
                                    media_group_paginado = []

                                    for media in media_group[i:i + imagenes_por_album]:
                                        media_group_paginado.append(media)

                                    await local_bot.send_media_group(chat_id=local_bot_chat, media=media_group_paginado)
                            except Exception as e:
                                logging.error('Error al enviar el mensaje multimedia', e)

                        except Exception as e:
                            logging.error('Error al descargar o enviar la imagen', e)
                    else:
                        bloques = 50
                        tamanio_lista = len(mensaje_colecciones)
                        total_bloques = tamanio_lista // bloques + (tamanio_lista % bloques > 0)
                        for i in range(0, tamanio_lista, bloques):
                            bloque_actual = mensaje_colecciones[i:i + bloques]
                            mensaje_bloque = pre_mensaje + f', con un total de {tamanio_lista} juegos'
                            if total_bloques > 1:
                                mensaje_bloque = mensaje_bloque + f' ({i // bloques + 1}/{total_bloques}):'
                            else:
                                mensaje_bloque = mensaje_bloque + f':'

                            for item in bloque_actual:
                                mensaje_bloque += f'\n' + constantes.SEP + f'{item}'
                            await update.message.reply_text(mensaje_bloque, parse_mode=ParseMode.HTML)
                else:
                    await update.message.reply_text('No se han encontrado coincidencias, consulta la ayuda con /ayuda')
            else:
                await update.message.reply_text(
                    'No se han especificado parámetros válidos, consulta la ayuda con /ayuda')
    except Exception as e:
        logging.error(e)
        await bot.send_message(update.effective_chat.id,
                               'Se ha producido un error, puedes consultar la ayuda con /ayuda')
    limpiar_imgs()


async def roms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global bot

    log_info(update, 'roms')
    try:
        mensaje_recibido = update.message.text
        if mensaje_recibido == '/juegos' or mensaje_recibido == '/roms':
            await estadisticas_gastos(update, True)
        else:
            parametros_encontrados = []
            nombre = None
            saga = None
            contiene_plataforma = False
            contiene_nombre = False
            contiene_saga = False

            parametro_encontrado = get_parametro_mensaje(mensaje_recibido, ' p ', constantes.PARAM_PLATAFORMA)
            if parametro_encontrado:
                contiene_plataforma = True
                parametros_encontrados.append(parametro_encontrado)

            parametro_encontrado = get_parametro_mensaje(mensaje_recibido, ' n ', constantes.PARAM_NOMBRE)
            if parametro_encontrado:
                contiene_nombre = True
                parametro_encontrado_param, parametro_encontrado_nombre = parametro_encontrado
                nombre = parametro_encontrado_nombre
                parametros_encontrados.append(parametro_encontrado)

            parametro_encontrado = get_parametro_mensaje(mensaje_recibido, ' s ', constantes.PARAM_SAGA)
            if parametro_encontrado:
                contiene_saga = True
                parametro_encontrado_param, parametro_encontrado_saga = parametro_encontrado
                saga = parametro_encontrado_saga
                parametros_encontrados.append(parametro_encontrado)

            if any(parametros_encontrados):
                data = hacer_peticion(constantes.ROMS, None, parametros_encontrados)

                if data:
                    pre_mensaje = 'Búsqueda de roms'
                    if contiene_plataforma:
                        primer_item = data[0]
                        plataforma = primer_item['plataforma']['nombre']
                        plata_corto = primer_item['plataforma']['corto']
                        if plata_corto:
                            pre_mensaje = f'{pre_mensaje} para <b>{plataforma}</b> ({plata_corto})'
                        else:
                            pre_mensaje = f'{pre_mensaje} para <b>{plataforma}</b>'

                    if contiene_nombre and nombre:
                        pre_mensaje = f'{pre_mensaje} que contengan en el nombre <b>{nombre}</b>'

                    if contiene_saga and saga:
                        pre_mensaje = f'{pre_mensaje} de la saga <b>{saga}</b>'

                    mensaje_roms = []
                    for item in data:
                        nombre_base = item['base']['nombre']
                        mensaje_rom = f'{nombre_base}'

                        if item['tipo_rom']:
                            extension = item['tipo_rom']['extension']
                            mensaje_rom = f'{mensaje_rom} (.{extension})'

                        if item['update']:
                            update_rom = item['update']
                            mensaje_rom = f'{mensaje_rom} <b>{update_rom}</b>'

                        mensaje_roms.append(mensaje_rom)

                    bloques = 50
                    tamanio_lista = len(mensaje_roms)
                    total_bloques = tamanio_lista // bloques + (tamanio_lista % bloques > 0)
                    for i in range(0, tamanio_lista, bloques):
                        bloque_actual = mensaje_roms[i:i + bloques]
                        mensaje_bloque = pre_mensaje + f', con un total de {tamanio_lista} juegos'
                        if total_bloques > 1:
                            mensaje_bloque = mensaje_bloque + f' ({i // bloques + 1}/{total_bloques}):'
                        else:
                            mensaje_bloque = mensaje_bloque + f':'

                        for item in bloque_actual:
                            mensaje_bloque += f'\n' + constantes.SEP + f'{item}'
                        await update.message.reply_text(mensaje_bloque, parse_mode=ParseMode.HTML)
                else:
                    await update.message.reply_text('No se han encontrado coincidencias, consulta la ayuda con /ayuda')
            else:
                await update.message.reply_text(
                    'No se han especificado parámetros válidos, consulta la ayuda con /ayuda')
    except Exception as e:
        logging.error(e)
        await bot.send_message(update.effective_chat.id,
                               'Se ha producido un error, puedes consultar la ayuda con /ayuda')


async def plataformas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log_info(update, 'plataformas')
    data = hacer_peticion(constantes.PLATAFORMAS, None, None)
    if not (data == constantes.ERROR_SOLICITUD or data == constantes.ERROR_VACIO):
        mensaje = 'Lista de plataformas:'
        for item in data:
            nombre_plataforma = item['nombre']
            corto_plataforma = item['corto']
            if corto_plataforma:
                mensaje = mensaje + f'\n' + constantes.SEP + f'{nombre_plataforma} ({corto_plataforma})'
            else:
                mensaje = mensaje + f'\n' + constantes.SEP + f'{nombre_plataforma}'

        await update.message.reply_text(mensaje)
    else:
        await update.message.reply_text('No se ha podido recuperar el listado de plataformas')


async def estadisticas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log_info(update, 'estadisticas')
    mensaje_recibido = update.message.text
    usuario = update.message.from_user.name

    if mensaje_recibido.find(' c') != -1:
        await estadisticas_completos(update)
    elif mensaje_recibido.find(' g') != -1 and usuario and usuario in get_usuarios_vip():
        await estadisticas_gastos(update, None)
    elif mensaje_recibido.find(' u') != -1:
        await estadisticas_ultimos(update)
    else:
        await update.message.reply_text('No te entiendo, puedes consultar la ayuda con /ayuda')


async def estadisticas_completos(update: Update) -> None:
    data = hacer_peticion(constantes.ESTADISTICAS_COMPLETOS, None, None)
    if not (data == constantes.ERROR_SOLICITUD or data == constantes.ERROR_VACIO):
        anio_mes_max = date.today().replace(year=date.today().year - 1).replace(month=date.today().month + 1).strftime(
            "%Y%m")
        mensaje = 'Completos último año:'
        for item in data:
            juegos = item['juegos']
            mes = item['mes']
            orden = item['orden_desc']
            if orden >= anio_mes_max:
                mensaje = mensaje + f'\n' + constantes.SEP + f'{mes}:'
                for juego in juegos.split(', '):
                    mensaje = mensaje + f'\n' + constantes.SEP_DOBLE + f'{juego}'

        await update.message.reply_text(mensaje)
    else:
        await update.message.reply_text('No se han podido recuperar las estadísticas')


async def estadisticas_gastos(update: Update, roms) -> None:
    data = hacer_peticion(constantes.ESTADISTICAS_GASTOS, None, None)
    if not (data == constantes.ERROR_SOLICITUD or data == constantes.ERROR_VACIO):
        mensaje_juegos_mes = 'Juegos por mes:'
        mensaje_juegos_plataforma = 'Juegos por plataforma:'
        mensaje_juegos_tienda = 'Juegos por tienda:'
        mensaje_total = 'Total:'

        mensaje_roms_plataforma = 'Roms:'

        if roms:
            for valor in sorted([item for item in data if item['tipo'] == constantes.ESTADISTICAS_TIPO_ROMS_PLATAFORMA],
                                key=lambda x: (x['orden_asc'] if x['orden_asc'] is not None else '')):
                mensaje_roms_plataforma = mensaje_roms_plataforma + f'\n' + constantes.SEP + valor.get(
                    'plataforma_nombre') + ' ' + str(valor.get('cantidad')) + ' juegos'
            await update.message.reply_text(mensaje_roms_plataforma)
        else:
            for valor in sorted([item for item in data if item['tipo'] == constantes.ESTADISTICAS_TIPO_JUEGOS_MES],
                                key=lambda x: (x['orden_desc'] if x['orden_desc'] is not None else ''), reverse=True)[
                         :12]:
                mensaje_juegos_mes = mensaje_juegos_mes + f'\n' + constantes.SEP + valor.get('descripcion') + ' ' + str(
                    valor.get('cantidad')) + ' juegos a ' + str(round(float(valor.get('coste')), 2)) + '€'

            await update.message.reply_text(mensaje_juegos_mes)

            for valor in sorted(
                    [item for item in data if item['tipo'] == constantes.ESTADISTICAS_TIPO_JUEGOS_PLATAFORMA],
                    key=lambda x: (x['orden_asc'] if x['orden_asc'] is not None else '')):
                mensaje_juegos_plataforma = mensaje_juegos_plataforma + f'\n' + constantes.SEP + valor.get(
                    'plataforma_nombre') + ' ' + str(valor.get('cantidad')) + ' juegos'
                if valor.get('coste'):
                    mensaje_juegos_plataforma = mensaje_juegos_plataforma + ' a ' + str(
                        round(float(valor.get('coste')), 2)) + '€'
            await update.message.reply_text(mensaje_juegos_plataforma)

            for valor in sorted([item for item in data if item['tipo'] == constantes.ESTADISTICAS_TIPO_JUEGOS_TIENDAS],
                                key=lambda x: (x['orden_asc'] if x['orden_asc'] is not None else '')):
                mensaje_juegos_tienda = mensaje_juegos_tienda + f'\n' + constantes.SEP + valor.get(
                    'descripcion') + ' ' + str(valor.get('cantidad')) + ' juegos a ' + str(
                    round(float(valor.get('coste')), 2)) + '€'
            await update.message.reply_text(mensaje_juegos_tienda)

            for valor in [item for item in data if item['tipo'] == constantes.ESTADISTICAS_TIPO_CONSOLAS_TOTAL or item[
                'tipo'] == constantes.ESTADISTICAS_TIPO_JUEGOS_TOTAL]:
                mensaje_total = mensaje_total + f'\n' + constantes.SEP
                if valor.get('tipo') == constantes.ESTADISTICAS_TIPO_CONSOLAS_TOTAL:
                    mensaje_total = mensaje_total + 'Consolas '
                else:
                    mensaje_total = mensaje_total + 'Juegos '

                mensaje_total = mensaje_total + str(round(float(valor.get('coste')), 2)) + '€'
            await update.message.reply_text(mensaje_total)
    else:
        await update.message.reply_text('No se han podido recuperar las estadísticas')


async def estadisticas_ultimos(update: Update) -> None:
    data = hacer_peticion(constantes.ESTADISTICAS_ULTIMOS, None, None)
    if not (data == constantes.ERROR_SOLICITUD or data == constantes.ERROR_VACIO):
        mensaje = 'Últimos jugados:'
        for item in data[:5]:
            nombre = item['base']['nombre']
            estado = item['estado_progreso']['descripcion']
            horas = round(float(item['horas']), 2)
            plataforma = item['plataforma']['corto'] if item['plataforma']['corto'] else item['plataforma']['nombre']
            mensaje = mensaje + f'\n' + constantes.SEP + f'({plataforma}) {nombre}: {horas}h - {estado}'

        await update.message.reply_text(mensaje)
    else:
        await update.message.reply_text('No se han podido recuperar las estadísticas')


async def defecto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log_info(update, 'defecto')
    await update.message.reply_text('No te entiendo, puedes consultar la ayuda con /ayuda')


def get_parametro_mensaje(mensaje_recibido, indentificador, parametro):
    if indentificador in mensaje_recibido:
        for mensaje_split in mensaje_recibido.split(','):
            if indentificador in mensaje_split:
                param = get_parametro(mensaje_split, indentificador)
                if param:
                    return parametro, param
    return None


def get_parametro(texto, param):
    posicion_param = texto.find(param)
    if posicion_param != -1:
        posicion = texto.find(' ', posicion_param)
        if posicion != -1:
            return texto[posicion + len(param): len(texto)]
        else:
            return None
    else:
        return None


def limpiar_imgs():
    try:
        for archivo in os.listdir(get_ruta()):
            ruta_completa = get_ruta(archivo)
            if os.path.isfile(ruta_completa):
                os.remove(ruta_completa)
    except Exception as e:
        logging.error('Error eliminando las imagenes')


def main() -> None:
    global bot

    try:
        os.mkdir(get_ruta())
    except FileExistsError:
        logging.debug(f'El directorio {get_ruta()} ya existe.')
    except Exception as e:
        logging.error('Error al crear el directorio', e)

    application = Application.builder().token(get_token()).build()
    bot = application.bot

    application.add_handler(CommandHandler('start', ayuda))
    application.add_handler(CommandHandler('iniciar', ayuda))
    application.add_handler(CommandHandler('ayuda', ayuda))

    application.add_handler(CommandHandler('descargas', descargas))

    application.add_handler(CommandHandler('subir', subir))

    application.add_handler(CommandHandler('colec', coleccion))
    application.add_handler(CommandHandler('coleccion', coleccion))

    application.add_handler(CommandHandler('juegos', roms))
    application.add_handler(CommandHandler('roms', roms))

    application.add_handler(CommandHandler('plataformas', plataformas))

    application.add_handler(CommandHandler('stats', estadisticas))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, defecto))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
