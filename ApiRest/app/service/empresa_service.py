from flask import jsonify
from app.model.empresa_model import Empresa, EmpresaSchema


class EmpresaService:
    _empresa_schema = EmpresaSchema()
    _empresas_schema = EmpresaSchema(many=True)

    def get_empresas(self):
        empresas = Empresa.query.order_by(Empresa.nombre.asc()).all()
        result = self._empresas_schema.dump(empresas)
        return jsonify(result), 200
