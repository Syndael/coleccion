from marshmallow import Schema, fields
from app.utils.datos import db
from app.model.base_model import BaseSchema


class BaseDlc(db.Model):
    __tablename__ = 'BASE_DLC'

    id = db.Column(db.Integer, primary_key=True)
    base_id = db.Column(db.Integer, db.ForeignKey('BASE.id'))
    nombre = db.Column(db.String(255))

    base = db.relationship('Base', primaryjoin='BaseDlc.base_id == Base.id')

    def __init__(self, base, nombre=None):
        self.base = base
        self.nombre = nombre


class BaseDlcSchema(Schema):
    base = fields.Nested(BaseSchema)

    class Meta:
        fields = ('id', 'base', 'nombre')
        include_relationships = True
