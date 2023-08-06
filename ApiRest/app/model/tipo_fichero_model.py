from marshmallow import Schema
from app.utils.datos import db


class TipoFichero(db.Model):
    __tablename__ = 'TIPO_FICHERO'

    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50))

    def __init__(self, descripcion):
        self.descripcion = descripcion


class TipoFicheroSchema(Schema):
    class Meta:
        fields = ('id', 'descripcion')