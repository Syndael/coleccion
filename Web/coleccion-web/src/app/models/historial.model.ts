import { Juego } from "./juego.model";
import { Plataforma } from "./plataforma.model";
import { Estado } from "./estado.model";

export class Historial {
    id: number | undefined;
    juego: Juego | undefined;
    plataforma: Plataforma | undefined;
    estado_jugado: Estado | undefined;
    porcentaje: number | undefined;
    horas: number | undefined;
    historia_completa: Boolean | undefined;
    notas: string | undefined;
    fecha_inicio: string | undefined;
    fecha_fin: string | undefined;
}