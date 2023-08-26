import { Base } from "./base.model";
import { Plataforma } from "./plataforma.model";
import { Estado } from "./estado.model";

export class Progreso {
    id: number | undefined;
    base: Base | undefined;
    plataforma: Plataforma | undefined;
    estado_progreso: Estado | undefined;
    porcentaje: number | undefined;
    horas: number | undefined;
    historia_completa: Boolean | undefined;
    notas: string | undefined;
    fecha_inicio: string | undefined;
    fecha_fin: string | undefined;
    fecha_ultimo: string | undefined;
}