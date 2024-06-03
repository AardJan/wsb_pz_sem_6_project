import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LoginComponent } from './login.component';
import {By} from "@angular/platform-browser";

describe('LoginComponent', () => {
  let component: LoginComponent;
  let fixture: ComponentFixture<LoginComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LoginComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LoginComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should have a form with required fields', () => {
    const usernameField = fixture.debugElement.query(By.css('input[name="username"]')).nativeElement;
    const passwordField = fixture.debugElement.query(By.css('input[name="password"]')).nativeElement;
    const submitButton = fixture.debugElement.query(By.css('button[type="submit"]')).nativeElement;

    expect(usernameField).toBeTruthy();
    expect(passwordField).toBeTruthy();
    expect(submitButton).toBeTruthy();
    expect(usernameField.getAttribute('required')).toBe('');
    expect(passwordField.getAttribute('required')).toBe('');
  });

  it('should call login() method when form is submitted', () => {
    spyOn(component, 'login');
    const form = fixture.debugElement.query(By.css('form')).nativeElement;
    form.dispatchEvent(new Event('submit'));
    fixture.detectChanges();
    expect(component.login).toHaveBeenCalled();
  });

  it('should display an error message for invalid login', () => {
    const usernameField = fixture.debugElement.query(By.css('input[name="username"]')).nativeElement;
    const passwordField = fixture.debugElement.query(By.css('input[name="password"]')).nativeElement;
    const submitButton = fixture.debugElement.query(By.css('button[type="submit"]')).nativeElement;

    usernameField.value = 'exampleUser';
    passwordField.value = 'invalidPassword';
    usernameField.dispatchEvent(new Event('input'));
    passwordField.dispatchEvent(new Event('input'));
    submitButton.click();
    fixture.detectChanges();

    const errorMessage = fixture.debugElement.query(By.css('.error-message')).nativeElement;
    expect(errorMessage).toBeTruthy();
  });

  it('should log in for valid username and password', () => {
    const usernameField = fixture.debugElement.query(By.css('input[name="username"]')).nativeElement;
    const passwordField = fixture.debugElement.query(By.css('input[name="password"]')).nativeElement;
    const submitButton = fixture.debugElement.query(By.css('button[type="submit"]')).nativeElement;

    usernameField.value = 'przykladowyUzytkownik';
    passwordField.value = 'przykladoweHaslo';
    usernameField.dispatchEvent(new Event('input'));
    passwordField.dispatchEvent(new Event('input'));
    submitButton.click();
    fixture.detectChanges();

    const errorMessage = fixture.debugElement.query(By.css('.error-message'));
    expect(errorMessage).toBeFalsy();
  });
});
