from flask import jsonify
from app.utils.datos import db
from app.model.base_model import Base, BaseSchema
from app.model.base_plataforma_model import BasePlataforma
from app.model.tipo_base_model import TipoBase


class BaseService:
    _base_schema = BaseSchema()
    _bases_schema = BaseSchema(many=True)

    def get_bases(self, request):
        bases = Base.query.join(Base.tipo_base)
        if request.args:
            if request.args.get('tipo_base_id'):
                tipo_base_id = request.args.get('tipo_base_id')
                bases = bases.filter(Base.tipo_id == tipo_base_id)
            if request.args.get('tipo_base_descripcion'):
                bases = bases.filter(TipoBase.descripcion == request.args.get('tipo_base_descripcion'))
            if request.args.get('nombre'):
                nombre = request.args.get('nombre')
                bases = bases.filter(Base.nombre.ilike(f'%{nombre}%'))
            if request.args.get('saga'):
                saga = request.args.get('saga')
                bases = bases.filter(Base.saga.ilike(f'%{saga}%'))
            if request.args.get('plataforma_id'):
                plataforma = request.args.get('plataforma_id')
                bases = bases.join(BasePlataforma).filter(BasePlataforma.plataforma_id == plataforma)
        bases = bases.order_by(TipoBase.descripcion.asc(), Base.nombre.asc()).all()
        result = self._bases_schema.dump(bases)
        return jsonify(result), 200

    def get_bases_by_nombre(self, nombre):
        bases = Base.query.filter(Base.nombre.ilike(f'%{nombre}%')).order_by(Base.nombre.asc()).all()
        result = self._bases_schema.dump(bases)
        return jsonify(result), 200

    def get_bases_by_id(self, id):
        base = Base.query.get(id)
        if not base:
            return jsonify({'message': 'Base no encontrado'}), 404
        base_dict = self._base_schema.dump(base)
        return jsonify(base_dict), 200

    def add_base(self, request):
        data = request.get_json()
        if 'tipo_base' not in data or data['tipo_base']['id'] is None:
            return jsonify({'message': 'Tipo no encontrado'}), 404
        tipo = TipoBase.query.get(data['tipo_base']['id'])
        if not tipo:
            return jsonify({'message': 'Tipo no encontrado'}), 404
        if 'nombre' not in data:
            return jsonify({'message': 'Nombre no encontrado'}), 404
        base = Base(tipo_base=tipo, nombre=data['nombre'])
        if 'saga' in data:
            base.saga = data['saga']
        if 'fecha_salida' in data:
            base.fecha_salida = data['fecha_salida']
        db.session.add(base)
        db.session.commit()

        base_dict = self._base_schema.dump(base)
        return jsonify(base_dict), 200

    def update_base(self, request, id):
        data = request.get_json()
        base = Base.query.get(id)

        if not base:
            return jsonify({'message': 'Base no encontrado'}), 404

        if 'tipo_base' in data and data['tipo_base']['id']:
            tipo = TipoBase.query.get(data['tipo_base']['id'])
            base.tipo_base = tipo
        base.nombre = data.get('nombre', base.nombre)
        if 'saga' in data and not data['saga'] == '':
            base.saga = data['saga']
        else:
            base.saga = None
        if 'fecha_salida' in data and not data['fecha_salida'] == '':
            base.fecha_salida = data['fecha_salida']
        else:
            base.fecha_salida = None

        db.session.commit()

        base_dict = self._base_schema.dump(base)
        return jsonify(base_dict), 200

    def delete_base_by_id(self, id):
        base = Base.query.get(id)
        if base:
            try:
                db.session.delete(base)
                db.session.commit()
                return {'success': True}
            except Exception as ex:
                db.session.rollback()
                print(ex)
                return {'success': False}

        return {'success': False}
