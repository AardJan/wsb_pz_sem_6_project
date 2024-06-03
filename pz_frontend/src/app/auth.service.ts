import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  isLoggedIn = false;

  login(username: string, password: string): boolean {
    this.isLoggedIn = username === 'przykladowyUzytkownik' && password === 'przykladoweHaslo';
    return this.isLoggedIn;
  }

  logout() {
    this.isLoggedIn = false;
  }
}
