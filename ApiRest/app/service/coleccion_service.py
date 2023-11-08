from flask import jsonify
from sqlalchemy import or_, case

from app.model.base_model import Base
from app.model.coleccion_model import Coleccion, ColeccionSchema
from app.model.edicion_model import Edicion
from app.model.estado_model import Estado
from app.model.idioma_model import Idioma
from app.model.plataforma_model import Plataforma
from app.model.region_model import Region
from app.model.tienda_model import Tienda
from app.model.tipo_base_model import TipoBase
from app.utils.datos import db


class ColeccionService:
    _coleccion_schema = ColeccionSchema()
    _colecciones_schema = ColeccionSchema(many=True)

    def get_colecciones(self, request):
        colecciones = Coleccion.query.join(Coleccion.plataforma).join(Coleccion.base).join(Base.tipo_base)
        orden_seleccionado = None
        if request.args:
            if request.args.get('id'):
                colecciones = colecciones.filter(Coleccion.id == request.args.get('id'))
            if request.args.get('tipo_base_id'):
                colecciones = colecciones.filter(Base.tipo_id == request.args.get('tipo_base_id'))
            if request.args.get('plataforma_id'):
                colecciones = colecciones.filter(Coleccion.plataforma_id == request.args.get('plataforma_id'))
            if request.args.get('plataforma'):
                colecciones = colecciones.filter(or_(Plataforma.nombre == request.args.get('plataforma'), Plataforma.corto == request.args.get('plataforma')))
            if request.args.get('nombre'):
                nombre = request.args.get('nombre')
                colecciones = colecciones.filter(Base.nombre.ilike(f'%{nombre}%'))
            if request.args.get('saga'):
                saga = request.args.get('saga')
                colecciones = colecciones.filter(Base.saga.ilike(f'%{saga}%'))
            if request.args.get('estado_gen_id'):
                colecciones = colecciones.filter(Coleccion.estado_general_id == request.args.get('estado_gen_id'))
            if request.args.get('tienda_id'):
                colecciones = colecciones.filter(Coleccion.tienda_id == request.args.get('tienda_id'))
            if request.args.get('orden'):
                orden_seleccionado = request.args.get('orden')

        colecciones = colecciones.filter(Coleccion.activado == 1)
        if orden_seleccionado == 'Pokémon':
            colecciones = colecciones.order_by(TipoBase.descripcion.asc(), Plataforma.nombre.asc(),
                                               case((Base.saga == "Pokémon", Base.fecha_salida), else_=1).asc(), Plataforma.corto.asc(),
                                               Base.nombre.asc()).all()
        elif orden_seleccionado == 'Colección':
            colecciones = colecciones.join(Coleccion.estado_general)
            estados_descripcion_excluidos = ['Buscado', 'Digital', 'N/A', 'Pedido', 'Reservado']
            colecciones = colecciones.filter(Estado.descripcion.notin_(estados_descripcion_excluidos))
            colecciones = colecciones.order_by(TipoBase.descripcion.asc(), Plataforma.nombre.asc(),
                                               case((Base.saga == "Pokémon", Base.fecha_salida), else_=1).asc(), Plataforma.corto.asc(),
                                               Base.nombre.asc()).all()
        elif orden_seleccionado == 'En curso':
            colecciones = colecciones.join(Coleccion.estado_general)
            estados_descripcion_incluidos = ['Pedido', 'Reservado']
            colecciones = colecciones.filter(Estado.descripcion.in_(estados_descripcion_incluidos))
            colecciones = colecciones.order_by(TipoBase.descripcion.asc(), Plataforma.nombre.asc(),
                                               Plataforma.corto.asc(), Base.nombre.asc()).all()
        elif orden_seleccionado == 'Compras':
            colecciones = colecciones.join(Coleccion.estado_general)
            estados_descripcion_excluidos = ['Buscado', 'N/A']
            colecciones = colecciones.filter(Estado.descripcion.notin_(estados_descripcion_excluidos))
            colecciones = colecciones.order_by(Coleccion.fecha_compra.desc(), Base.nombre.asc()).all()
        elif orden_seleccionado == 'IG':
            colecciones = colecciones.join(Coleccion.estado_general)
            estados_descripcion_excluidos = ['Buscado', 'Digital', 'N/A', 'Pedido', 'Reservado']
            colecciones = colecciones.filter(Estado.descripcion.notin_(estados_descripcion_excluidos))
            colecciones = colecciones.order_by(case((Coleccion.ig.isnot(None), 0), else_=1), TipoBase.descripcion.asc(), Plataforma.nombre.asc(),
                                               Plataforma.corto.asc(), Base.nombre.asc()).all()
        elif orden_seleccionado == 'telegram':
            colecciones = colecciones.join(Coleccion.estado_general)
            estados_descripcion_excluidos = ['Buscado', 'N/A']
            colecciones = colecciones.filter(Estado.descripcion.notin_(estados_descripcion_excluidos))
            colecciones = colecciones.order_by(Plataforma.nombre.asc(), Base.nombre.asc()).all()
        else:
            colecciones = colecciones.order_by(TipoBase.descripcion.asc(), Plataforma.nombre.asc(),
                                               Plataforma.corto.asc(), Base.nombre.asc()).all()

        result = self._colecciones_schema.dump(colecciones)
        return jsonify(result), 200

    def get_coleccion_by_id(self, id):
        coleccion = Coleccion.query.get(id)
        if not coleccion:
            return jsonify({'message': 'Colección no encontrada'}), 404
        result = self._coleccion_schema.dump(coleccion)
        return jsonify(result), 200

    def get_colecciones_by_nombre(self, nombre):
        colecciones = db.session.query(Coleccion).join(Base).filter(Base.nombre.ilike(f'%{nombre}%'),
                                                                    Coleccion.activado == 1).join(
            Coleccion.plataforma).join(Coleccion.base).order_by(Plataforma.nombre.asc(), Plataforma.corto.asc(),
                                                                Base.nombre.asc()).all()
        result = self._colecciones_schema.dump(colecciones)
        return jsonify(result), 200

    def add_coleccion(self, request):
        data = request.get_json()

        if 'base' not in data or data['base']['id'] is None or 'plataforma' not in data or data['plataforma'][
            'id'] is None:
            return jsonify({'message': 'Base o plataforma no encontrado'}), 404
        base = Base.query.get(data['base']['id'])
        if base is None:
            return jsonify({'message': 'Base no encontrado'}), 404
        plataforma = Plataforma.query.get(data['plataforma']['id'])
        if plataforma is None:
            return jsonify({'message': 'Plataforma no encontrada'}), 404

        coleccion = Coleccion(base=base, plataforma=plataforma)

        if 'edicion' in data and data['edicion']['id']:
            coleccion.edicion = Edicion.query.get(data['edicion']['id'])
        if 'idioma' in data and data['idioma']['id']:
            coleccion.idioma = Idioma.query.get(data['idioma']['id'])
        if 'region' in data and data['region']['id']:
            coleccion.region = Region.query.get(data['region']['id'])
        if 'estado_general' in data and data['estado_general']['id']:
            coleccion.estado_general = Estado.query.get(data['estado_general']['id'])
        if 'estado_caja' in data and data['estado_caja']['id']:
            coleccion.estado_caja = Estado.query.get(data['estado_caja']['id'])
        if 'fecha_reserva' in data:
            coleccion.fecha_reserva = data['fecha_reserva']
        if 'fecha_compra' in data:
            coleccion.fecha_compra = data['fecha_compra']
        if 'fecha_recibo' in data:
            coleccion.fecha_recibo = data['fecha_recibo']
        if 'unidades' in data:
            coleccion.unidades = data['unidades']
        if 'coste' in data:
            coleccion.coste = data['coste']
        if 'tienda' in data and data['tienda']['id']:
            coleccion.tienda = Tienda.query.get(data['tienda']['id'])
        if 'url' in data:
            coleccion.url = data['url']
        if 'ig' in data:
            coleccion.ig = data['ig']
        if 'notas' in data:
            coleccion.notas = data['notas']
        coleccion.activado = 1

        db.session.add(coleccion)
        db.session.commit()
        coleccion_dict = self._coleccion_schema.dump(coleccion)
        return jsonify(coleccion_dict), 200

    def update_coleccion(self, request, id):
        data = request.get_json()
        coleccion = Coleccion.query.get(id)

        if not coleccion:
            return jsonify({'message': 'Colección no encontrada'}), 404

        if 'base' in data and data['base']['id']:
            if coleccion.base is None or not coleccion.base.id == data['base']['id']:
                coleccion.base = Base.query.get(data['base']['id'])
        if 'edicion' in data and data['edicion']['id']:
            if coleccion.edicion is None or not coleccion.edicion.id == data['edicion']['id']:
                coleccion.edicion = Edicion.query.get(data['edicion']['id'])
        else:
            coleccion.edicion = None
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
        if 'fecha_reserva' in data:
            coleccion.fecha_reserva = data['fecha_reserva']
        else:
            coleccion.fecha_reserva = None
        if 'fecha_compra' in data and not data['fecha_compra'] == '':
            coleccion.fecha_compra = data['fecha_compra']
        else:
            coleccion.fecha_compra = None
        if 'fecha_recibo' in data and not data['fecha_recibo'] == '':
            coleccion.fecha_recibo = data['fecha_recibo']
        else:
            coleccion.fecha_recibo = None
        if 'unidades' in data and not data['unidades'] == '':
            coleccion.unidades = data['unidades']
        else:
            coleccion.unidades = None
        if 'coste' in data and not data['coste'] == '':
            coleccion.coste = data['coste']
        else:
            coleccion.coste = None
        if 'tienda' in data and data['tienda']['id']:
            if coleccion.tienda is None or not coleccion.tienda.id == data['tienda']['id']:
                coleccion.tienda = Tienda.query.get(data['tienda']['id'])
        else:
            coleccion.tienda = None
        if 'url' in data and not data['url'] == '':
            coleccion.url = data['url']
        else:
            coleccion.url = None
        if 'ig' in data and not data['ig'] == '':
            coleccion.ig = data['ig']
        else:
            coleccion.ig = None
        if 'notas' in data and not data['notas'] == '':
            coleccion.notas = data['notas']
        else:
            coleccion.notas = None

        db.session.commit()
        coleccion_dict = self._coleccion_schema.dump(coleccion)
        return jsonify(coleccion_dict), 200

    def delete_coleccion_by_id(self, id):
        coleccion = Coleccion.query.get(id)
        if coleccion:
            try:
                db.session.delete(coleccion)
                db.session.commit()
                return {'success': True}
            except:
                db.session.rollback()
                return {'success': False}

        return {'success': False}
