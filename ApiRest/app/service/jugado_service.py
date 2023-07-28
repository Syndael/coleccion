from flask import jsonify
from app.utils.datos import db
from app.model.estado_model import Estado
from app.model.juego_model import Juego
from app.model.jugado_model import Jugado, JugadoSchema
from app.model.plataforma_model import Plataforma


class JugadoService:
    _jugado_schema = JugadoSchema()
    _jugados_schema = JugadoSchema(many=True)

    def get_jugados(self):
        jugados = Jugado.query.join(Jugado.plataforma).join(Jugado.juego).order_by(Plataforma.nombre.asc(), Plataforma.corto.asc(), Juego.nombre.asc()).all()
        result = self._jugados_schema.dump(jugados)
        return jsonify(result), 200

    def get_jugado_by_id(self, id):
        jugado = Jugado.query.get(id)
        if not jugado:
            return jsonify({'message': 'Historial no encontrado'}), 404
        result = self._jugado_schema.dump(jugado)
        return jsonify(result), 200


    def add_jugado(self, request):
        data = request.get_json()

        if 'juego' not in data or data['juego']['id'] is None or 'plataforma' not in data or data['plataforma']['id'] is None:
            return jsonify({'message': 'Juego o plataforma no encontrado'}), 404
        juego = Juego.query.get(data['juego']['id'])
        if juego is None:
            return jsonify({'message': 'Juego no encontrado'}), 404
        plataforma = Plataforma.query.get(data['plataforma']['id'])
        if plataforma is None:
            return jsonify({'message': 'Plataforma no encontrada'}), 404

        jugado = Jugado(juego=juego, plataforma=plataforma)

        if 'estado_jugado' in data and data['estado_jugado']['id']:
            jugado.estado_jugado = Estado.query.get(data['estado_jugado']['id'])
        if 'porcentaje' in data:
            jugado.porcentaje = data['porcentaje']
        if 'horas' in data:
            jugado.horas = data['horas']
        if 'historia_completa' in data:
            jugado.historia_completa = data['historia_completa']
        if 'notas' in data:
            jugado.notas = data['notas']
        if 'fecha_inicio' in data:
            jugado.fecha_inicio = data['fecha_inicio']
        if 'fecha_fin' in data:
            jugado.fecha_fin = data['fecha_fin']

        db.session.add(jugado)
        db.session.commit()
        jugado_dict = self._jugado_schema.dump(jugado)
        return jsonify(jugado_dict), 200

    def update_jugado(self, request, id):
        data = request.get_json()
        jugado = Jugado.query.get(id)

        if not jugado:
            return jsonify({'message': 'Historial no encontrado'}), 404

        if 'estado_jugado' in data and data['estado_jugado']['id']:
            if jugado.estado_jugado is None or not jugado.estado_jugado.id == data['estado_jugado']['id']:
                jugado.estado_jugado = Estado.query.get(data['estado_jugado']['id'])
        else:
            jugado.estado_jugado = None
        if 'juego' in data and data['juego']['id']:
            if jugado.juego is None or not jugado.juego.id == data['juego']['id']:
                jugado.juego = Juego.query.get(data['juego']['id'])
        if 'plataforma' in data and data['plataforma']['id']:
            if jugado.plataforma is None or not jugado.plataforma.id == data['plataforma']['id']:
                jugado.plataforma = Plataforma.query.get(data['plataforma']['id'])
        if 'porcentaje' in data and not data['porcentaje'] == '':
            jugado.porcentaje = data['porcentaje']
        else:
            jugado.porcentaje = None
        if 'horas' in data and not data['horas'] == '':
            jugado.horas = data['horas']
        else:
            jugado.horas = None
        if 'historia_completa' in data and not data['historia_completa'] == '':
            jugado.historia_completa = data['historia_completa']
        else:
            jugado.historia_completa = None
        if 'notas' in data and not data['notas'] == '':
            jugado.notas = data['notas']
        else:
            jugado.notas = None
        if 'fecha_inicio' in data and not data['fecha_inicio'] == '':
            jugado.fecha_inicio = data['fecha_inicio']
        else:
            jugado.fecha_inicio = None
        if 'fecha_fin' in data and not data['fecha_fin'] == '':
            jugado.fecha_fin = data['fecha_fin']
        else:
            jugado.fecha_fin = None

        db.session.commit()
        jugado_dict = self._jugado_schema.dump(jugado)
        return jsonify(jugado_dict), 200
