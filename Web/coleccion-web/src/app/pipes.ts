import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'ellipsis' })
export class EllipsisPipe implements PipeTransform {
  transform(valor: string | undefined, maxLength: number): string {
    if (!valor) {
      return '';
    }

    if (valor.length <= maxLength) {
      return valor;
    }

    return valor.slice(0, maxLength) + '...';
  }
}

@Pipe({ name: 'formateo' })
export class FormatPipe implements PipeTransform {
  transform(valor: any | undefined, simbolo: string): string {
    if (!valor) {
      return '';
    }
    return valor.toString() + simbolo;
  }
}
