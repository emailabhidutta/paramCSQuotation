import { Component } from '@angular/core';
import { navItems } from './nav';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  public navItems = navItems;

  perfectScrollbarConfig = {
    suppressScrollX: true,
  };
}
