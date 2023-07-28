from flask import jsonify
from app.utils.datos import db
from app.model.coleccion_model import Coleccion, ColeccionSchema
from app.model.estado_model import Estado
from app.model.idioma_model import Idioma
from app.model.juego_model import Juego
from app.model.plataforma_model import Plataforma
from app.model.region_model import Region
from app.model.tienda_model import Tienda


class ColeccionService:
    _coleccion_schema = ColeccionSchema()
    _colecciones_schema = ColeccionSchema(many=True)

    def get_colecciones(self):
        colecciones = Coleccion.query.join(Coleccion.plataforma).join(Coleccion.juego).order_by(Plataforma.nombre.asc(), Plataforma.corto.asc(), Juego.nombre.asc()).all()
        result = self._colecciones_schema.dump(colecciones)
        return jsonify(result), 200

    def get_coleccion_by_id(self, id):
        coleccion = Coleccion.query.get(id)
        if not coleccion:
            return jsonify({'message': 'Colección no encontrada'}), 404
        result = self._coleccion_schema.dump(coleccion)
        return jsonify(result), 200

    def get_colecciones_by_nombre(self, nombre):
        colecciones = db.session.query(Coleccion).join(Juego).filter(Juego.nombre.ilike(f'%{nombre}%')).join(Coleccion.plataforma).join(Coleccion.juego).order_by(Plataforma.nombre.asc(), Plataforma.corto.asc(), Juego.nombre.asc()).all()
        result = self._colecciones_schema.dump(colecciones)
        return jsonify(result), 200

    def add_coleccion(self, request):
        data = request.get_json()

        if 'juego' not in data or data['juego']['id'] is None or 'plataforma' not in data or data['plataforma']['id'] is None:
            return jsonify({'message': 'Juego o plataforma no encontrado'}), 404
        juego = Juego.query.get(data['juego']['id'])
        if juego is None:
            return jsonify({'message': 'Juego no encontrado'}), 404
        plataforma = Plataforma.query.get(data['plataforma']['id'])
        if plataforma is None:
            return jsonify({'message': 'Plataforma no encontrada'}), 404

        coleccion = Coleccion(juego=juego, plataforma=plataforma)

        if 'idioma' in data and data['idioma']['id']:
            coleccion.idioma = Idioma.query.get(data['idioma']['id'])
        if 'region' in data and data['region']['id']:
            coleccion.region = Region.query.get(data['region']['id'])
        if 'estado_general' in data and data['estado_general']['id']:
            coleccion.estado_general = Estado.query.get(data['estado_general']['id'])
        if 'estado_caja' in data and data['estado_caja']['id']:
            coleccion.estado_caja = Estado.query.get(data['estado_caja']['id'])
        if 'fecha_compra' in data:
            coleccion.fecha_compra = data['fecha_compra']
        if 'fecha_recibo' in data:
            coleccion.fecha_recibo = data['fecha_recibo']
        if 'coste' in data:
            coleccion.coste = data['coste']
        if 'tienda' in data and data['tienda']['id']:
            coleccion.tienda = Tienda.query.get(data['tienda']['id'])
        if 'notas' in data:
            coleccion.notas = data['notas']

        db.session.add(coleccion)
        db.session.commit()
        coleccion_dict = self._coleccion_schema.dump(coleccion)
        return jsonify(coleccion_dict), 200

    def update_coleccion(self, request, id):
        data = request.get_json()
        print (data)
        coleccion = Coleccion.query.get(id)

        if not coleccion:
            return jsonify({'message': 'Colección no encontrada'}), 404

        if 'juego' in data and data['juego']['id']:
            if coleccion.juego is None or not coleccion.juego.id == data['juego']['id']:
                coleccion.juego = Juego.query.get(data['juego']['id'])
        if 'plataforma' in data and data['plataforma']['id']:
            if coleccion.plataforma is None or not coleccion.plataforma.id == data['plataforma']['id']:
                coleccion.plataforma = Plataforma.query.get(data['plataforma']['id'])
        if 'idioma' in data and data['idioma']['id']:
            if coleccion.idioma is None or not coleccion.idioma.id == data['idioma']['id']:
                coleccion.idioma = Idioma.query.get(data['idioma']['id'])
        else:
            coleccion.idioma = None
        if 'region' in data and data['region']['id']:
            if coleccion.region is None or not coleccion.region.id == data['region']['id']:
                coleccion.region = Region.query.get(data['region']['id'])
        else:
            coleccion.region = None
        if 'estado_general' in data and data['estado_general']['id']:
            if coleccion.estado_general is None or not coleccion.estado_general.id == data['estado_general']['id']:
                coleccion.estado_general = Estado.query.get(data['estado_general']['id'])
        else:
            coleccion.estado_general = None
        if 'estado_caja' in data and data['estado_caja']['id']:
            if coleccion.estado_caja is None or not coleccion.estado_caja.id == data['estado_caja']['id']:
                coleccion.estado_caja = Estado.query.get(data['estado_caja']['id'])
        else:
            coleccion.estado_caja = None
        if 'fecha_compra' in data and not data['fecha_compra'] == '':
            coleccion.fecha_compra = data['fecha_compra']
        else:
            coleccion.fecha_compra = None
        if 'fecha_recibo' in data and not data['fecha_recibo'] == '':
            coleccion.fecha_recibo = data['fecha_recibo']
        else:
            coleccion.fecha_recibo = None
        if 'coste' in data and not data['coste'] == '':
            coleccion.coste = data['coste']
        else:
            coleccion.coste = None
        if 'tienda' in data and data['tienda']['id']:
            if coleccion.tienda is None or not coleccion.tienda.id == data['tienda']['id']:
                coleccion.tienda = Tienda.query.get(data['tienda']['id'])
        else:
            coleccion.tienda = None
        coleccion.notas = request.json['notas']
        if 'notas' in data and not data['notas'] == '':
            coleccion.notas = data['notas']
        else:
            coleccion.notas = None

        db.session.commit()
        coleccion_dict = self._coleccion_schema.dump(coleccion)
        return jsonify(coleccion_dict), 200