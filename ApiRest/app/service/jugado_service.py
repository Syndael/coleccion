from flask import jsonify
from app.model.jugado_model import Jugado, JugadoSchema
from app.model.juego_model import Juego
from app.model.plataforma_model import Plataforma


class JugadoService:
    _jugado_schema = JugadoSchema(many=True)

    def get_jugados(self):
        jugados = Jugado.query.join(Jugado.plataforma).join(Jugado.juego).order_by(Plataforma.nombre.asc(), Plataforma.corto.asc(), Juego.nombre.asc()).all()
        result = self._jugado_schema.dump(jugados)
        return jsonify(result)

    def get_jugado_by_id(self, id):
        jugados = Jugado.query.filter(Jugado.id == id).join(Jugado.plataforma).join(Jugado.juego).order_by(Plataforma.nombre.asc(), Plataforma.corto.asc(), Juego.nombre.asc()).all()
        result = self._jugado_schema.dump(jugados)
        return jsonify(result)
