from flask import jsonify
from app.model.tienda_model import Tienda, TiendaSchema


class TiendaService:
    _tienda_schema = TiendaSchema()
    _tiendas_schema = TiendaSchema(many=True)

    def get_tiendas(self):
        tiendas = Tienda.query.order_by(Tienda.nombre.asc()).all()
        result = self._tiendas_schema.dump(tiendas)
        return jsonify(result), 200
