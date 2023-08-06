import { Coleccion } from "./coleccion.model";
import { TipoFichero } from "./tipo-fichero.model";

export class Fichero {
    id: number | undefined;
    ruta: string | undefined;
    nombre_original: string | undefined;
    nombre_almacenado: string | undefined;
    tipo_fichero: TipoFichero | undefined;
    coleccion: Coleccion | undefined;
}

export class DatoFichero {
    id: number | undefined;
    nombre_final: string | undefined;
    nombre_original: string | undefined;
    tipo_fichero: string | undefined;
    url: string | undefined;
}