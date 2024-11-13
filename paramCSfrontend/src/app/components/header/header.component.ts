import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent {
  constructor(private authService: AuthService, private router: Router) { }

  toggleSidebar() {
    // Implement sidebar toggle logic here
    // For example, you might emit an event or call a service method
    console.log('Sidebar toggled');
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
