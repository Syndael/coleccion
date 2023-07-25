export class Constantes {
    static readonly BASE_URL = 'http://localhost:5000';
    // static readonly BASE_URL = 'https://192.168.1.55:9448';
    // static readonly BASE_URL = 'https://chorizox.duckdns.org:9448';
    static readonly API = '/api';
    static readonly COLECCIONES_URL = Constantes.BASE_URL + Constantes.API + '/colecciones';
    static readonly COLECCION_URL = Constantes.BASE_URL + Constantes.API + '/coleccion/id';
    static readonly HISTORIALES_URL = Constantes.BASE_URL + Constantes.API + '/jugados';
    static readonly HISTORIAL_URL = Constantes.BASE_URL + Constantes.API + '/jugado/id';
    static readonly JUEGOS_URL = Constantes.BASE_URL + Constantes.API + '/juegos';
    static readonly JUEGO_URL = Constantes.BASE_URL + Constantes.API + '/juego';
    static readonly JUEGO_ID_URL = Constantes.JUEGO_URL + '/id';
    static readonly ROMS_URL = Constantes.BASE_URL + Constantes.API + '/roms';
    static readonly ROM_URL = Constantes.BASE_URL + Constantes.API + '/rom';
    static readonly ROM_ID_URL = Constantes.ROM_URL + '/id';
}