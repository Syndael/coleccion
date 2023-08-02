import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { ToastrModule } from 'ngx-toastr';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { JuegosComponent } from './components/juego/juego.component';
import { JuegoTemplateComponent } from './components/juego-template/juego-template.component';
import { ColeccionComponent } from './components/coleccion/coleccion.component';
import { EllipsisPipe, FormatPipe } from './pipes';
import { HistorialComponent } from './components/historial/historial.component';
import { RomsComponent } from './components/roms/roms.component';
import { RomsTemplateComponent } from './components/roms-template/roms-template.component';
import { HistorialTemplateComponent } from './components/historial-template/historial-template.component';
import { ColeccionTemplateComponent } from './components/coleccion-template/coleccion-template.component';

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
    ColeccionTemplateComponent,
    EllipsisPipe,
    FormatPipe
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
