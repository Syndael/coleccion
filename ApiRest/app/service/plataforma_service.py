from flask import jsonify
from app.model.plataforma_model import Plataforma, PlataformaSchema


class PlataformaService:
    _plataformas_schema = PlataformaSchema(many=True)

    def get_plataformas(self):
        plataformas = Plataforma.query.order_by(Plataforma.nombre.asc()).all()
        result = self._plataformas_schema.dump(plataformas)
        return jsonify(result), 200
