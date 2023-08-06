from flask import jsonify
from app.utils.datos import db
from app.model.base_model import Base
from app.model.base_plataforma_model import BasePlataforma, BasePlataformaSchema
from app.model.plataforma_model import Plataforma


class BasePlataformaService:
    _base_plataforma_schema = BasePlataformaSchema()
    _bases_plataforma_schema = BasePlataformaSchema(many=True)

    def get_bases_plataforma(self, request):
        bases = BasePlataforma.query
        if request.args:
            if request.args.get('base_id'):
                bases = bases.filter(BasePlataforma.base_id == request.args.get('base_id'))
            else:
                return jsonify({'message': 'Base no encontrada en filtro'}), 404
        else:
            return jsonify({'message': 'Filtro no encontrado'}), 404
        bases = (bases.join(BasePlataforma.plataforma).join(BasePlataforma.base)
                 .order_by(Plataforma.nombre.asc(), Plataforma.corto.asc(), Base.nombre.asc()).all())
        result = self._bases_plataforma_schema.dump(bases)
        return jsonify(result), 200

    def get_base_plataforma_by_id(self, id):
        base = BasePlataforma.query.get(id)
        result = self._base_plataforma_schema.dump(base)
        return jsonify(result), 200

    def add_base_plataforma(self, request):
        data = request.get_json()
        if 'base' not in data:
            return jsonify({'message': 'Base no encontrada'}), 404
        if 'plataforma' not in data:
            return jsonify({'message': 'Plataforma no encontrada'}), 404

        base = Base.query.get(data['base'])
        if not base:
            return jsonify({'message': 'Base no encontrada'}), 404
        plataforma = Plataforma.query.get(data['plataforma'])
        if not plataforma:
            return jsonify({'message': 'Plataforma no encontrada'}), 404
        baseplata = BasePlataforma(base=base, plataforma=plataforma)
        if 'fecha' in data:
            baseplata.fecha = data['fecha']

        db.session.add(baseplata)
        db.session.commit()
        base_dict = self._base_plataforma_schema.dump(baseplata)
        return jsonify(base_dict), 200

    def delete_base_plataforma_by_id(self, id):
        base = BasePlataforma.query.get(id)
        if base:
            db.session.delete(base)
            db.session.commit()
            return jsonify({'message': 'Base plataforma eliminada correctamente'})
        else:
            return jsonify({'message': 'No se encontró la base plataforma con el ID proporcionado'}), 404