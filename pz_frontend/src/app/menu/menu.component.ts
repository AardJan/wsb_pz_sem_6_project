import { Component } from '@angular/core';
import { CommonModule } from "@angular/common";
import { AuthService } from '../auth.service';
import {RouterLink} from "@angular/router";

@Component({
  selector: 'app-menu',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './menu.component.html',
  styleUrl: './menu.component.css'
})
export class MenuComponent {
  isLoggedIn: boolean = true;

  // constructor(authService: AuthService) {
  //   this.isLoggedIn = authService.isLoggedIn;
  // }

}
