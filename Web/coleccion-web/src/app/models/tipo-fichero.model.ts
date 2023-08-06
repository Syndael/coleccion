export class TipoFichero {
    id: number | undefined;
    descripcion: string | undefined;
}

export enum TipoFicheroEnum {
    FOTO = 'Foto',
    FACTURA = 'Factura'
}