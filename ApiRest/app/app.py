import logging
import os
from app.utils import constantes

from flask import Flask, request
from flask_cors import CORS
from app.utils.datos import db
from app.utils.config_parser_utils import ConfigParser
from app.service.base_service import BaseService
from app.service.base_dlc_service import BaseDlcService
from app.service.base_plataforma_service import BasePlataformaService
from app.service.coleccion_service import ColeccionService
from app.service.edicion_service import EdicionService
from app.service.estadistica_service import EstadisticasService
from app.service.estado_service import EstadoService
from app.service.fichero_service import FicheroService
from app.service.idioma_service import IdiomaService
from app.service.progreso_service import ProgresoService
from app.service.progreso_sesion_service import ProgresoSesionService
from app.service.plataforma_service import PlataformaService
from app.service.region_service import RegionService
from app.service.rom_service import RomService
from app.service.tienda_service import TiendaService
from app.service.tipo_base_service import TipoBaseService
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{}:{}@{}/{}'.format(mssql['user'], mssql['passwd'],
                                                                                    mssql['host'], mssql['db'])
db.init_app(app)

# Bases
_base_service = BaseService()


@app.route('/api/bases', methods=['GET'])
def get_bases():
    return _base_service.get_bases(request)


@app.route('/api/base/id/<id>', methods=['GET'])
def get_bases_by_id(id):
    return _base_service.get_bases_by_id(id)


@app.route('/api/base', methods=['POST'])
def add_base():
    return _base_service.add_base(request)


@app.route('/api/base/id/<id>', methods=['PUT'])
def update_base(id):
    return _base_service.update_base(request, id)


@app.route('/api/base/id/<id>', methods=['DELETE'])
def delete_base_by_id(id):
    return _base_service.delete_base_by_id(id)


# Bases DLC
_base_dlc_service = BaseDlcService()


@app.route('/api/basesdlc', methods=['GET'])
def get_bases_dlc():
    return _base_dlc_service.get_bases_dlc(request)


@app.route('/api/basedlc/id/<id>', methods=['GET'])
def get_bases_dlc_by_id(id):
    return _base_dlc_service.get_base_dlc_by_id(id)


@app.route('/api/basedlc', methods=['POST'])
def add_base_dlc():
    return _base_dlc_service.add_base_dlc(request)


@app.route('/api/basedlc/id/<id>', methods=['DELETE'])
def delete_bases_dlc_by_id(id):
    return _base_dlc_service.delete_base_dlc_by_id(id)


# Bases Plataforma
_base_plataforma_service = BasePlataformaService()


@app.route('/api/basesplataforma', methods=['GET'])
def get_bases_plataforma():
    return _base_plataforma_service.get_bases_plataforma(request)


@app.route('/api/baseplataforma/id/<id>', methods=['GET'])
def get_bases_plataforma_by_id(id):
    return _base_plataforma_service.get_base_plataforma_by_id(id)


@app.route('/api/baseplataforma', methods=['POST'])
def add_base_plataforma():
    return _base_plataforma_service.add_base_plataforma(request)


@app.route('/api/baseplataforma/id/<id>', methods=['DELETE'])
def delete_bases_plataforma_by_id(id):
    return _base_plataforma_service.delete_base_plataforma_by_id(id)


# Colecciones
_coleccion_service = ColeccionService()


@app.route('/api/colecciones', methods=['GET'])
def get_colecciones():
    return _coleccion_service.get_colecciones(request)


@app.route('/api/coleccion/id/<id>', methods=['GET'])
def get_colecciones_by_id(id):
    return _coleccion_service.get_coleccion_by_id(id)


@app.route('/api/coleccion', methods=['POST'])
def add_coleccion():
    return _coleccion_service.add_coleccion(request)


@app.route('/api/coleccion/id/<id>', methods=['PUT'])
def update_coleccion(id):
    return _coleccion_service.update_coleccion(request, id)


@app.route('/api/coleccion/id/<id>', methods=['DELETE'])
def delete_coleccion_by_id(id):
    return _coleccion_service.delete_coleccion_by_id(id)


# Edicion
_edicion_service = EdicionService()


@app.route('/api/ediciones', methods=['GET'])
def get_ediciones():
    return _edicion_service.get_ediciones(request)


@app.route('/api/edicion/id/<id>', methods=['GET'])
def get_edicion_by_id(id):
    return _edicion_service.get_edicion_by_id(id)


