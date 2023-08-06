from marshmallow import Schema, fields
from app.utils.datos import db
from app.model.coleccion_model import ColeccionSchema
from app.model.tipo_fichero_model import TipoFicheroSchema


class Fichero(db.Model):
    __tablename__ = 'FICHERO'

    id = db.Column(db.Integer, primary_key=True)
    ruta = db.Column(db.String(255))
    nombre_original = db.Column(db.String(255))
    nombre_almacenado = db.Column(db.String(255))
    activado = db.Column(db.Boolean)

    tipo_fichero_id = db.Column(db.Integer, db.ForeignKey('TIPO_FICHERO.id'))
    coleccion_id = db.Column(db.Integer, db.ForeignKey('COLECCION.id'))

    tipo_fichero = db.relationship('TipoFichero', primaryjoin='Fichero.tipo_fichero_id == TipoFichero.id')
    coleccion = db.relationship('Coleccion', primaryjoin='Fichero.coleccion_id == Coleccion.id')

    def __init__(self, ruta, nombre_original, nombre_almacenado, tipo_fichero, coleccion, activado=None):
        self.ruta = ruta
        self.nombre_original = nombre_original
        self.nombre_almacenado = nombre_almacenado
        self.tipo_fichero = tipo_fichero
        self.coleccion = coleccion
        self.activado = activado


class FicheroSchema(Schema):
    tipo_fichero = fields.Nested(TipoFicheroSchema)
    coleccion = fields.Nested(ColeccionSchema)

    class Meta:
        fields = ('id', 'ruta', 'nombre_original', 'nombre_almacenado', 'tipo_fichero', 'coleccion')
        include_relationships = True


class DatoFichero():
    id = db.Integer
    nombre_original = db.String(255)
    nombre_final = db.String(255)
    tipo_fichero = db.String(50)

    def __init__(self, id, nombre_original, nombre_final, tipo_fichero):
        self.id = id
        self.nombre_original = nombre_original
        self.nombre_final = nombre_final
        self.tipo_fichero = tipo_fichero


class DatoFicheroSchema(Schema):
    class Meta:
        fields = ('id', 'nombre_original', 'nombre_final', 'tipo_fichero')