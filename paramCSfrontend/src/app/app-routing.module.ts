import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
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
import { AuthGuard } from './guards/auth.guard';

const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'dashboard', component: DashboardComponent, canActivate: [AuthGuard] },
  { path: 'quotes/create', component: QuoteCreateComponent, canActivate: [AuthGuard] },
  { path: 'quotes/all', component: QuotesAllComponent, canActivate: [AuthGuard] },
  { path: 'quotes/accepted', component: QuotesAcceptedComponent, canActivate: [AuthGuard] },
  { path: 'quotes/rejected', component: QuotesRejectedComponent, canActivate: [AuthGuard] },
  { path: 'quotes/cancelled', component: QuotesCancelledComponent, canActivate: [AuthGuard] },
  { path: 'quotes/:id', component: QuotationDetailComponent, canActivate: [AuthGuard] },
  { path: 'master/users', component: UsersComponent, canActivate: [AuthGuard] },
  { path: 'master/roles', component: RolesComponent, canActivate: [AuthGuard] },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
