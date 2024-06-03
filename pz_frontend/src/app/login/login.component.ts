import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  formData = {
      username: '',
      password: ''
    };
  loginError: boolean = false;

  constructor(private authService: AuthService, private router: Router) {}

  login() {

    if (this.authService.login(this.formData.username, this.formData.password)) {
      console.log('Zalogowano pomyślnie');
      this.router.navigate(['/dashboard']);

    } else {
      console.log('Błąd logowania. Sprawdź dane.');
      this.loginError = true;
    }
  }
}
