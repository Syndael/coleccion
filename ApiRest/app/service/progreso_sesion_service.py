from flask import jsonify

from app.model.base_dlc_model import BaseDlc
from app.model.progreso_model import Progreso
from app.model.progreso_sesion_model import ProgresoSesion, ProgresoSesionSchema
from app.utils.datos import db


class ProgresoSesionService:
    _progreso_sesion_schema = ProgresoSesionSchema()
    _progreso_sesiones_schema = ProgresoSesionSchema(many=True)

    def get_sesiones(self, request):
        sesiones = ProgresoSesion.query.join(ProgresoSesion.progreso)
        if request.args:
            if request.args.get('progreso_id'):
                sesiones = sesiones.filter(ProgresoSesion.progreso_id == request.args.get('progreso_id'))

        result = self._progreso_sesiones_schema.dump(sesiones)
        return jsonify(result), 200

    def add_sesion(self, request):
        data = request.get_json()

        if 'progreso' not in data or data['progreso']['id'] is None:
            return jsonify({'message': 'Progreso no especificado'}), 404

        progreso = Progreso.query.get(data['progreso']['id'])
        if progreso is None:
            return jsonify({'message': 'Progreso no encontrado'}), 404

        sesion = ProgresoSesion(progreso=progreso)

        if 'base_dlc' in data:
            base_dlc = BaseDlc.query.get(data['base_dlc']['id'])
            if base_dlc is not None:
                sesion.base_dlc = base_dlc
        if 'fecha_inicio' in data:
            sesion.fecha_inicio = data['fecha_inicio']
        if 'fecha_fin' in data:
            sesion.fecha_fin = data['fecha_fin']
        if 'horas' in data:
            sesion.horas = data['horas']
        if 'notas' in data:
            sesion.notas = data['notas']

        db.session.add(sesion)
        db.session.commit()
        sesion_dict = self._progreso_sesion_schema.dump(sesion)
        return jsonify(sesion_dict), 200

    def update_sesion(self, request, id):
        data = request.get_json()
        sesion = ProgresoSesion.query.get(id)

        if not sesion:
            return jsonify({'message': 'Sesion no encontrada'}), 404

        if 'progreso' in data and data['progreso']['id']:
            if sesion.progreso is None or not sesion.progreso.id == data['progreso']['id']:
                sesion.progreso = Progreso.query.get(data['progreso']['id'])

        if 'base_dlc' in data and data['base_dlc'] and data['base_dlc']['id']:
            if sesion.base_dlc is None or not sesion.base_dlc.id == data['base_dlc']['id']:
                sesion.base_dlc = BaseDlc.query.get(data['base_dlc']['id'])
        else:
            sesion.base_dlc = None


        if 'fecha_inicio' in data and not data['fecha_inicio'] == '':
            sesion.fecha_inicio = data['fecha_inicio']
        else:
            sesion.fecha_inicio = None
        if 'fecha_fin' in data and not data['fecha_fin'] == '':
            sesion.fecha_fin = data['fecha_fin']
        else:
            sesion.fecha_fin = None
        if 'horas' in data and not data['horas'] == '':
            sesion.horas = data['horas']
        else:
            sesion.horas = None
        if 'fecha_h_inicio' in data and not data['fecha_h_inicio'] == '':
            sesion.fecha_h_inicio = data['fecha_h_inicio']
        else:
            sesion.fecha_h_inicio = None
        if 'fecha_h_fin' in data and not data['fecha_h_fin'] == '':
            sesion.fecha_h_fin = data['fecha_h_fin']
        else:
            sesion.fecha_h_fin = None
        if 'horas_h' in data and not data['horas_h'] == '':
            sesion.horas_h = data['horas_h']
        else:
            sesion.horas_h = None
        if 'notas' in data and not data['notas'] == '':
            sesion.notas = data['notas']
        else:
            sesion.notas = None

        db.session.commit()
        sesion_dict = self._progreso_sesion_schema.dump(sesion)
        return jsonify(sesion_dict), 200

    def delete_sesion_by_id(self, id):
        sesion = ProgresoSesion.query.get(id)
        if sesion:
            try:
                db.session.delete(sesion)
                db.session.commit()
                return {'success': True}
            except:
                db.session.rollback()
                return {'success': False}

        return {'success': False}
