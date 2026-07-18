from marshmallow import Schema, fields
from app.utils.datos import db
from app.model.coleccion_model import ColeccionSchema
from app.model.fichero_model import FicheroSchema


class IgPublicacion(db.Model):
    __tablename__ = 'IG_PUBLICACION'

    id = db.Column(db.Integer, primary_key=True)
    coleccion_id = db.Column(db.Integer, db.ForeignKey('COLECCION.id'))
    estado = db.Column(db.Enum('Revisar', 'Publicar', 'Publicado', 'Error', 'Cancelada', 'Descartado'))
    texto_publicacion = db.Column(db.Text)
    fecha_ig_publicacion = db.Column(db.DateTime)
    fecha_prevista_publicacion = db.Column(db.DateTime)
    ig_post_id = db.Column(db.String(100))
    fecha_creacion = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP"))
    fecha_modificacion = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP"), onupdate=db.text("CURRENT_TIMESTAMP"))

    coleccion = db.relationship('Coleccion', primaryjoin='IgPublicacion.coleccion_id == Coleccion.id')

    def __init__(self, coleccion, estado='Revisar', texto_publicacion=None,
                 fecha_ig_publicacion=None, fecha_prevista_publicacion=None, ig_post_id=None):
        self.coleccion = coleccion
        self.coleccion_id = coleccion.id if coleccion else None
        self.estado = estado
        self.texto_publicacion = texto_publicacion
        self.fecha_ig_publicacion = fecha_ig_publicacion
        self.fecha_prevista_publicacion = fecha_prevista_publicacion
        self.ig_post_id = ig_post_id


class IgPublicacionSchema(Schema):
    class Meta:
        fields = ('id', 'coleccion_id', 'estado', 'texto_publicacion',
                  'fecha_ig_publicacion', 'fecha_prevista_publicacion', 'ig_post_id', 'fecha_creacion', 'fecha_modificacion')


class IgFotoSeleccion(db.Model):
    __tablename__ = 'IG_FOTO_SELECCION'

    id = db.Column(db.Integer, primary_key=True)
    coleccion_id = db.Column(db.Integer, db.ForeignKey('COLECCION.id'))
    fichero_id = db.Column(db.Integer, db.ForeignKey('FICHERO.id'))
    orden = db.Column(db.Integer)
    activado = db.Column(db.Boolean)

    coleccion = db.relationship('Coleccion', primaryjoin='IgFotoSeleccion.coleccion_id == Coleccion.id')
    fichero = db.relationship('Fichero', primaryjoin='IgFotoSeleccion.fichero_id == Fichero.id')

    def __init__(self, coleccion, fichero, orden=None, activado=True):
        self.coleccion = coleccion
        self.fichero = fichero
        self.orden = orden
        self.activado = activado


class IgFotoSeleccionSchema(Schema):
    class Meta:
        fields = ('id', 'coleccion_id', 'fichero_id', 'orden', 'activado')


class IgToken(db.Model):
    __tablename__ = 'IG_TOKEN'

    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.Text)
    token_type = db.Column(db.String(50))
    expires_at = db.Column(db.DateTime)
    refresh_token = db.Column(db.Text)
    ig_user_id = db.Column(db.String(100))
    activado = db.Column(db.Boolean)
    fecha_creacion = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP"))

    def __init__(self, access_token, token_type='bearer', expires_at=None,
                 refresh_token=None, ig_user_id=None, activado=True):
        self.access_token = access_token
        self.token_type = token_type
        self.expires_at = expires_at
        self.refresh_token = refresh_token
        self.ig_user_id = ig_user_id
        self.activado = activado


class IgTokenSchema(Schema):
    class Meta:
        fields = ('id', 'access_token', 'token_type', 'expires_at',
                  'refresh_token', 'ig_user_id', 'activado', 'fecha_creacion')
