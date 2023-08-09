from flask import jsonify
from app.model.region_model import Region, RegionSchema


class RegionService:
    _regiones_schema = RegionSchema(many=True)

    def get_regiones(self):
        regiones = Region.query.order_by(Region.descripcion.asc()).all()
        result = self._regiones_schema.dump(regiones)
        return jsonify(result), 200
