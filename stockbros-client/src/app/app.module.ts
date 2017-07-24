import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './component/login/login.component';
import { AlertComponent } from './component/alert/alert.component';
import { StocksComponent } from './component/stocks/stocks.component';
import { LoginService } from './service/login.service';
import { AlertService } from './service/alert.service';
import { StocksService } from './service/stocks.service';
import { AuthGuard } from './guard/auth.guard';

@NgModule({
  declarations: [ AppComponent, LoginComponent, AlertComponent, StocksComponent ],
  imports: [ BrowserModule, FormsModule, HttpModule, AppRoutingModule ],
  providers: [ LoginService, AlertService, AuthGuard, StocksService ],
  bootstrap: [AppComponent]
})
export class AppModule { }
