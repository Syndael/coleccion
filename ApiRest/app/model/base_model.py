from marshmallow import Schema, fields
from app.utils.datos import db
from app.model.tipo_base_model import TipoBase, TipoBaseSchema


class Base(db.Model):
    __tablename__ = 'BASE'

    id = db.Column(db.Integer, primary_key=True)
    tipo_id = db.Column(db.Integer, db.ForeignKey('TIPO_BASE.id'))
    nombre = db.Column(db.String(255))
    codigo = db.Column(db.String(255))
    saga = db.Column(db.String(255))
    fecha_salida = db.Column(db.Date)
    plataformas = db.Column(db.String(100))

    tipo_base = db.relationship('TipoBase', primaryjoin='Base.tipo_id == TipoBase.id')

    def __init__(self, tipo_base, nombre, codigo=None, saga=None, fecha_salida=None, plataformas=None):
        self.tipo_base = tipo_base
        self.nombre = nombre
        self.codigo = codigo
        self.saga = saga
        self.fecha_salida = fecha_salida
        self.plataformas = plataformas


class BaseSchema(Schema):
    tipo_base = fields.Nested(TipoBaseSchema)
    class Meta:
        fields = ('id', 'tipo_base', 'nombre', 'codigo', 'saga', 'fecha_salida', 'plataformas')
        include_relationships = True
