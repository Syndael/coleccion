import { TipoBase } from "./tipo-base.model";

export class Base {
    id: number | undefined;
    tipo_base: TipoBase | undefined;
    nombre: string | undefined;
    codigo: string | undefined;
    saga: string | undefined;
    url: string | undefined;
    fecha_salida: string | undefined;
    plataformas: string | undefined;
}