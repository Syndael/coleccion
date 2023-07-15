from flask import jsonify
from app.utils.datos import db
from app.model.coleccion_model import Coleccion, ColeccionSchema
from app.model.juego_model import Juego


class ColeccionService:
    _coleccion_schema = ColeccionSchema(many=True)

    def get_colecciones(self):
        colecciones = Coleccion.query.all()
        result = self._coleccion_schema.dump(colecciones)
        return jsonify(result)

    def get_colecciones_by_id(self, id):
        colecciones = Coleccion.query.filter(Coleccion.id == id).all()
        result = self._coleccion_schema.dump(colecciones)
        return jsonify(result)

    def get_colecciones_by_nombre(self, nombre):
        colecciones = db.session.query(Coleccion).join(Juego).filter(Juego.nombre.ilike(f'%{nombre}%')).all()
        result = self._coleccion_schema.dump(colecciones)
        return jsonify(result)

    def add_coleccion(self, request):
        juego_id = request.json['juego_id']
        plataforma_id = request.json['plataforma_id']
        idioma_id = request.json['idioma_id']
        region_id = request.json['region_id']
        estado_general_id = request.json['estado_general_id']
        estado_caja_id = request.json['estado_caja_id']
        fecha_compra = request.json['fecha_compra']
        fecha_recibo = request.json['fecha_recibo']
        coste = request.json['coste']
        tienda_id = request.json['tienda_id']
        notas = request.json['notas']

        juego = Juego.query.get(juego_id)
        nueva_coleccion = Coleccion(juego, plataforma_id, idioma_id, region_id, estado_general_id, estado_caja_id, fecha_compra, fecha_recibo, coste, tienda_id, notas)
        db.session.add(nueva_coleccion)
        db.session.commit()

        return jsonify(nueva_coleccion)

    def update_coleccion(self, request, id):
        coleccion = Coleccion.query.get(id)

        coleccion.juego_id = request.json['juego_id']
        coleccion.plataforma_id = request.json['plataforma_id']
        coleccion.idioma_id = request.json['idioma_id']
        coleccion.region_id = request.json['region_id']
        coleccion.estado_general_id = request.json['estado_general_id']
        coleccion.estado_caja_id = request.json['estado_caja_id']
        coleccion.fecha_compra = request.json['fecha_compra']
        coleccion.fecha_recibo = request.json['fecha_recibo']
        coleccion.coste = request.json['coste']
        coleccion.tienda_id = request.json['tienda_id']
        coleccion.notas = request.json['notas']

        db.session.commit()

        return jsonify(coleccion)

    def delete_coleccion(self, id):
        coleccion = Coleccion.query.get(id)

        db.session.delete(coleccion)
        db.session.commit()

        return jsonify(coleccion)