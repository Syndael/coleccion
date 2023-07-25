from flask import jsonify
import json
from app.utils.datos import db
from app.model.juego_model import Juego, JuegoSchema


class JuegoService:
    _juego_schema = JuegoSchema()
    _juegos_schema = JuegoSchema(many=True)

    def get_juegos(self):
        juegos = Juego.query.order_by(Juego.nombre.asc()).all()
        result = self._juegos_schema.dump(juegos)
        return jsonify(result)

    def get_juegos_by_nombre(self, nombre):
        juegos = Juego.query.filter(Juego.nombre.ilike(f'%{nombre}%')).order_by(Juego.nombre.asc()).all()
        result = self._juegos_schema.dump(juegos)
        return jsonify(result)

    def get_juegos_by_id(self, id):
        juego = Juego.query.get(id)
        if not juego:
            return jsonify({'message': 'Juego no encontrado'}), 404
        juego_dict = self._juego_schema.dump(juego)
        return jsonify(juego_dict), 200


    def add_juego(self, request):
        data = request.get_json()
        if 'nombre' not in data:
            return None
        juego = Juego(nombre=data['nombre'])
        if 'saga' in data:
            juego.saga = data['saga']
        if 'fecha_salida' in data:
            juego.fecha_salida = data['fecha_salida']
        db.session.add(juego)
        db.session.commit()

        juego_dict = self._juego_schema.dump(juego)
        juego_json = json.dumps(juego_dict)

        return juego_json

    def update_juego(self, request, id):
        data = request.get_json()
        juego = Juego.query.get(id)

        if not juego:
            return jsonify({'message': 'Juego no encontrado'}), 404

        juego.nombre = data.get('nombre', juego.nombre)
        juego.saga = data.get('saga', juego.saga)
        juego.fecha_salida = data.get('fecha_salida', juego.fecha_salida)

        db.session.commit()

        juego_dict = self._juego_schema.dump(juego)
        return jsonify(juego_dict), 200