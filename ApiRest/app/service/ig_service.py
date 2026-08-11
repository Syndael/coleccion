import os

from datetime import datetime
try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None

from flask import jsonify

from app.model.base_model import Base
from app.model.coleccion_model import Coleccion
from app.model.fichero_model import Fichero, DatoFichero, DatoFicheroSchema
from app.model.ig_model import IgPublicacion, IgPublicacionSchema, IgFotoSeleccion, IgFotoSeleccionSchema, IgToken, IgTokenSchema
from app.model.plataforma_model import Plataforma
from app.model.estado_model import Estado
from app.model.edicion_model import Edicion
from app.model.idioma_model import Idioma
from app.model.region_model import Region
from app.model.tienda_model import Tienda
from app.model.tipo_base_model import TipoBase
from app.model.tipo_fichero_model import TipoFichero
from app.utils.datos import db
from app.utils.config_parser_utils import ConfigParser
from sqlalchemy import func, or_, not_
from sqlalchemy.orm import aliased


class IgService:
    _ig_publicacion_schema = IgPublicacionSchema()
    _ig_publicaciones_schema = IgPublicacionSchema(many=True)
    _ig_foto_seleccion_schema = IgFotoSeleccionSchema()
    _ig_fotos_seleccion_schema = IgFotoSeleccionSchema(many=True)
    _ig_token_schema = IgTokenSchema()
    _datofichero_schema = DatoFicheroSchema()
    _datosfichero_schema = DatoFicheroSchema(many=True)
    PAGE_SIZE = 25

    @staticmethod
    def _ahora():
        dt = datetime.now(ZoneInfo("Europe/Madrid")) if ZoneInfo else datetime.now()
        return dt.replace(tzinfo=None)

    # ── Publicaciones ──────────────────────────────────────────────

    def get_publicaciones(self, request):
        page = request.args.get('pagina', 1, type=int)
        EstadoCaja = aliased(Estado)
        q = db.session.query(
            Coleccion.id,
            Base.nombre,
            TipoBase.descripcion.label('tipo'),
            Plataforma.nombre.label('plataforma'),
            Edicion.nombre.label('edicion'),
            Idioma.descripcion.label('idioma'),
            Region.descripcion.label('region'),
            Estado.descripcion.label('estado_general'),
            EstadoCaja.descripcion.label('estado_caja'),
            Coleccion.fecha_reserva,
            Coleccion.fecha_compra,
            Coleccion.fecha_recibo,
            Coleccion.envio,
            Coleccion.precio,
            Coleccion.coste,
            Coleccion.unidades,
            Tienda.nombre.label('tienda'),
            Coleccion.url,
            Coleccion.ig,
            IgPublicacion.id.label('ig_publicacion_id'),
            IgPublicacion.estado.label('ig_estado'),
            IgPublicacion.texto_publicacion,
            IgPublicacion.fecha_ig_publicacion.label('ig_pub_fecha'),
            Coleccion.fecha_ig_publicacion.label('col_fecha_ig'),
            IgPublicacion.ig_post_id,
            IgPublicacion.fecha_prevista_publicacion,
            Coleccion.codigo,
        ).select_from(Coleccion)\
         .join(Base, Coleccion.base_id == Base.id)\
         .join(TipoBase, Base.tipo_id == TipoBase.id)\
         .join(Plataforma, Coleccion.plataforma_id == Plataforma.id)\
         .outerjoin(Edicion, Coleccion.edicion_id == Edicion.id)\
         .outerjoin(Idioma, Coleccion.idioma_id == Idioma.id)\
         .outerjoin(Region, Coleccion.region_id == Region.id)\
         .join(Estado, Coleccion.estado_general_id == Estado.id)\
         .outerjoin(EstadoCaja, Coleccion.estado_caja_id == EstadoCaja.id)\
         .outerjoin(Tienda, Coleccion.tienda_id == Tienda.id)\
         .outerjoin(IgPublicacion, Coleccion.id == IgPublicacion.coleccion_id)\
         .filter(Coleccion.activado == 1)

        # Filtros
        if request.args.get('nombre'):
            q = q.filter(Base.nombre.ilike(f'%{request.args.get("nombre")}%'))
        if request.args.get('plataforma_id'):
            q = q.filter(Coleccion.plataforma_id == request.args.get('plataforma_id'))
        if request.args.get('tipo_base_id'):
            q = q.filter(Base.tipo_id == request.args.get('tipo_base_id'))
        if request.args.get('estado_gen_id'):
            q = q.filter(Coleccion.estado_general_id == request.args.get('estado_gen_id'))
        if request.args.get('ig_estado'):
            estados = request.args.get('ig_estado').split(',')
            if 'Revisar' in estados:
                q = q.filter(or_(IgPublicacion.estado.in_(estados), IgPublicacion.id == None))
            else:
                q = q.filter(IgPublicacion.estado.in_(estados))
        if request.args.get('ig_estado_excluir'):
            estados_excluir = request.args.get('ig_estado_excluir').split(',')
            if 'Revisar' in estados_excluir:
                q = q.filter(not_(or_(IgPublicacion.estado.in_(estados_excluir), IgPublicacion.id == None)))
            else:
                q = q.filter(or_(not_(IgPublicacion.estado.in_(estados_excluir)), IgPublicacion.id == None))
        if request.args.get('sin_ig'):
            q = q.filter(Coleccion.ig.is_(None) | (Coleccion.ig == ''))
        if request.args.get('con_ig'):
            q = q.filter(Coleccion.ig.isnot(None) & (Coleccion.ig != ''))
        if request.args.get('con_fotos'):
            sub = db.session.query(Fichero.coleccion_id).filter(Fichero.activado == 1).distinct()
            q = q.filter(Coleccion.id.in_(sub))

        # Conteo de fotos
        foto_count = db.session.query(Fichero.coleccion_id, func.count(Fichero.id).label('total_fotos'))\
            .join(TipoFichero, Fichero.tipo_fichero_id == TipoFichero.id)\
            .filter(Fichero.activado == 1, TipoFichero.descripcion == 'foto')\
            .group_by(Fichero.coleccion_id).subquery()
        q = q.outerjoin(foto_count, Coleccion.id == foto_count.c.coleccion_id)
        q = q.add_columns(func.coalesce(foto_count.c.total_fotos, 0).label('total_fotos'))

        # Orden
        orden = request.args.get('orden', 'tipo_asc')
        if orden == 'id_asc':
            q = q.order_by(Coleccion.id.asc())
        elif orden == 'id_desc':
            q = q.order_by(Coleccion.id.desc())
        elif orden == 'fecha_prevista_desc':
            q = q.order_by(IgPublicacion.fecha_prevista_publicacion.desc(), Coleccion.id.desc())
        elif orden == 'fecha_prevista_pub_desc':
            q = q.order_by(IgPublicacion.fecha_prevista_publicacion.desc(), IgPublicacion.fecha_ig_publicacion.desc(), Coleccion.id.desc())
        elif orden == 'fecha_pub_desc':
            q = q.order_by(IgPublicacion.fecha_ig_publicacion.desc(), Coleccion.id.desc())
        elif orden == 'fecha_pub_asc':
            q = q.order_by(IgPublicacion.fecha_ig_publicacion.asc(), Coleccion.id.asc())
        else:  # tipo_asc (default): tipo, plataforma, nombre
            q = q.order_by(TipoBase.descripcion.asc(), Plataforma.nombre.asc(), Base.nombre.asc())

        # Contar total: sin order_by para evitar errores en la subquery
        total = db.session.query(func.count()).select_from(q.order_by(None).subquery()).scalar() or 0
        resultados = q.limit(self.PAGE_SIZE).offset((page - 1) * self.PAGE_SIZE).all()

        # Formatear
        items = []
        for r in resultados:
            items.append({
                'id': r.id,
                'nombre': r.nombre,
                'tipo': r.tipo,
                'plataforma': r.plataforma,
                'edicion': r.edicion,
                'idioma': r.idioma,
                'region': r.region,
                'estado_general': r.estado_general,
                'estado_caja': r.estado_caja,
                'fecha_reserva': r.fecha_reserva.isoformat() if r.fecha_reserva else None,
                'fecha_compra': r.fecha_compra.isoformat() if r.fecha_compra else None,
                'fecha_recibo': r.fecha_recibo.isoformat() if r.fecha_recibo else None,
                'envio': float(r.envio) if r.envio else None,
                'precio': float(r.precio) if r.precio else None,
                'coste': float(r.coste) if r.coste else None,
                'unidades': r.unidades,
                'tienda': r.tienda,
                'url': r.url,
                'ig': r.ig,
                'ig_publicacion_id': r.ig_publicacion_id,
                'ig_estado': r.ig_estado or 'Revisar',
                'texto_publicacion': r.texto_publicacion,
                'fecha_ig_publicacion': r.ig_pub_fecha.isoformat() if r.ig_pub_fecha else (r.col_fecha_ig.isoformat() + 'T00:00' if r.col_fecha_ig else None),
                'ig_post_id': r.ig_post_id,
                'fecha_prevista_publicacion': r.fecha_prevista_publicacion.isoformat() if r.fecha_prevista_publicacion else None,
                'codigo': r.codigo,
                'total_fotos': r.total_fotos,
            })

        return jsonify({
            'items': items,
            'total': total,
            'pagina': page,
            'total_paginas': max(1, (total + self.PAGE_SIZE - 1) // self.PAGE_SIZE)
        }), 200

    def get_publicacion(self, id):
        try:
            coleccion_id = int(id)
            pub = IgPublicacion.query.filter_by(coleccion_id=coleccion_id).first()
            if not pub:
                coleccion = Coleccion.query.get(coleccion_id)
                if not coleccion:
                    return jsonify({'message': 'Coleccion no encontrada'}), 404
                pub = IgPublicacion(coleccion=coleccion, estado='Revisar')
                db.session.add(pub)
                db.session.commit()

            coleccion = Coleccion.query.get(coleccion_id)
            result = self._ig_publicacion_schema.dump(pub)
            if coleccion:
                if not result.get('fecha_ig_publicacion') and coleccion.fecha_ig_publicacion:
                    result['fecha_ig_publicacion'] = coleccion.fecha_ig_publicacion.isoformat()
            if result.get('fecha_ig_publicacion') and 'T' not in str(result['fecha_ig_publicacion']):
                result['fecha_ig_publicacion'] = str(result['fecha_ig_publicacion']) + 'T00:00'
            if result.get('fecha_prevista_publicacion') and 'T' not in str(result['fecha_prevista_publicacion']):
                result['fecha_prevista_publicacion'] = str(result['fecha_prevista_publicacion']) + 'T00:00'
            if coleccion:
                result['coleccion'] = {
                    'id': coleccion.id,
                    'base': {
                        'id': coleccion.base_id,
                        'nombre': coleccion.base.nombre if coleccion.base else None,
                        'tipo': coleccion.base.tipo_base.descripcion if coleccion.base and coleccion.base.tipo_base else None,
                    },
                    'plataforma': {'id': coleccion.plataforma_id, 'nombre': coleccion.plataforma.nombre if coleccion.plataforma else None},
                    'ig': coleccion.ig,
                    'codigo': coleccion.codigo,
                }
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'message': f'Error: {str(e)}'}), 500

    def update_publicacion(self, request, id):
        data = request.get_json()
        pub = IgPublicacion.query.filter_by(coleccion_id=id).first()
        if not pub:
            coleccion = Coleccion.query.get(id)
            if not coleccion:
                return jsonify({'message': 'Coleccion no encontrada'}), 404
            pub = IgPublicacion(coleccion=coleccion)
            db.session.add(pub)

        if 'estado' in data:
            pub.estado = data['estado']
        if 'texto_publicacion' in data:
            pub.texto_publicacion = data['texto_publicacion']
        if 'fecha_ig_publicacion' in data:
            coleccion_obj = Coleccion.query.get(pub.coleccion_id)
            if coleccion_obj:
                coleccion_obj.fecha_ig_publicacion = data['fecha_ig_publicacion'] if data['fecha_ig_publicacion'] else None
            pub.fecha_ig_publicacion = data['fecha_ig_publicacion']
        if 'fecha_prevista_publicacion' in data:
            pub.fecha_prevista_publicacion = data['fecha_prevista_publicacion'] if data['fecha_prevista_publicacion'] else None
        if 'ig_post_id' in data:
            pub.ig_post_id = data['ig_post_id']
        if 'ig' in data:
            coleccion_obj = Coleccion.query.get(pub.coleccion_id)
            if coleccion_obj:
                coleccion_obj.ig = data['ig'] if data['ig'] else None

        db.session.commit()
        result = self._ig_publicacion_schema.dump(pub)
        return jsonify(result), 200

    # ── Fotos seleccionadas ────────────────────────────────────────

    def get_fotos_seleccion(self, coleccion_id):
        seleccionadas = IgFotoSeleccion.query\
            .filter(IgFotoSeleccion.coleccion_id == coleccion_id, IgFotoSeleccion.activado == 1)\
            .order_by(IgFotoSeleccion.orden.asc()).all()
        result = self._ig_fotos_seleccion_schema.dump(seleccionadas)
        return jsonify(result), 200

    def get_fotos_coleccion(self, coleccion_id):
        """Devuelve todos los ficheros de la colección con info de selección."""
        ficheros = Fichero.query\
            .filter(Fichero.coleccion_id == coleccion_id, Fichero.activado == 1)\
            .order_by(Fichero.nombre_original.asc()).all()

        selecciones = {
            s.fichero_id: s for s in IgFotoSeleccion.query
            .filter(IgFotoSeleccion.coleccion_id == coleccion_id, IgFotoSeleccion.activado == 1)
            .all()
        }

        items = []
        for f in ficheros:
            sel = selecciones.get(f.id)
            items.append({
                'id': f.id,
                'nombre_original': f.nombre_original,
                'nombre_almacenado': f.nombre_almacenado,
                'tipo_fichero': f.tipo_fichero.descripcion if f.tipo_fichero else None,
                'seleccionada': sel is not None,
                'orden': sel.orden if sel else None,
                'ig_foto_id': sel.id if sel else None,
            })

        return jsonify(items), 200

    def save_fotos_seleccion(self, request, coleccion_id):
        """Recibe [{fichero_id, orden}, ...] y guarda la selección."""
        data = request.get_json()
        if not isinstance(data, list):
            return jsonify({'message': 'Se espera un array de {fichero_id, orden}'}), 400

        coleccion = Coleccion.query.get(coleccion_id)
        if not coleccion:
            return jsonify({'message': 'Coleccion no encontrada'}), 404

        # Desactivar selecciones existentes
        IgFotoSeleccion.query.filter_by(coleccion_id=coleccion_id).update({'activado': 0})

        for item in data:
            fichero_id = item.get('fichero_id')
            orden = item.get('orden')
            if not fichero_id or orden is None:
                continue

            fichero = Fichero.query.get(fichero_id)
            if not fichero:
                continue

            # Buscar existente o crear
            sel = IgFotoSeleccion.query.filter_by(coleccion_id=coleccion_id, fichero_id=fichero_id).first()
            if sel:
                sel.orden = orden
                sel.activado = True
            else:
                sel = IgFotoSeleccion(coleccion=coleccion, fichero=fichero, orden=orden, activado=True)
                db.session.add(sel)

        db.session.commit()
        return self.get_fotos_seleccion(coleccion_id)

    # ── Token ──────────────────────────────────────────────────────

    def get_token(self):
        token = IgToken.query.filter_by(activado=1).order_by(IgToken.fecha_creacion.desc()).first()
        if not token:
            return jsonify({'access_token': None, 'expires_at': None, 'ig_user_id': None}), 200
        result = self._ig_token_schema.dump(token)
        return jsonify(result), 200

    def save_token(self, request):
        data = request.get_json()
        token = IgToken(
            access_token=data.get('access_token'),
            token_type=data.get('token_type', 'bearer'),
            expires_at=data.get('expires_at'),
            refresh_token=data.get('refresh_token'),
            ig_user_id=data.get('ig_user_id'),
            activado=True
        )
        # Desactivar anteriores
        IgToken.query.update({'activado': False})
        db.session.add(token)
        db.session.commit()
        result = self._ig_token_schema.dump(token)
        return jsonify(result), 200

    # ── Utilidades para el publicador ──────────────────────────────

    def get_pendientes_publicar(self):
        """Devuelve publicaciones listas (estado Publicar/Error y fecha prevista <= ahora o nula)."""
        ahora = self._ahora()
        publicaciones = IgPublicacion.query.filter(
            IgPublicacion.estado.in_(['Publicar', 'Error']),
            db.or_(IgPublicacion.fecha_prevista_publicacion == None,
                   IgPublicacion.fecha_prevista_publicacion <= ahora)
        ).all()

        result = []
        for pub in publicaciones:
            item = self._ig_publicacion_schema.dump(pub)
            coleccion = Coleccion.query.get(pub.coleccion_id)
            if coleccion:
                item['coleccion'] = {
                    'id': coleccion.id,
                    'base': {'id': coleccion.base_id, 'nombre': coleccion.base.nombre if coleccion.base else None},
                    'plataforma': {'nombre': coleccion.plataforma.nombre if coleccion.plataforma else None},
                    'ig': coleccion.ig,
                }

            fotos = IgFotoSeleccion.query\
                .filter(IgFotoSeleccion.coleccion_id == pub.coleccion_id,
                        IgFotoSeleccion.activado == 1)\
                .order_by(IgFotoSeleccion.orden.asc()).all()
            item['fotos_seleccionadas'] = self._ig_fotos_seleccion_schema.dump(fotos)
            result.append(item)

        return jsonify(result), 200

    def marcar_publicado(self, coleccion_id, ig_post_id, ig_permalink=None):
        ahora = self._ahora()
        pub = IgPublicacion.query.filter_by(coleccion_id=coleccion_id).first()
        if pub:
            pub.estado = 'Publicado'
            pub.fecha_ig_publicacion = ahora
            pub.ig_post_id = ig_post_id
            coleccion = Coleccion.query.get(coleccion_id)
            if coleccion:
                coleccion.fecha_ig_publicacion = ahora.date()
                if ig_permalink:
                    coleccion.ig = ig_permalink
            db.session.commit()
        return jsonify({'success': True}), 200

    def marcar_error(self, coleccion_id, error_msg):
        pub = IgPublicacion.query.filter_by(coleccion_id=coleccion_id).first()
        if pub:
            pub.estado = 'Error'
            pub.texto_publicacion = f"{pub.texto_publicacion or ''}\n[ERROR: {error_msg}]"
            db.session.commit()
        return jsonify({'success': True}), 200

    # ── Calendario ──────────────────────────────────────────────────

    def get_calendario(self):
        """Devuelve todas las fechas con publicaciones (previstas o realizadas)."""
        pub_fechas = db.session.query(
            IgPublicacion.fecha_prevista_publicacion,
            IgPublicacion.fecha_ig_publicacion,
            IgPublicacion.estado,
            Coleccion.id
        ).join(Coleccion, IgPublicacion.coleccion_id == Coleccion.id)\
         .filter(Coleccion.activado == 1)\
         .filter(IgPublicacion.estado != 'Descartado')

        col_fechas = db.session.query(
            Coleccion.fecha_ig_publicacion,
            Coleccion.estado_general_id,
            Coleccion.id
        ).outerjoin(IgPublicacion, Coleccion.id == IgPublicacion.coleccion_id)\
         .filter(Coleccion.activado == 1, Coleccion.fecha_ig_publicacion != None)\
         .filter(db.or_(IgPublicacion.id == None, IgPublicacion.estado != 'Descartado'))

        fechas = {}
        for prevista, ig_pub, estado, col_id in pub_fechas.all():
            for f in [prevista, ig_pub]:
                if not f:
                    continue
                dia = f.strftime('%Y-%m-%d') if not isinstance(f, str) else f[:10]
                if dia not in fechas:
                    fechas[dia] = {'prevista': 0, 'publicada': 0, 'ids': []}
                if estado == 'Publicado':
                    fechas[dia]['publicada'] += 1
                else:
                    fechas[dia]['prevista'] += 1
                if col_id not in fechas[dia]['ids']:
                    fechas[dia]['ids'].append(col_id)

        for f, _, col_id in col_fechas.all():
            dia = f.strftime('%Y-%m-%d') if not isinstance(f, str) else f[:10]
            if dia not in fechas:
                fechas[dia] = {'prevista': 0, 'publicada': 0, 'ids': []}
            fechas[dia]['publicada'] += 1
            if col_id not in fechas[dia]['ids']:
                fechas[dia]['ids'].append(col_id)

        return jsonify({dia: fechas[dia] for dia in sorted(fechas.keys())}), 200

    # ── IA ──────────────────────────────────────────────────────────

    def generar_descripcion_ia(self, request):
        data = request.get_json()
        nombre = data.get('nombre', '')
        plataforma = data.get('plataforma', '')
        tipo = data.get('tipo', '')

        if not nombre:
            return jsonify({'error': 'Falta el nombre del juego'}), 400

        prompt = f"""Eres un experto en videojuegos y coleccionismo. Genera contenido para una publicación de Instagram sobre el siguiente juego:

Nombre: {nombre}
Plataforma: {plataforma}
Tipo: {tipo}

Dame dos cosas:

1. IA: Un dato curioso o interesante sobre este juego (2-3 líneas, estilo divulgativo y ameno, en español). Si es un juego poco conocido, explica brevemente de qué trata primero.

2. Una lista de hashtags relevantes para Instagram (entre 12 y 20) en una sola línea, sin etiquetas ni prefijos. Incluye siempre:
   - El nombre del juego como hashtag (ej: #TheLegendOfZelda)
   - La plataforma (#Nintendo, #PlayStation, #Xbox, #Switch, #PS5, #PS4, #GameBoy, #NES, #SNES, #MegaDrive, etc.)
   - Géneros del juego (#Acción, #Aventura, #RPG, #RTS, #Shooter, #Plataformas, #Estrategia, etc.)
   - Coleccionismo (#Videojuegos, #Coleccionismo, #RetroGaming, #Gaming, #GameCollector, etc.)

Formatea la respuesta EXACTAMENTE así:
IA:
(texto de la curiosidad)

#tag1 #tag2 #tag3 ..."""

        try:
            import requests as _req

            _config = ConfigParser()
            api_key = _config.get_value('gemini_api_key')
            url = f'https://generativelanguage.googleapis.com/v1/models/gemini-3.1-flash-lite:generateContent?key={api_key}'

            payload = {
                'contents': [{
                    'parts': [{'text': prompt}]
                }]
            }

            r = _req.post(url, json=payload, timeout=30)
            resp = r.json()

            if r.status_code != 200:
                err_info = resp.get('error', {})
                msg = err_info.get('message', r.text)
                if r.status_code == 429:
                    detalles = err_info.get('details', [])
                    retry = ''
                    for d in detalles:
                        md = d.get('metadata', {})
                        if 'quotaLocation' in md:
                            retry = f" (servicio: {md['quotaLocation']})"
                    return jsonify({'error': f'Límite de uso gratuito alcanzado{retry}. Esperá 1 minuto y reintentá.\n{msg[:200]}'}), 429
                return jsonify({'error': f'Error de Gemini ({r.status_code}): {msg[:300]}'}), 500

            candidates = resp.get('candidates', [])
            if candidates:
                text = candidates[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                if text:
                    return jsonify({'texto': text.strip()}), 200

            return jsonify({'error': 'Gemini no devolvió texto'}), 500

        except Exception as e:
            return jsonify({'error': f'Error al generar: {str(e)[:300]}'}), 500