@app.route('/api/edicion', methods=['POST'])
def add_edicion():
    return _edicion_service.add_edicion(request)


@app.route('/api/edicion/id/<id>', methods=['DELETE'])
def delete_edicion_by_id(id):
    return _edicion_service.delete_edicion_by_id(id)


# Estadísticas
_estadisticas_service = EstadisticasService()


@app.route('/api/estadisticas/completos', methods=['GET'])
def get_completos():
    return _estadisticas_service.get_completos()


@app.route('/api/estadisticas/gastos', methods=['GET'])
def get_gastos():
    return _estadisticas_service.get_gastos()


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


# Progresos
_progreso_service = ProgresoService()


@app.route('/api/progresos', methods=['GET'])
def get_progresos():
    return _progreso_service.get_progresos(request)


@app.route('/api/progreso/id/<id>', methods=['GET'])
def get_progreso_by_id(id):
    return _progreso_service.get_progreso_by_id(id)


@app.route('/api/progresos/ultimos', methods=['GET'])
def get_ultimos_progresos():
    return _progreso_service.get_ultimos_progresos()


@app.route('/api/progreso', methods=['POST'])
def add_progreso():
    return _progreso_service.add_progreso(request)


@app.route('/api/progreso/id/<id>', methods=['PUT'])
def update_progreso(id):
    return _progreso_service.update_progreso(request, id)


@app.route('/api/progreso/id/<id>', methods=['DELETE'])
def delete_progreso_by_id(id):
    return _progreso_service.delete_progreso_by_id(id)


# Progreso Sesiones
_progreso_sesion_service = ProgresoSesionService()

@app.route('/api/sesiones', methods=['GET'])
def get_sesiones():
    return _progreso_sesion_service.get_sesiones(request)


@app.route('/api/sesion', methods=['POST'])
def add_sesion():
    return _progreso_sesion_service.add_sesion(request)


@app.route('/api/sesion/id/<id>', methods=['PUT'])
def update_sesion(id):
    return _progreso_sesion_service.update_sesion(request, id)


@app.route('/api/sesion/id/<id>', methods=['DELETE'])
def delete_sesion_by_id(id):
    return _progreso_sesion_service.delete_sesion_by_id(id)


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
    return _rom_service.get_roms(request)


@app.route('/api/rom/id/<id>', methods=['GET'])
def get_rom_by_id(id):
    return _rom_service.get_rom_by_id(id)


@app.route('/api/rom', methods=['POST'])
def add_rom():
    return _rom_service.add_rom(request)


@app.route('/api/rom/id/<id>', methods=['PUT'])
def update_rom(id):
    return _rom_service.update_rom(request, id)


@app.route('/api/rom/id/<id>', methods=['DELETE'])
def delete_rom_by_id(id):
    return _rom_service.delete_rom_by_id(id)


# Tiendas
_tienda_service = TiendaService()


@app.route('/api/tiendas', methods=['GET'])
def get_tiendas():
    return _tienda_service.get_tiendas()


# Tipo Base
_tipo_base_service = TipoBaseService()


@app.route('/api/tiposbase', methods=['GET'])
def get_tipos_base():
    return _tipo_base_service.get_tipos_base()


# Tipo ROM
_tipo_rom_service = TipoRomService()


@app.route('/api/tiposrom', methods=['GET'])
def get_tipos_rom():
    return _tipo_rom_service.get_tipos_rom()


# File Service
_fichero_service = FicheroService()


@app.route('/api/fichero/id/<id>', methods=['GET'])
def get_fichero(id):
    return _fichero_service.get_fichero(id)


@app.route('/api/datos_ficheros_coleccion/<id>', methods=['GET'])
def get_datos_ficheros_coleccion(id):
    return _fichero_service.get_datos_ficheros_coleccion(id)

@app.route('/api/datos_ficheros_progreso/<id>', methods=['GET'])
def get_datos_ficheros_progreso(id):
    return _fichero_service.get_datos_ficheros_progreso(id)


@app.route('/api/fichero', methods=['POST'])
def subir_fichero():
    return _fichero_service.subir_fichero(request)


@app.route('/api/fichero/id/<id>', methods=['DELETE'])
def eliminar_fichero(id):
    return _fichero_service.eliminar_fichero(id)


# default
@app.route('/')
def index():
    return "<span style='color:green'>ApiColeccion</span>"
