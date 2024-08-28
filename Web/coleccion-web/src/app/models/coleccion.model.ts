import { Idioma } from "./idioma.model";
import { Base } from "./base.model";
import { Edicion } from "./edicion.model";
import { Plataforma } from "./plataforma.model";
import { Region } from "./region.model";
import { Estado } from "./estado.model";
import { Tienda } from "./tienda.model";
import { Empresa } from "./empresa.model";

export class Coleccion {
    id: number | undefined;
    base: Base | undefined;
    edicion: Edicion | undefined;
    plataforma: Plataforma | undefined;
    idioma: Idioma | undefined;
    region: Region | undefined;
    estado_general: Estado | undefined;
    estado_caja: Estado | undefined;
    reparto: Empresa | undefined;
    fecha_reserva: string | undefined;
    fecha_compra: string | undefined;
    fecha_recibo: string | undefined;
    unidades: number | undefined;
    precio: number | undefined;
    envio: number | undefined;
    coste: number | undefined;
    reparto_seguimiento: string | undefined;
    tienda: Tienda | undefined;
    url: string | undefined;
    ig: string | undefined;
    notas: string | undefined;
    codigo: string | undefined;
    mascara_aux: string | undefined;
}