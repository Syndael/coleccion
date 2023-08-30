export class Estado {
    id: number | undefined;
    descripcion: string | undefined;
    tipo!: number;
}

export enum TipoEstado {
    GENERAL,
    CAJAS,
    PROGRESO
}