import { Injectable, Optional } from '@angular/core';
import { Observable, of } from 'rxjs';
import { ToastrService } from 'ngx-toastr';

@Injectable({ providedIn: 'root', })
export class ErrorService {

    constructor(
        @Optional() private toastr: ToastrService
    ) { }

    public handleError<T>(operation = 'operation', result?: T) {
        return (error: any): Observable<T> => {
            this.toastr.error('Se ha producido un error durante la conexión al servidor.', 'Error', {
                timeOut: 6000,
                closeButton: true
            });
            console.error(error);
            return of(result as T);
        };
    }

    public printError(texto: string) {
        this.toastr.error(texto, 'Error', {
            timeOut: 6000,
            closeButton: true
        });
    }
}