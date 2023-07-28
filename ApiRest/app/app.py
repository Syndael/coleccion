import logging
import os
from app.utils import constantes

from flask import Flask, request
from flask_cors import CORS
from app.utils.datos import db
from app.utils.config_parser_utils import ConfigParser
from app.service.coleccion_service import ColeccionService
from app.service.estado_service import EstadoService
from app.service.idioma_service import IdiomaService
from app.service.juego_service import JuegoService
from app.service.jugado_service import JugadoService
from app.service.plataforma_service import PlataformaService
from app.service.region_service import RegionService
from app.service.rom_service import RomService
from app.service.tipo_rom_service import TipoRomService

_config = ConfigParser()
mssql = {'host': _config.get_value(constantes.HOST),
         'user': _config.get_value(constantes.USER),
         'passwd': _config.get_value(constantes.PASS),
         'db': _config.get_value(constantes.DB)}

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    level=logging.DEBUG,
                    handlers=[logging.FileHandler(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                                               _config.get_value(constantes.LOG_FILE)),
                                                  mode='w',
                                                  encoding='UTF-8'),
                              logging.StreamHandler()
                              ]
                    )
logger = logging.getLogger()

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{}:{}@{}/{}'.format(mssql['user'], mssql['passwd'], mssql['host'], mssql['db'])
db.init_app(app)

# Colecciones
_coleccion_service = ColeccionService()


@app.route('/api/colecciones', methods=['GET'])
def get_colecciones():
    return _coleccion_service.get_colecciones()

@app.route('/api/coleccion/id/<id>', methods=['GET'])
def get_colecciones_by_id(id):
    return _coleccion_service.get_coleccion_by_id(id)

@app.route('/api/coleccion/nombre/<nombre>', methods=['GET'])
def get_colecciones_by_nombre(nombre):
    return _coleccion_service.get_colecciones_by_nombre(nombre)

@app.route('/api/coleccion', methods=['POST'])
def add_coleccion():
    return _coleccion_service.add_coleccion(request)

@app.route('/api/coleccion/id/<id>', methods=['PUT'])
def update_coleccion(id):
    return _coleccion_service.update_coleccion(request, id)


# Estados
_estado_service = EstadoService()


@app.route('/api/estados', methods=['GET'])
def get_estados():
    return _estado_service.get_estados()


# Idiomas
_idioma_service = IdiomaService()


@app.route('/api/idiomas', methods=['GET'])
def get_idiomas():
    return _idioma_service.get_idiomas()


# Juegos
_juego_service = JuegoService()


@app.route('/api/juegos', methods=['GET'])
def get_juegos():
    return _juego_service.get_juegos()

@app.route('/api/juego/id/<id>', methods=['GET'])
def get_juegos_by_id(id):
    return _juego_service.get_juegos_by_id(id)

@app.route('/api/juego/nombre/<nombre>', methods=['GET'])
def get_juegos_by_nombre(nombre):
    return _juego_service.get_juegos_by_nombre(nombre)

@app.route('/api/juego', methods=['POST'])
def add_juego():
    return _juego_service.add_juego(request)

@app.route('/api/juego/id/<id>', methods=['PUT'])
def update_juego(id):
    return _juego_service.update_juego(request, id)


# Jugados
_jugado_service = JugadoService()


@app.route('/api/jugados', methods=['GET'])
def get_jugados():
    return _jugado_service.get_jugados()

@app.route('/api/jugado/id/<id>', methods=['GET'])
def get_jugado_by_id(id):
    return _jugado_service.get_jugado_by_id(id)

@app.route('/api/jugado', methods=['POST'])
def add_jugado():
    return _jugado_service.add_jugado(request)

@app.route('/api/jugado/id/<id>', methods=['PUT'])
def update_jugado(id):
    return _jugado_service.update_jugado(request, id)


# Plataformas
_plataforma_service = PlataformaService()


@app.route('/api/plataformas', methods=['GET'])
def get_plataformas():
    return _plataforma_service.get_plataformas()


# Regiones
_region_service = RegionService()


@app.route('/api/regiones', methods=['GET'])
def get_regiones():
    return _region_service.get_regiones()


# roms
_rom_service = RomService()


@app.route('/api/roms', methods=['GET'])
def get_roms():
    return _rom_service.get_roms()

@app.route('/api/rom/id/<id>', methods=['GET'])
def get_rom_by_id(id):
    return _rom_service.get_rom_by_id(id)

@app.route('/api/rom', methods=['POST'])
def add_rom():
    return _rom_service.add_rom(request)

@app.route('/api/rom/id/<id>', methods=['PUT'])
def update_rom(id):
    return _rom_service.update_rom(request, id)


# Tipo ROM
_tipo_rom_service = TipoRomService()


@app.route('/api/tiposrom', methods=['GET'])
def get_tipos_rom():
    return _tipo_rom_service.get_tipos_rom()


# default
@app.route('/')
def index():
    return "<span style='color:green'>ApiColeccion</span>"