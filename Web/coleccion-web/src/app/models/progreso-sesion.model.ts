import { Progreso } from "./progreso.model";
import { BaseDlc } from "./base-dlc.model";

export class ProgresoSesion {
    id: number | undefined;
    progreso: Progreso | undefined;
    base_dlc: BaseDlc | undefined;
    fecha_inicio: string | undefined;
    fecha_fin: string | undefined;
    horas: number | undefined;
    fecha_h_inicio: string | undefined;
    fecha_h_fin: string | undefined;
    horas_h: number | undefined;
    notas: string | undefined;
    nombre: string | undefined;
}