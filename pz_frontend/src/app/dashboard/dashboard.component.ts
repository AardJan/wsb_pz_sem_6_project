import { Component } from '@angular/core';
import { MenuComponent } from '../menu/menu.component';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [MenuComponent],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent {
  isLoggedIn: boolean = false;

  constructor(authService: AuthService) {
    this.isLoggedIn = authService.isLoggedIn;
  }
}
