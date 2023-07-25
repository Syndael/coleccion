from marshmallow import Schema, fields
from sqlalchemy import Numeric
from app.utils.datos import db
from app.model.juego_model import JuegoSchema
from app.model.plataforma_model import PlataformaSchema
from app.model.estado_model import EstadoSchema


class Jugado(db.Model):
    __tablename__ = 'JUGADO'

    id = db.Column(db.Integer, primary_key=True)
    juego_id = db.Column(db.Integer, db.ForeignKey('JUEGO.id'))
    plataforma_id = db.Column(db.Integer, db.ForeignKey('PLATAFORMA.id'))
    estado_jugado_id = db.Column(db.Integer, db.ForeignKey('ESTADO.id'))
    porcentaje = db.Column(db.Integer)
    horas = db.Column(Numeric(precision=20, scale=6))
    historia_completa = db.Column(db.Boolean)
    notas = db.Column(db.String(255))
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)

    juego = db.relationship('Juego', primaryjoin='Jugado.juego_id == Juego.id')
    plataforma = db.relationship('Plataforma', primaryjoin='Jugado.plataforma_id == Plataforma.id')
    estado_jugado = db.relationship('Estado', primaryjoin='Jugado.estado_jugado_id == Estado.id')

    def __init__(self, juego, plataforma, estado_jugado, porcentaje, horas, historia_completa, notas, fecha_inicio, fecha_fin):
        self.juego = juego
        self.plataforma = plataforma
        self.estado_jugado = estado_jugado
        self.porcentaje = porcentaje
        self.horas = horas
        self.historia_completa = historia_completa
        self.notas = notas
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin


class JugadoSchema(Schema):
    juego = fields.Nested(JuegoSchema)
    plataforma = fields.Nested(PlataformaSchema)
    estado_jugado = fields.Nested(EstadoSchema)

    class Meta:
        fields = ('id', 'juego', 'plataforma', 'estado_jugado', 'porcentaje', 'horas', 'historia_completa', 'notas', 'fecha_inicio', 'fecha_fin')
        include_relationships = True