import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';

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
  SpinnerModule,
  TabsModule,
  UtilitiesModule,
  WidgetModule
} from '@coreui/angular';

import { IconModule, IconSetService } from '@coreui/icons-angular';

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
    SpinnerModule,
    TabsModule,
    UtilitiesModule,
    IconModule,
    WidgetModule,
  ],
  providers: [
    IconSetService,
  ],
  bootstrap: [AppComponent],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class AppModule { }
