from flask import jsonify
from app.utils.datos import db
from app.model.estado_model import Estado
from app.model.base_model import Base
from app.model.progreso_model import Progreso, ProgresoSchema
from app.model.plataforma_model import Plataforma


class ProgresoService:
    _progreso_schema = ProgresoSchema()
    _progresos_schema = ProgresoSchema(many=True)

    def get_progresos(self, request):
        progresos = Progreso.query.join(Progreso.estado_progreso).join(Progreso.plataforma).join(Progreso.base)
        if request.args:
            if request.args.get('plataforma_id'):
                progresos = progresos.filter(Progreso.plataforma_id == request.args.get('plataforma_id'))
            if request.args.get('nombre'):
                nombre = request.args.get('nombre')
                progresos = progresos.filter(Base.nombre.ilike(f'%{nombre}%'))
            if request.args.get('saga'):
                saga = request.args.get('saga')
                progresos = progresos.filter(Base.saga.ilike(f'%{saga}%'))
            if request.args.get('estado_id'):
                progresos = progresos.filter(Progreso.estado_progreso_id == request.args.get('estado_id'))
        progresos = progresos.order_by(Estado.orden.asc(), Plataforma.nombre.asc(), Plataforma.corto.asc(),
                                       Base.nombre.asc()).all()
        result = self._progresos_schema.dump(progresos)
        return jsonify(result), 200

    def get_progreso_by_id(self, id):
        progreso = Progreso.query.get(id)
        if not progreso:
            return jsonify({'message': 'Historial no encontrado'}), 404
        result = self._progreso_schema.dump(progreso)
        return jsonify(result), 200

    def add_progreso(self, request):
        data = request.get_json()

        if 'base' not in data or data['base']['id'] is None or 'plataforma' not in data or data['plataforma'][
            'id'] is None:
            return jsonify({'message': 'Base o plataforma no encontrado'}), 404
        base = Base.query.get(data['base']['id'])
        if base is None:
            return jsonify({'message': 'Base no encontrado'}), 404
        plataforma = Plataforma.query.get(data['plataforma']['id'])
        if plataforma is None:
            return jsonify({'message': 'Plataforma no encontrada'}), 404

        progreso = Progreso(base=base, plataforma=plataforma)

        if 'estado_progreso' in data and data['estado_progreso']['id']:
            progreso.estado_progreso = Estado.query.get(data['estado_progreso']['id'])
        if 'porcentaje' in data:
            progreso.porcentaje = data['porcentaje']
        if 'horas' in data:
            progreso.horas = data['horas']
        if 'historia_completa' in data:
            progreso.historia_completa = data['historia_completa']
        if 'notas' in data:
            progreso.notas = data['notas']
        if 'fecha_inicio' in data:
            progreso.fecha_inicio = data['fecha_inicio']
        if 'fecha_fin' in data:
            progreso.fecha_fin = data['fecha_fin']

        db.session.add(progreso)
        db.session.commit()
        progreso_dict = self._progreso_schema.dump(progreso)
        return jsonify(progreso_dict), 200

    def update_progreso(self, request, id):
        data = request.get_json()
        progreso = Progreso.query.get(id)

        if not progreso:
            return jsonify({'message': 'Historial no encontrado'}), 404

        if 'estado_progreso' in data and data['estado_progreso']['id']:
            if progreso.estado_progreso is None or not progreso.estado_progreso.id == data['estado_progreso']['id']:
                progreso.estado_progreso = Estado.query.get(data['estado_progreso']['id'])
        else:
            progreso.estado_progreso = None
        if 'base' in data and data['base']['id']:
            if progreso.base is None or not progreso.base.id == data['base']['id']:
                progreso.base = Base.query.get(data['base']['id'])
        if 'plataforma' in data and data['plataforma']['id']:
            if progreso.plataforma is None or not progreso.plataforma.id == data['plataforma']['id']:
                progreso.plataforma = Plataforma.query.get(data['plataforma']['id'])
        if 'porcentaje' in data and not data['porcentaje'] == '':
            progreso.porcentaje = data['porcentaje']
        else:
            progreso.porcentaje = None
        if 'horas' in data and not data['horas'] == '':
            progreso.horas = data['horas']
        else:
            progreso.horas = None
        if 'historia_completa' in data and not data['historia_completa'] == '':
            progreso.historia_completa = data['historia_completa']
        else:
            progreso.historia_completa = None
        if 'notas' in data and not data['notas'] == '':
            progreso.notas = data['notas']
        else:
            progreso.notas = None
        if 'fecha_inicio' in data and not data['fecha_inicio'] == '':
            progreso.fecha_inicio = data['fecha_inicio']
        else:
            progreso.fecha_inicio = None
        if 'fecha_fin' in data and not data['fecha_fin'] == '':
            progreso.fecha_fin = data['fecha_fin']
        else:
            progreso.fecha_fin = None

        db.session.commit()
        progreso_dict = self._progreso_schema.dump(progreso)
        return jsonify(progreso_dict), 200
