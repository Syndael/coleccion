from marshmallow import Schema
from app.utils.datos import db


class Idioma(db.Model):
    __tablename__ = 'IDIOMA'

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(255))
    corto = db.Column(db.String(255))

    def __init__(self, descripcion, corto):
        self.descripcion = descripcion
        self.corto = corto


class IdiomaSchema(Schema):
    class Meta:
        fields = ('id', 'descripcion', 'corto')
