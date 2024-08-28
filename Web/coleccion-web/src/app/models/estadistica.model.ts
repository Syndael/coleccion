export class Completo {
    id: number | undefined;
    mes: string | undefined;
    cantidad: number | undefined;
    juegos: string | undefined;
    orden_desc: string | undefined;
}

export class Gasto {
    id: number | undefined;
    tipo: TipoGasto | undefined;
    plataforma_nombre: string | undefined;
    plataforma_corto: string | undefined;
    descripcion: string | undefined;
    cantidad: number | undefined;
    fisico: number | undefined;
    digital: number | undefined;
    coste: number | undefined;
    orden_desc: string | undefined;
    orden_asc: string | undefined;
}

export enum TipoGasto {
    JUEGOS_PLATAFORMA = "JUEGOS_PLATAFORMA",
    JUEGOS_MES = "JUEGOS_MES",
    JUEGOS_TIENDA = "JUEGOS_TIENDAS",
    ROMS_PLATAFORMA = "ROMS_PLATAFORMA",
    TOTAL = "TOTAL"
}