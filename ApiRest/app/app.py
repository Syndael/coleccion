import logging
import os
from app.utils import constantes

from flask import Flask, request
from app.utils.datos import db
from app.utils.config_parser_utils import ConfigParser
from app.service.coleccion_service import ColeccionService
from app.service.juego_service import JuegoService

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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{}:{}@{}/{}'.format(mssql['user'], mssql['passwd'], mssql['host'], mssql['db'])
db.init_app(app)

# coleccion
_coleccion_service = ColeccionService()


@app.route('/api/coleccion', methods=['GET'])
def get_colecciones():
    return _coleccion_service.get_colecciones()


@app.route('/api/coleccion/<id>', methods=['GET'])
def get_colecciones_by_id(id):
    return _coleccion_service.get_colecciones_by_id(id)


@app.route('/api/coleccion/nombre/<nombre>', methods=['GET'])
def get_colecciones_by_nombre(nombre):
    return _coleccion_service.get_colecciones_by_nombre(nombre)


@app.route('/api/coleccion', methods=['POST'])
def add_coleccion():
    return _coleccion_service.add_coleccion(request)


@app.route('/api/coleccion/<id>', methods=['PUT'])
def update_coleccion(id):
    return _coleccion_service.update_coleccion(request, id)


@app.route('/api/coleccion/<id>', methods=['DELETE'])
def delete_coleccion(id):
    return _coleccion_service.delete_coleccion(id)


# juegos
_juego_service = JuegoService()


@app.route('/api/juegos', methods=['GET'])
def get_juegos():
    return _juego_service.get_juegos()


@app.route('/api/juego/nombre/<nombre>', methods=['GET'])
def get_juegos_by_nombre(nombre):
    return _juego_service.get_juegos_by_nombre(nombre)


@app.route('/api/juego', methods=['POST'])
def add_juego():
    return _juego_service.add_juego(request)


@app.route('/api/juego/<id>', methods=['PUT'])
def update_juego(id):
    return _juego_service.update_juego(request, id)


# default
@app.route('/')
def index():
    return "<span style='color:green'>ApiColeccion</span>"