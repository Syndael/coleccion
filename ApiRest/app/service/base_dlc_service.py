from flask import jsonify
from app.utils.datos import db
from app.model.base_model import Base
from app.model.base_dlc_model import BaseDlc, BaseDlcSchema


class BaseDlcService:
    _base_dlc_schema = BaseDlcSchema()
    _bases_dlc_schema = BaseDlcSchema(many=True)

    def get_bases_dlc(self, request):
        bases = BaseDlc.query
        if request.args:
            if request.args.get('base_id'):
                bases = bases.filter(BaseDlc.base_id == request.args.get('base_id'))

        bases = bases.order_by(BaseDlc.nombre.asc()).all()
        result = self._bases_dlc_schema.dump(bases)
        return jsonify(result), 200

    def get_base_dlc_by_id(self, id):
        base = BaseDlc.query.get(id)
        result = self._base_dlc_schema.dump(base)
        return jsonify(result), 200

    def add_base_dlc(self, request):
        data = request.get_json()

        if 'base' not in data:
            return jsonify({'message': 'Base no especificada'}), 404

        base = Base.query.get(data['base'])
        if base is None:
            return jsonify({'message': 'Base no encontrada'}), 404

        basedlc = BaseDlc(base=base)
        if 'nombre' in data:
            basedlc.nombre = data['nombre']

        db.session.add(basedlc)
        db.session.commit()
        base_dict = self._base_dlc_schema.dump(basedlc)
        return jsonify(base_dict), 200

    def delete_base_dlc_by_id(self, id):
        basedlc = BaseDlc.query.get(id)
        if basedlc:
            db.session.delete(basedlc)
            db.session.commit()
            return jsonify({'message': 'Base dlc eliminada correctamente'})
        else:
            return jsonify({'message': 'No se encontró la base dlc con el ID proporcionado'}), 404
