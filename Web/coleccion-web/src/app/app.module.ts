import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { ToastrModule } from 'ngx-toastr';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { JuegosComponent } from './juego/juego.component';
import { JuegoTemplateComponent } from './juego-template/juego-template.component';
import { ColeccionComponent } from './coleccion/coleccion.component';
import { HistorialComponent } from './historial/historial.component';
import { RomsComponent } from './roms/roms.component';
import { RomsTemplateComponent } from './roms-template/roms-template.component';
import { HistorialTemplateComponent } from './historial-template/historial-template.component';
import { ColeccionTemplateComponent } from './coleccion-template/coleccion-template.component';

@NgModule({
  declarations: [
    AppComponent,
    JuegosComponent,
    JuegoTemplateComponent,
    ColeccionComponent,
    HistorialComponent,
    RomsComponent,
    RomsTemplateComponent,
    HistorialTemplateComponent,
    ColeccionTemplateComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    HttpClientModule,
    ToastrModule.forRoot()
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
