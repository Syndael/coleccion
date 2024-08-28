export class Empresa {
    id: number | undefined;
    nombre: string | undefined;
    tipo!: number;
    url: string | undefined;
}

export enum TipoEmpresa {
    REPARTO
}