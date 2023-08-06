import { Plataforma } from "./plataforma.model";

export class BasePlataforma {
    id: number | undefined;
    base: number | undefined;
    plataforma: Plataforma | undefined;
    fecha: string | undefined;
}

export class BasePlataformaBeanNew {
    base: number | undefined;
    plataforma: number | undefined;
    fecha: string | undefined;
}