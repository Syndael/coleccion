import { Environment } from "../environments/environment";

export class Constantes {
    static readonly COLECCIONES_URL = Environment.BASE_URL + Environment.API + '/colecciones';
    static readonly COLECCION_URL = Environment.BASE_URL + Environment.API + '/coleccion';
    static readonly COLECCION_ID_URL = Constantes.COLECCION_URL + '/id';

    static readonly ESTADOS_URL = Environment.BASE_URL + Environment.API + '/estados';

    static readonly HISTORIALES_URL = Environment.BASE_URL + Environment.API + '/jugados';
    static readonly HISTORIAL_URL = Environment.BASE_URL + Environment.API + '/jugado';
    static readonly HISTORIAL_ID_URL = Constantes.HISTORIAL_URL + '/id';

    static readonly IDIOMAS_URL = Environment.BASE_URL + Environment.API + '/idiomas';

    static readonly JUEGOS_URL = Environment.BASE_URL + Environment.API + '/juegos';
    static readonly JUEGO_URL = Environment.BASE_URL + Environment.API + '/juego';
    static readonly JUEGO_ID_URL = Constantes.JUEGO_URL + '/id';

    static readonly PLATAFORMAS_URL = Environment.BASE_URL + Environment.API + '/plataformas';

    static readonly REGIONES_URL = Environment.BASE_URL + Environment.API + '/regiones';

    static readonly ROMS_URL = Environment.BASE_URL + Environment.API + '/roms';
    static readonly ROM_URL = Environment.BASE_URL + Environment.API + '/rom';
    static readonly ROM_ID_URL = Constantes.ROM_URL + '/id';

    static readonly TIENDAS_URL = Environment.BASE_URL + Environment.API + '/tiendas';

    static readonly TIPOS_ROM_URL = Environment.BASE_URL + Environment.API + '/tiposrom';
}