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
    porcentaje = db.Column(db.Integer)
    horas = db.Column(Numeric(precision=20, scale=6))
    historia_completa = db.Column(db.Boolean)
    notas = db.Column(db.String(255))
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)

    base = db.relationship('Base', primaryjoin='Progreso.base_id == Base.id')
    plataforma = db.relationship('Plataforma', primaryjoin='Progreso.plataforma_id == Plataforma.id')
    estado_progreso = db.relationship('Estado', primaryjoin='Progreso.estado_progreso_id == Estado.id')

    def __init__(self, base, plataforma, estado_progreso=None, porcentaje=None, horas=None, historia_completa=None, notas=None, fecha_inicio=None, fecha_fin=None):
        self.base = base
        self.plataforma = plataforma
        self.estado_progreso = estado_progreso
        self.porcentaje = porcentaje
        self.horas = horas
        self.historia_completa = historia_completa
        self.notas = notas
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin


class ProgresoSchema(Schema):
    base = fields.Nested(BaseSchema)
    plataforma = fields.Nested(PlataformaSchema)
    estado_jugado = fields.Nested(EstadoSchema)

    class Meta:
        fields = ('id', 'base', 'plataforma', 'estado_jugado', 'porcentaje', 'horas', 'historia_completa', 'notas', 'fecha_inicio', 'fecha_fin')
        include_relationships = True