from flask import jsonify
from app.utils.datos import db
from app.model.juego_model import Juego, JuegoSchema


class JuegoService:
    _juego_schema = JuegoSchema()
    _juegos_schema = JuegoSchema(many=True)

    def get_juegos(self, request):
        juegos = Juego.query
        if request.args:
            if request.args.get('nombre'):
                nombre = request.args.get('nombre')
                juegos = juegos.filter(Juego.nombre.ilike(f'%{nombre}%'))
            if request.args.get('saga'):
                saga = request.args.get('saga')
                juegos = juegos.filter(Juego.saga.ilike(f'%{saga}%'))
        juegos = juegos.order_by(Juego.nombre.asc()).all()
        result = self._juegos_schema.dump(juegos)
        return jsonify(result), 200

    def get_juegos_by_nombre(self, nombre):
        juegos = Juego.query.filter(Juego.nombre.ilike(f'%{nombre}%')).order_by(Juego.nombre.asc()).all()
        result = self._juegos_schema.dump(juegos)
        return jsonify(result), 200

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
        return jsonify(juego_dict), 200

    def update_juego(self, request, id):
        data = request.get_json()
        juego = Juego.query.get(id)

        if not juego:
            return jsonify({'message': 'Juego no encontrado'}), 404

        juego.nombre = data.get('nombre', juego.nombre)
        if 'saga' in data and not data['saga'] == '':
            juego.saga = data['saga']
        else:
            juego.saga = None
        if 'fecha_salida' in data and not data['fecha_salida'] == '':
            juego.fecha_salida = data['fecha_salida']
        else:
            juego.fecha_salida = None

        db.session.commit()

        juego_dict = self._juego_schema.dump(juego)
        return jsonify(juego_dict), 200