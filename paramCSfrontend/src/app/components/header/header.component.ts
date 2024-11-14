import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  currentPageTitle: string = 'Dashboard';
  notificationCount: number = 1800;
  userName: string = 'KSB Admin';

  constructor(private router: Router) { }

  ngOnInit() {
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe((event: NavigationEnd) => {
      this.updatePageTitle(event.urlAfterRedirects);
    });
  }

  updatePageTitle(url: string) {
    const segments = url.split('/').filter(segment => segment);
    if (segments.length > 0) {
      this.currentPageTitle = segments[segments.length - 1]
        .split('-')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
    } else {
      this.currentPageTitle = 'Dashboard';
    }
  }

  toggleSidebar() {
    document.body.classList.toggle('sidebar-show');
  }

  toggleNotifications() {
    console.log('Toggle notifications');
    // Implement notification toggle functionality
  }

  openSettings() {
    console.log('Open settings');
    // Implement settings functionality
  }

  changeLanguage() {
    console.log('Change language');
    // Implement language change functionality
  }

  toggleUserMenu() {
    console.log('Toggle user menu');
    // Implement user menu toggle functionality
  }
}
