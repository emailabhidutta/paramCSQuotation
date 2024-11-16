import { NgModule, CUSTOM_ELEMENTS_SCHEMA, InjectionToken } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { environment } from '../environments/environment';

export const API_URL = new InjectionToken<string>('apiUrl');

// Import CoreUI modules
import {
  AvatarModule,
  BadgeModule,
  BreadcrumbModule,
  ButtonGroupModule,
  ButtonModule,
  CardModule,
  DropdownModule,
  FooterModule,
  FormModule,
  GridModule,
  HeaderModule,
  ListGroupModule,
  NavModule,
  ProgressModule,
  SharedModule,
  SidebarModule,
  TabsModule,
  UtilitiesModule,
  WidgetModule
} from '@coreui/angular';

import { IconModule, IconSetService } from '@coreui/icons-angular';
import { IconSetModule } from '@coreui/icons-angular';
import {
  cilMenu,
  cilBell,
  cilSettings,
  cilGlobeAlt,
  cilUser,
  cilAccountLogout
} from '@coreui/icons';

import { ChartjsModule } from '@coreui/angular-chartjs';

// Import components
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { LoginComponent } from './components/login/login.component';
// Remove this import as QuoteCreateComponent is now standalone
// import { QuoteCreateComponent } from './components/quotes/quote-create/quote-create.component';
import { QuotesAllComponent } from './components/quotes/quotes-all/quotes-all.component';
import { QuotesAcceptedComponent } from './components/quotes/quotes-accepted/quotes-accepted.component';
import { QuotesRejectedComponent } from './components/quotes/quotes-rejected/quotes-rejected.component';
import { QuotesCancelledComponent } from './components/quotes/quotes-cancelled/quotes-cancelled.component';
import { HeaderComponent } from './components/header/header.component';
import { FooterComponent } from './components/footer/footer.component';
import { UsersComponent } from './components/master/users/users.component';
import { RolesComponent } from './components/master/roles/roles.component';

// Import services
import { AuthService } from './services/auth.service';
import { DashboardService } from './services/dashboard.service';
import { CustomerService } from './services/customer.service';
import { MaterialService } from './services/material.service';
import { QuotationService } from './services/quotation.service';

// Import interceptors
import { AuthInterceptor } from './auth.interceptor';

@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    LoginComponent,
    // Remove QuoteCreateComponent from here
    QuotesAllComponent,
    QuotesAcceptedComponent,
    QuotesRejectedComponent,
    QuotesCancelledComponent,
    HeaderComponent,
    FooterComponent,
    UsersComponent,
    RolesComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    CommonModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule,
    FormsModule,
    RouterModule,
    AvatarModule,
    BadgeModule,
    BreadcrumbModule,
    ButtonGroupModule,
    ButtonModule,
    CardModule,
    DropdownModule,
    FooterModule,
    FormModule,
    GridModule,
    HeaderModule,
    ListGroupModule,
    NavModule,
    ProgressModule,
    SharedModule,
    SidebarModule,
    TabsModule,
    UtilitiesModule,
    IconModule,
    IconSetModule,
    ChartjsModule,
    WidgetModule,
    NgbModule
  ],
  providers: [
    IconSetService,
    AuthService,
    DashboardService,
    CustomerService,
    MaterialService,
    QuotationService,
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true },
    { provide: API_URL, useValue: environment.apiUrl }
  ],
  bootstrap: [AppComponent],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class AppModule {
  constructor(private iconSetService: IconSetService) {
    iconSetService.icons = {
      cilMenu,
      cilBell,
      cilSettings,
      cilGlobeAlt,
      cilUser,
      cilAccountLogout
    };
  }
}
