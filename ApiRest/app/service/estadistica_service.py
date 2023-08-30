from flask import jsonify

from app.model.completo_v_model import Completo, CompletoSchema
from app.model.gasto_v_model import Gasto, GastoSchema


class EstadisticasService:
    _completos_schema = CompletoSchema(many=True)
    _gastos_schema = GastoSchema(many=True)

    def get_completos(self):
        completos = Completo.query.order_by(Completo.mes.desc()).all()
        result = self._completos_schema.dump(completos)
        return jsonify(result), 200

    def get_gastos(self):
        gastos = Gasto.query.order_by(Gasto.tipo.asc(), Gasto.orden_desc.desc(), Gasto.orden_asc.asc()).all()
        result = self._gastos_schema.dump(gastos)
        return jsonify(result), 200
