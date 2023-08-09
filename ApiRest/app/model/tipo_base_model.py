from marshmallow import Schema
from app.utils.datos import db


class TipoBase(db.Model):
    __tablename__ = 'TIPO_BASE'

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50))

    def __init__(self, descripcion):
        self.descripcion = descripcion


class TipoBaseSchema(Schema):
    class Meta:
        fields = ('id', 'descripcion')
