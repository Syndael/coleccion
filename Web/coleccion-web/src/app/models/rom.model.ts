import { Idioma } from "./idioma.model";
import { Base } from "./base.model";
import { Plataforma } from "./plataforma.model";
import { Region } from "./region.model";
import { TipoRom } from "./tipo-rom.model";

export class Rom {
    id: number | undefined;
    base: Base | undefined;
    plataforma: Plataforma | undefined;
    nombre_rom: string | undefined;
    nombre_rom_ext: string | undefined;
    idioma: Idioma | undefined;
    region: Region | undefined;
    tipo_rom: TipoRom | undefined;
    fecha_descarga: string | undefined;
}