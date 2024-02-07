import { Base } from "./base.model";
import { Plataforma } from "./plataforma.model";
import { Estado } from "./estado.model";

export class Progreso {
    id: number | undefined;
    base: Base | undefined;
    plataforma: Plataforma | undefined;
    estado_progreso: Estado | undefined;
    horas: number | undefined;
    notas: string | undefined;
    fecha_ultimo: string | undefined;
}