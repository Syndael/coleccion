import { Plataforma } from "./plataforma.model";

export class Edicion {
    id: number | undefined;
    base: number | undefined;
    plataforma: Plataforma | undefined;
    nombre: string | undefined;
    fecha: string | undefined;
}

export class EdicionBeanNew {
    base: number | undefined;
    plataforma: number | undefined;
    nombre: string | undefined;
    fecha: string | undefined;
}