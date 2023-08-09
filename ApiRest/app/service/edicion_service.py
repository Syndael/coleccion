from flask import jsonify
from app.utils.datos import db
from app.model.base_model import Base
from app.model.edicion_model import Edicion, EdicionSchema
from app.model.plataforma_model import Plataforma


class EdicionService:
    _edicion_schema = EdicionSchema()
    _ediciones_schema = EdicionSchema(many=True)

    def get_ediciones(self, request):
        ediciones = Edicion.query
        if request.args:
            if request.args.get('base_id'):
                ediciones = ediciones.filter(Edicion.base_id == request.args.get('base_id'))
            else:
                return jsonify({'message': 'Base no encontrada en filtro'}), 404
        else:
            return jsonify({'message': 'Filtro no encontrado'}), 404
        ediciones = ediciones.join(Edicion.base).order_by(Edicion.nombre.asc()).all()
        result = self._ediciones_schema.dump(ediciones)
        return jsonify(result), 200

    def get_edicion_by_id(self, id):
        edicion = Edicion.query.get(id)
        result = self._edicion_schema.dump(edicion)
        return jsonify(result), 200

    def add_edicion(self, request):
        data = request.get_json()
        if 'base' not in data:
            return jsonify({'message': 'Base no encontrada'}), 404
        if 'nombre' not in data:
            return jsonify({'message': 'Nombre no encontrado'}), 404

        base = Base.query.get(data['base'])
        if not base:
            return jsonify({'message': 'Base no encontrada'}), 404
        edicion = Edicion(base=base, nombre=data['nombre'])

        if 'plataforma' in data:
            plataforma = Plataforma.query.get(data['plataforma'])
            if plataforma:
                edicion.plataforma = plataforma
        if 'fecha' in data:
            edicion.fecha = data['fecha']

        db.session.add(edicion)
        db.session.commit()
        edicion_dict = self._edicion_schema.dump(edicion)
        return jsonify(edicion_dict), 200

    def delete_edicion_by_id(self, id):
        edicion = Edicion.query.get(id)
        if edicion:
            db.session.delete(edicion)
            db.session.commit()
            return jsonify({'message': 'Edición eliminada correctamente'})
        else:
            return jsonify({'message': 'No se encontró la edcición con el ID proporcionado'}), 404
