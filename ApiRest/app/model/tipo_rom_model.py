from marshmallow import Schema
from app.utils.datos import db


class TipoRom(db.Model):
    __tablename__ = 'TIPO_ROM'

    id = db.Column(db.Integer, primary_key=True)
    extension = db.Column(db.String(50))

    def __init__(self, extension):
        self.extension = extension


class TipoRomSchema(Schema):
    class Meta:
        fields = ('id', 'extension')