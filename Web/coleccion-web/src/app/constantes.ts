import { Environment } from "../environments/environment";

export class Constantes {
    static readonly URL_API_BASE = Environment.BASE_URL + Environment.API

    static readonly BASES_URL = Constantes.URL_API_BASE + '/bases';
    static readonly BASE_URL = Constantes.URL_API_BASE + '/base';
    static readonly BASE_ID_URL = Constantes.BASE_URL + '/id';
    static readonly BASE_VANDAL_URL = Constantes.BASE_URL + '/vandal';
    
    static readonly BASES_PLATAFORMA_URL = Constantes.URL_API_BASE + '/basesplataforma';
    static readonly BASE_PLATAFORMA_URL = Constantes.URL_API_BASE + '/baseplataforma';
    static readonly BASE_PLATAFORMA_ID_URL = Constantes.BASE_PLATAFORMA_URL + '/id';

    static readonly COLECCIONES_URL = Constantes.URL_API_BASE + '/colecciones';
    static readonly COLECCION_URL = Constantes.URL_API_BASE + '/coleccion';
    static readonly COLECCION_ID_URL = Constantes.COLECCION_URL + '/id';
    
    static readonly BASES_DLC_URL = Constantes.URL_API_BASE + '/basesdlc';
    static readonly BASE_DLC_URL = Constantes.URL_API_BASE + '/basedlc';
    static readonly BASE_DLC_ID_URL = Constantes.BASE_DLC_URL + '/id';
    
    static readonly EDICIONES_URL = Constantes.URL_API_BASE + '/ediciones';
    static readonly EDICION_URL = Constantes.URL_API_BASE + '/edicion';
    static readonly EDICION_ID_URL = Constantes.EDICION_URL + '/id';
    
    static readonly ESTADISITCAS_URL = Constantes.URL_API_BASE + '/estadisticas';
    static readonly ESTADISITCAS_COMPLETOS_URL = Constantes.ESTADISITCAS_URL + '/completos';
    static readonly ESTADISITCAS_GASTOS_URL = Constantes.ESTADISITCAS_URL + '/gastos';

    static readonly FICHERO_URL = Constantes.URL_API_BASE + '/fichero';
    static readonly FICHERO_ID_URL = Constantes.FICHERO_URL + '/id';

    static readonly DATOS_FICHEROS_COLECCION_ID_URL = Constantes.URL_API_BASE + '/datos_ficheros_coleccion';
    static readonly DATOS_FICHEROS_PROGRESO_ID_URL = Constantes.URL_API_BASE + '/datos_ficheros_progreso';

    static readonly ESTADOS_URL = Constantes.URL_API_BASE + '/estados';

    static readonly EMPRESAS_URL = Constantes.URL_API_BASE + '/empresas';
    static readonly EMPRESAS_REPARTO_COD_SEG = '<SEGUIMIENTO>';

    static readonly PROGRESOS_URL = Constantes.URL_API_BASE + '/progresos';
    static readonly PROGRESO_URL = Constantes.URL_API_BASE + '/progreso';
    static readonly PROGRESO_ID_URL = Constantes.PROGRESO_URL + '/id';
    static readonly ULTIMOS_PROGRESOS_ID_URL = Constantes.PROGRESOS_URL + '/ultimos';

    static readonly SESIONES_URL = Constantes.URL_API_BASE + '/sesiones';
    static readonly SESION_URL = Constantes.URL_API_BASE + '/sesion';
    static readonly SESION_ID_URL = Constantes.SESION_URL + '/id';

    static readonly IDIOMAS_URL = Constantes.URL_API_BASE + '/idiomas';

    static readonly PLATAFORMAS_URL = Constantes.URL_API_BASE + '/plataformas';

    static readonly REGIONES_URL = Constantes.URL_API_BASE + '/regiones';

    static readonly ROMS_URL = Constantes.URL_API_BASE + '/roms';
    static readonly ROM_URL = Constantes.URL_API_BASE + '/rom';
    static readonly ROM_ID_URL = Constantes.ROM_URL + '/id';

    static readonly TIENDAS_URL = Constantes.URL_API_BASE + '/tiendas';

    static readonly TIPOS_BASE_URL = Constantes.URL_API_BASE + '/tiposbase';

    static readonly TIPOS_ROM_URL = Constantes.URL_API_BASE + '/tiposrom';
}