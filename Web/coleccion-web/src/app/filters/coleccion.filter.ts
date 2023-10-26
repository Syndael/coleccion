export class FiltroColeccion {
    idColeccion: number | undefined;
    tipo: number | undefined;
    estadoGeneralSeleccionado: number | undefined;
    plataformaSeleccionada: number | undefined;
    nombreBase: string | undefined;
    saga: string | undefined;
    tiendaSeleccionada: number | undefined;
    ordenSeleccionado: string | undefined;
}

export enum OrdenEnum {
    NONE = '',
    COLECCION = 'Colección',
    COMPRAS = 'Compras',
    EN_CURSO = 'En curso',
    POKEMON = 'Pokémon'
}