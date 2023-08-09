from flask import jsonify
from app.model.tipo_base_model import TipoBase, TipoBaseSchema


class TipoBaseService:
    _tipo_base_schema = TipoBaseSchema()
    _tipos_base_schema = TipoBaseSchema(many=True)

    def get_tipos_base(self):
        tipos = TipoBase.query.order_by(TipoBase.descripcion.asc()).all()
        result = self._tipos_base_schema.dump(tipos)
        return jsonify(result), 200
