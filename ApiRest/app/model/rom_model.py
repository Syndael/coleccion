from marshmallow import Schema, fields
from app.utils.datos import db
from app.model.idioma_model import IdiomaSchema
from app.model.juego_model import JuegoSchema
from app.model.plataforma_model import PlataformaSchema
from app.model.region_model import RegionSchema
from app.model.tipo_rom_model import TipoRomSchema


class Rom(db.Model):
    __tablename__ = 'ROM'

    id = db.Column(db.Integer, primary_key=True)
    juego_id = db.Column(db.Integer, db.ForeignKey('JUEGO.id'))
    plataforma_id = db.Column(db.Integer, db.ForeignKey('PLATAFORMA.id'))
    nombre_rom = db.Column(db.String(255))
    nombre_rom_ext = db.Column(db.String(255))
    idioma_id = db.Column(db.Integer, db.ForeignKey('IDIOMA.id'))
    region_id = db.Column(db.Integer, db.ForeignKey('REGION.id'))
    tipo_rom_id = db.Column(db.Integer, db.ForeignKey('TIPO_ROM.id'))
    fecha_descarga = db.Column(db.Date)

    juego = db.relationship('Juego', primaryjoin='Rom.juego_id == Juego.id')
    plataforma = db.relationship('Plataforma', primaryjoin='Rom.plataforma_id == Plataforma.id')
    idioma = db.relationship('Idioma', primaryjoin='Rom.idioma_id == Idioma.id')
    region = db.relationship('Region', primaryjoin='Rom.region_id == Region.id')
    tipo_rom = db.relationship('TipoRom', primaryjoin='Rom.tipo_rom_id == TipoRom.id')

    def __init__(self, juego, plataforma, nombre_rom=None, nombre_rom_ext=None, idioma=None, region=None, tipo_rom=None, fecha_descarga=None):
        self.juego = juego
        self.plataforma = plataforma
        self.nombre_rom = nombre_rom
        self.nombre_rom_ext = nombre_rom_ext
        self.idioma = idioma
        self.region = region
        self.tipo_rom = tipo_rom
        self.fecha_descarga = fecha_descarga


class RomSchema(Schema):
    juego = fields.Nested(JuegoSchema)
    plataforma = fields.Nested(PlataformaSchema)
    idioma = fields.Nested(IdiomaSchema)
    region = fields.Nested(RegionSchema)
    tipo_rom = fields.Nested(TipoRomSchema)

    class Meta:
        fields = ('id', 'juego', 'plataforma', 'idioma', 'nombre_rom', 'nombre_rom_ext', 'region', 'tipo_rom', 'fecha_descarga')
        include_relationships = True