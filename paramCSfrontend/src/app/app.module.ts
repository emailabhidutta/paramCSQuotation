import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

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
import { ChartjsModule } from '@coreui/angular-chartjs';

// Import components
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { LoginComponent } from './components/login/login.component';
import { QuoteCreateComponent } from './components/quotes/quote-create/quote-create.component';
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

// Import interceptors
import { AuthInterceptor } from './auth.interceptor';

@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    LoginComponent,
    QuoteCreateComponent,
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
    ChartjsModule,
    WidgetModule
  ],
  providers: [
    IconSetService,
    AuthService,
    DashboardService,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    }
  ],
  bootstrap: [AppComponent],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class AppModule { }
