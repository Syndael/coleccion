from marshmallow import Schema, fields
from app.utils.datos import db
from app.model.base_model import BaseSchema
from app.model.plataforma_model import PlataformaSchema


class Edicion(db.Model):
    __tablename__ = 'EDICION'

    id = db.Column(db.Integer, primary_key=True)
    base_id = db.Column(db.Integer, db.ForeignKey('BASE.id'))
    plataforma_id = db.Column(db.Integer, db.ForeignKey('PLATAFORMA.id'))
    nombre = db.Column(db.String(255))
    fecha = db.Column(db.Date)

    base = db.relationship('Base', primaryjoin='Edicion.base_id == Base.id')
    plataforma = db.relationship('Plataforma', primaryjoin='Edicion.plataforma_id == Plataforma.id')

    def __init__(self, base, nombre, plataforma=None, fecha=None):
        self.base = base
        self.plataforma = plataforma
        self.nombre = nombre
        self.fecha = fecha


class EdicionSchema(Schema):
    base = fields.Nested(BaseSchema)
    plataforma = fields.Nested(PlataformaSchema)

    class Meta:
        fields = ('id', 'base', 'plataforma', 'nombre', 'fecha')
        include_relationships = True