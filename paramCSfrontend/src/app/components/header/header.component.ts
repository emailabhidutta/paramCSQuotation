import { Component, OnInit, Input } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {
  @Input() sidebarId: string = "sidebar";

  currentPageTitle: string = 'Dashboard';
  notificationCount: number = 1800;
  userName: string = 'KSB Admin';

  constructor(
    private router: Router,
    private authService: AuthService
  ) { }

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
    const sidebar = document.querySelector('#' + this.sidebarId);
    if (sidebar) {
      sidebar.classList.toggle('hide');
    }
  }

  toggleNotifications() {
    console.log('Toggle notifications');
  }

  openSettings() {
    console.log('Open settings');
  }

  changeLanguage() {
    console.log('Change language');
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
