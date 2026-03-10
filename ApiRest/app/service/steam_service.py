import os
import re

import requests
from flask import jsonify

from app.model.base_model import Base
from app.model.coleccion_model import Coleccion
from app.model.estado_model import Estado
from app.model.plataforma_model import Plataforma
from app.model.tienda_model import Tienda
from app.model.tipo_base_model import TipoBase
from app.utils.datos import db
from app.utils.config_parser_utils import ConfigParser



class SteamService:
    _config = ConfigParser()
    _api_url = 'https://api.steampowered.com'

    def import_owned_games(self, request):
        data = request.get_json() or {}
        steam_user = data.get('steam_user')
        if not steam_user:
            return jsonify({'message': 'steam_user es obligatorio'}), 400

        # In case you want to use os/terminal environment
        # api_key = os.getenv('STEAM_API_KEY')
        api_key = self._config.get_value("steam_api_key")
        if not api_key:
            return jsonify({'message': 'No se ha configurado STEAM_API_KEY'}), 500

        print("Steam API Key:", api_key)
        steam_id, error = self._resolve_steam_id(api_key, steam_user)
        if error:
            return jsonify({'message': error}), 400

        owned_games, error = self._get_owned_games(api_key, steam_id)
        if error:
            return jsonify({'message': error}), 400

        tipo_juego = TipoBase.query.filter(TipoBase.descripcion == 'Juego').first()
        plataforma_pc = Plataforma.query.filter(Plataforma.nombre == 'PC').first()
        estado_general_digital = Estado.query.filter(Estado.tipo == 0, Estado.descripcion == 'Digital').first()
        estado_caja_na = Estado.query.filter(Estado.tipo == 1, Estado.descripcion == 'N/A').first()
        tienda_steam = Tienda.query.filter(Tienda.nombre == 'Steam').first()

        if not tipo_juego or not plataforma_pc or not estado_general_digital or not estado_caja_na:
            return jsonify({'message': 'Faltan datos maestros requeridos (Juego, PC, Digital, N/A)'}), 500

        bases = Base.query.filter(Base.tipo_id == tipo_juego.id).all()
        bases_por_nombre = {}
        for base in bases:
            nombre_normalizado = self._normalizar_titulo(base.nombre)
            if not nombre_normalizado:
                continue
            if nombre_normalizado not in bases_por_nombre:
                bases_por_nombre[nombre_normalizado] = []
            bases_por_nombre[nombre_normalizado].append(base)

        colecciones_pc = Coleccion.query.join(Coleccion.base).filter(
            Coleccion.activado == 1,
            Coleccion.plataforma_id == plataforma_pc.id,
            Base.tipo_id == tipo_juego.id
        ).all()

        existentes_por_nombre = {}
        for coleccion in colecciones_pc:
            nombre_normalizado = self._normalizar_titulo(coleccion.base.nombre)
            if nombre_normalizado:
                existentes_por_nombre[nombre_normalizado] = coleccion

        importados = []
        omitidos_duplicado = []
        omitidos_dudosos = []
        errores = []

        try:
            for game in owned_games:
                nombre = game.get('name')
                app_id = game.get('appid')

                if not nombre:
                    errores.append({'appid': app_id, 'error': 'Juego sin nombre en respuesta de Steam'})
                    continue

                nombre_normalizado = self._normalizar_titulo(nombre)
                if not nombre_normalizado:
                    errores.append({'appid': app_id, 'name': nombre, 'error': 'Nombre no válido tras normalización'})
                    continue

                if nombre_normalizado in existentes_por_nombre:
                    omitidos_duplicado.append({'appid': app_id, 'name': nombre, 'reason': 'Ya existe en colección para PC'})
                    continue

                bases_encontradas = bases_por_nombre.get(nombre_normalizado, [])
                if len(bases_encontradas) > 1:
                    omitidos_dudosos.append({'appid': app_id, 'name': nombre, 'reason': 'Coincidencia ambigua con varias bases'})
                    continue

                if len(bases_encontradas) == 1:
                    base = bases_encontradas[0]
                else:
                    base = Base(tipo_base=tipo_juego, nombre=nombre)
                    if app_id:
                        base.url = f'https://store.steampowered.com/app/{app_id}/'
                    db.session.add(base)
                    db.session.flush()
                    bases_por_nombre[nombre_normalizado] = [base]

                nueva_coleccion = Coleccion(
                    base=base,
                    plataforma=plataforma_pc,
                    estado_general=estado_general_digital,
                    estado_caja=estado_caja_na,
                    tienda=tienda_steam,
                    activado=1
                )
                if app_id:
                    nueva_coleccion.url = f'https://store.steampowered.com/app/{app_id}/'
                    nueva_coleccion.notas = f'Importado desde Steam (appid: {app_id})'
                else:
                    nueva_coleccion.notas = 'Importado desde Steam'

                db.session.add(nueva_coleccion)
                db.session.flush()
                existentes_por_nombre[nombre_normalizado] = nueva_coleccion

                importados.append({'appid': app_id, 'name': nombre, 'coleccion_id': nueva_coleccion.id})

            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            return jsonify({'message': f'Error importando juegos: {str(ex)}'}), 500

        return jsonify({
            'steam_id': steam_id,
            'total_encontrados': len(owned_games),
            'importados': importados,
            'omitidos_duplicado': omitidos_duplicado,
            'omitidos_dudosos': omitidos_dudosos,
            'errores': errores,
            'resumen': {
                'importados': len(importados),
                'omitidos_duplicado': len(omitidos_duplicado),
                'omitidos_dudosos': len(omitidos_dudosos),
                'errores': len(errores)
            }
        }), 200

    def _resolve_steam_id(self, api_key, steam_user):
        steam_user = steam_user.strip()

        profile_match = re.match(r'^https?://steamcommunity\.com/profiles/(\d{17})/?$', steam_user)
        if profile_match:
            return profile_match.group(1), None

        vanity_match = re.match(r'^https?://steamcommunity\.com/id/([^/]+)/?$', steam_user)
        if vanity_match:
            steam_user = vanity_match.group(1)

        if re.match(r'^\d{17}$', steam_user):
            return steam_user, None

        url = f'{self._api_url}/ISteamUser/ResolveVanityURL/v1/'
        try:
            response = requests.get(url, params={'key': api_key, 'vanityurl': steam_user}, timeout=20)
            response.raise_for_status()
            payload = response.json().get('response', {})
            if payload.get('success') == 1 and payload.get('steamid'):
                return payload.get('steamid'), None
            return None, 'No se pudo resolver el vanity URL/usuario de Steam'
        except requests.RequestException as ex:
            return None, f'Error llamando a Steam ResolveVanityURL: {str(ex)}'

    def _get_owned_games(self, api_key, steam_id):
        url = f'{self._api_url}/IPlayerService/GetOwnedGames/v1/'
        try:
            response = requests.get(url, params={
                'key': api_key,
                'steamid': steam_id,
                'include_appinfo': 1,
                'include_played_free_games': 1,
                'format': 'json'
            }, timeout=30)
            response.raise_for_status()
            payload = response.json().get('response', {})
            games = payload.get('games', [])
            return games, None
        except requests.RequestException as ex:
            return None, f'Error llamando a Steam GetOwnedGames: {str(ex)}'

    def _normalizar_titulo(self, texto):
        if not texto:
            return None
        texto = texto.lower().strip()
        texto = re.sub(r'[^a-z0-9]+', ' ', texto)
        texto = re.sub(r'\s+', ' ', texto).strip()
        return texto
