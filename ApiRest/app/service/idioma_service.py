from flask import jsonify
from app.model.idioma_model import Idioma, IdiomaSchema


class IdiomaService:
    _idiomas_schema = IdiomaSchema(many=True)

    def get_idiomas(self):
        idiomas = Idioma.query.order_by(Idioma.descripcion.asc()).all()
        result = self._idiomas_schema.dump(idiomas)
        return jsonify(result), 200
