import { Idioma } from "./idioma.model";
import { Juego } from "./juego.model";
import { Plataforma } from "./plataforma.model";
import { Region } from "./region.model";
import { TipoRom } from "./tipo-rom.model";

export class lista {
    idiomas: Idioma[] = [];
    juegos: Juego[] = [];
    plataformas: Plataforma[] = [];
    regiones: Region[] = [];
    tipo_roms: TipoRom[] = [];
}