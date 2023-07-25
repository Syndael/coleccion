from marshmallow import Schema, fields
from app.utils.datos import db
from app.model.estado_model import EstadoSchema
from app.model.idioma_model import IdiomaSchema
from app.model.juego_model import JuegoSchema
from app.model.plataforma_model import PlataformaSchema
from app.model.region_model import RegionSchema
from app.model.tienda_model import TiendaSchema


class Coleccion(db.Model):
    __tablename__ = 'COLECCION'

    id = db.Column(db.Integer, primary_key=True)
    juego_id = db.Column(db.Integer, db.ForeignKey('JUEGO.id'))
    plataforma_id = db.Column(db.Integer, db.ForeignKey('PLATAFORMA.id'))
    idioma_id = db.Column(db.Integer, db.ForeignKey('IDIOMA.id'))
    region_id = db.Column(db.Integer, db.ForeignKey('REGION.id'))
    estado_general_id = db.Column(db.Integer, db.ForeignKey('ESTADO.id'))
    estado_caja_id = db.Column(db.Integer, db.ForeignKey('ESTADO.id'))
    fecha_compra = db.Column(db.Date)
    fecha_recibo = db.Column(db.Date)
    coste = db.Column(db.Float)
    tienda_id = db.Column(db.Integer, db.ForeignKey('TIENDA.id'))
    notas = db.Column(db.String(255))

    juego = db.relationship('Juego', primaryjoin='Coleccion.juego_id == Juego.id')
    plataforma = db.relationship('Plataforma', primaryjoin='Coleccion.plataforma_id == Plataforma.id')
    idioma = db.relationship('Idioma', primaryjoin='Coleccion.idioma_id == Idioma.id')
    region = db.relationship('Region', primaryjoin='Coleccion.region_id == Region.id')
    estado_general = db.relationship('Estado', primaryjoin='Coleccion.estado_general_id == Estado.id')
    estado_caja = db.relationship('Estado', primaryjoin='Coleccion.estado_caja_id == Estado.id')
    tienda = db.relationship('Tienda', primaryjoin='Coleccion.tienda_id == Tienda.id')

    def __init__(self, juego, plataforma, idioma, region, estado_general, estado_caja, fecha_compra, fecha_recibo, coste, tienda, notas):
        self.juego = juego
        self.plataforma = plataforma
        self.idioma = idioma
        self.region = region
        self.estado_general = estado_general
        self.estado_caja = estado_caja
        self.fecha_compra = fecha_compra
        self.fecha_recibo = fecha_recibo
        self.coste = coste
        self.tienda = tienda
        self.notas = notas


class ColeccionSchema(Schema):
    juego = fields.Nested(JuegoSchema)
    plataforma = fields.Nested(PlataformaSchema)
    idioma = fields.Nested(IdiomaSchema)
    region = fields.Nested(RegionSchema)
    estado_general = fields.Nested(EstadoSchema)
    estado_caja = fields.Nested(EstadoSchema)
    tienda = fields.Nested(TiendaSchema)

    class Meta:
        fields = ('id', 'juego', 'plataforma', 'idioma', 'region', 'estado_general', 'estado_caja', 'fecha_compra', 'fecha_recibo', 'coste', 'tienda', 'notas')
        include_relationships = True