import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

// Import CoreUI Modules
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
  UtilitiesModule
} from '@coreui/angular';

import { IconModule, IconSetService } from '@coreui/icons-angular';
import { PerfectScrollbarModule } from 'ngx-perfect-scrollbar';

// Import ng2-charts
import { NgChartsModule } from 'ng2-charts';

// Import components
import { HeaderComponent } from './components/header/header.component';
import { FooterComponent } from './components/footer/footer.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { LoginComponent } from './components/login/login.component';
import { UsersComponent } from './components/master/users/users.component';
import { RolesComponent } from './components/master/roles/roles.component';
import { QuoteCreateComponent } from './components/quotes/quote-create/quote-create.component';
import { QuotesAllComponent } from './components/quotes/quotes-all/quotes-all.component';
import { QuotesAcceptedComponent } from './components/quotes/quotes-accepted/quotes-accepted.component';
import { QuotesRejectedComponent } from './components/quotes/quotes-rejected/quotes-rejected.component';
import { QuotesCancelledComponent } from './components/quotes/quotes-cancelled/quotes-cancelled.component';
import { QuotationDetailComponent } from './components/quotes/quotation-detail/quotation-detail.component';
import { QuotationListComponent } from './components/quotes/quotation-list/quotation-list.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    FooterComponent,
    DashboardComponent,
    LoginComponent,
    UsersComponent,
    RolesComponent,
    QuoteCreateComponent,
    QuotesAllComponent,
    QuotesAcceptedComponent,
    QuotesRejectedComponent,
    QuotesCancelledComponent,
    QuotationDetailComponent,
    QuotationListComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    ReactiveFormsModule,
    HttpClientModule,
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
    PerfectScrollbarModule,
    NgChartsModule  // Add this line
  ],
  providers: [IconSetService],
  bootstrap: [AppComponent]
})
export class AppModule { }
