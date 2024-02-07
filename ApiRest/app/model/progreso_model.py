from marshmallow import Schema, fields
from sqlalchemy import Numeric
from app.utils.datos import db
from app.model.base_model import BaseSchema
from app.model.plataforma_model import PlataformaSchema
from app.model.estado_model import EstadoSchema


class Progreso(db.Model):
    __tablename__ = 'PROGRESO'

    id = db.Column(db.Integer, primary_key=True)
    base_id = db.Column(db.Integer, db.ForeignKey('BASE.id'))
    plataforma_id = db.Column(db.Integer, db.ForeignKey('PLATAFORMA.id'))
    estado_progreso_id = db.Column(db.Integer, db.ForeignKey('ESTADO.id'))
    horas = db.Column(Numeric(precision=20, scale=6))
    notas = db.Column(db.String(255))
    fecha_ultimo = db.Column(db.Date)

    base = db.relationship('Base', primaryjoin='Progreso.base_id == Base.id')
    plataforma = db.relationship('Plataforma', primaryjoin='Progreso.plataforma_id == Plataforma.id')
    estado_progreso = db.relationship('Estado', primaryjoin='Progreso.estado_progreso_id == Estado.id')

    def __init__(self, base, plataforma, estado_progreso=None, horas=None, notas=None, fecha_ultimo=None):
        self.base = base
        self.plataforma = plataforma
        self.estado_progreso = estado_progreso
        self.horas = horas
        self.notas = notas
        self.fecha_ultimo = fecha_ultimo


class ProgresoSchema(Schema):
    base = fields.Nested(BaseSchema)
    plataforma = fields.Nested(PlataformaSchema)
    estado_progreso = fields.Nested(EstadoSchema)

    class Meta:
        fields = ('id', 'base', 'plataforma', 'estado_progreso', 'horas', 'notas', 'fecha_ultimo')
        include_relationships = True
