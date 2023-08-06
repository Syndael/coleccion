import uuid
import os
from flask import jsonify, send_from_directory
from app.model.coleccion_model import Coleccion
from app.model.fichero_model import Fichero, FicheroSchema, DatoFichero, DatoFicheroSchema
from app.model.tipo_fichero_model import TipoFichero
from app.utils import constantes
from app.utils.datos import db
from app.utils.config_parser_utils import ConfigParser


_config = ConfigParser()


class FicheroService:
    _path = _config.get_value(constantes.PATH_FILES)
    _fichero_schema = FicheroSchema()
    _ficheros_schema = FicheroSchema(many=True)
    _datofichero_schema = DatoFicheroSchema()
    _datosfichero_schema = DatoFicheroSchema(many=True)

    def _almacenar(self, fichero, ruta, nombre):
        self._crear_ruta(ruta)
        try:
            ruta = os.path.join(ruta, nombre)
            fichero.save(ruta)
        except IOError:
            return {'mensaje': 'Se ha producido un error almacenando el fichero'}, 500

        return None

    def _crear_ruta(self, ruta):
        try:
            os.makedirs(ruta)
        except FileExistsError:
            return {'mensaje': 'Se ha producido un error generando las rutas internas de los ficheros'}, 500

    def get_fichero(self, id):
        fichero = Fichero.query.get(id)
        if not fichero:
            return {'mensaje': 'No se ha encontrado ningún fichero con ese id'}, 404
        elif fichero.activado:
            return send_from_directory(fichero.ruta, fichero.nombre_almacenado)
        else:
            return {'mensaje': 'El fichero fue eliminado'}, 404

    def get_datos_ficheros(self, id):
        if id:
            ficheros = Fichero.query.filter(Fichero.coleccion_id == id, Fichero.activado == 1).all()
            datos = []
            for fichero in ficheros:
                datos.append(DatoFichero(fichero.id, fichero.nombre_original, fichero.nombre_almacenado,
                                         fichero.tipo_fichero.descripcion))
            result = self._datosfichero_schema.dump(datos)
            return jsonify(result), 200
        else:
            return {'mensaje': 'Se necesita informar una colección para recuperar sus ficheros'}, 404

    def get_dato_fichero(self, id):
        if id:
            fichero = Fichero.query.get(id)
            dato = DatoFichero(fichero.id, fichero.nombre_original, fichero.nombre_almacenado, fichero.tipo_fichero.descripcion)
            result = self._datofichero_schema.dump(dato)
            return jsonify(result), 200
        else:
            return {'mensaje': 'No se ha encontrado id fichero'}, 404

    def subir_fichero(self, request):
        data = request.values

        if 'coleccion' not in data:
            return {'mensaje': 'No se ha proporcionado ninguna base asociada'}, 400
        if 'fichero' not in request.files:
            return {'mensaje': 'No se ha proporcionado ningún fichero'}, 400
        if 'tipo' not in data:
            return {'mensaje': 'No se ha proporcionado ningún tipo fichero'}, 400

        tipo = TipoFichero.query.filter(TipoFichero.descripcion == data['tipo']).first()
        if not tipo:
            return {'mensaje': 'No se ha encontrado ningún tipo fichero'}, 400

        archivo = request.files['fichero']
        if archivo.filename == '':
            return {'mensaje': 'No se ha seleccionado ningún archivo'}, 400

        nombre_original = archivo.filename
        parts = nombre_original.split('.')
        extension = parts[-1]

        coleccion = Coleccion.query.get(data['coleccion'])
        ruta = os.path.abspath(self._path)
        nombre = str(uuid.uuid4()) + '.' + extension
        fichero = Fichero(ruta, nombre_original, nombre, tipo, coleccion, 1)
        res = self._almacenar(archivo, ruta, nombre)

        if res:
            return res
        else:
            db.session.add(fichero)
            db.session.commit()
            return self.get_dato_fichero(fichero.id)

    def eliminar_fichero(self, id):
        fichero = Fichero.query.get(id)
        if not fichero:
            return {'mensaje': 'No se ha encontrado ningún fichero con ese id'}, 404
        fichero.activado = 0
        db.session.commit()
        return {'mensaje': 'Fichero eliminado correctamente'}, 200