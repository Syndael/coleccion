import { Idioma } from "./idioma.model";
import { Base } from "./base.model";
import { Plataforma } from "./plataforma.model";
import { Region } from "./region.model";
import { Estado } from "./estado.model";
import { Tienda } from "./tienda.model";

export class Coleccion {
    id: number | undefined;
    base: Base | undefined;
    plataforma: Plataforma | undefined;
    idioma: Idioma | undefined;
    region: Region | undefined;
    estado_general: Estado | undefined;
    estado_caja: Estado | undefined;
    fecha_compra: string | undefined;
    fecha_recibo: string | undefined;
    unidades: number | undefined;
    coste: number | undefined;
    tienda: Tienda | undefined;
    notas: string | undefined;
    codigo: string | undefined;
}