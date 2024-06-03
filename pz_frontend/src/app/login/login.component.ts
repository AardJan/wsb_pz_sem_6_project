import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule
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

  login() {

    if (this.formData.username === 'przykladowyUzytkownik' && this.formData.password === 'przykladoweHaslo') {
      console.log('Zalogowano pomyślnie');
      this.loginError = false;
    } else {
      console.log('Błąd logowania. Sprawdź dane.');
      this.loginError = true;
    }
  }
}
