import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';
import { navItems } from './nav';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  public navItems = navItems;
  public isLoginPage = false;
  title = 'paramCSQuotation'; // Add this line to resolve the test error

  constructor(private router: Router) { }

  ngOnInit() {
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe((event: NavigationEnd) => {
      // Check if the current route starts with '/login'
      this.isLoginPage = event.urlAfterRedirects.startsWith('/login');
      console.log('Is Login Page:', this.isLoginPage); // Debugging line
    });
  }
}
