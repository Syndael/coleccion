export class TipoBase {
    id: number | undefined;
    descripcion: string | undefined;
}

export enum TipoBaseEnum {
    JUEGO = 'Juego',
    CONSOLA = 'Consola',
    MANDO = 'Mando',
    OTROS = 'Otros'
}