from flask import jsonify
from app.model.estado_model import Estado, EstadoSchema


class EstadoService:
    _estado_schema = EstadoSchema()
    _estados_schema = EstadoSchema(many=True)

    def get_estados(self):
        estados = Estado.query.order_by(Estado.tipo.asc(), Estado.descripcion.asc()).all()
        result = self._estados_schema.dump(estados)
        return jsonify(result), 200