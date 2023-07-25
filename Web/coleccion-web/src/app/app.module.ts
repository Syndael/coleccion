import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { JuegosComponent } from './juego/juego.component';
import { JuegoTemplateComponent } from './juego-template/juego-template.component';
import { ColeccionComponent } from './coleccion/coleccion.component';
import { HistorialComponent } from './historial/historial.component';
import { RomsComponent } from './roms/roms.component';
import { RomsTemplateComponent } from './roms-template/roms-template.component';

@NgModule({
  declarations: [
    AppComponent,
    JuegosComponent,
    JuegoTemplateComponent,
    ColeccionComponent,
    HistorialComponent,
    RomsComponent,
    RomsTemplateComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
