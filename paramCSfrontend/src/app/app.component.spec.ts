import { TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { AppComponent } from './app.component';
import { Router, NavigationEnd } from '@angular/router';
import { of } from 'rxjs';

describe('AppComponent', () => {
  let component: AppComponent;
  let router: Router;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RouterTestingModule],
      declarations: [AppComponent],
    }).compileComponents();

    router = TestBed.inject(Router);
    const fixture = TestBed.createComponent(AppComponent);
    component = fixture.componentInstance;
  });

  it('should create the app', () => {
    expect(component).toBeTruthy();
  });

  it(`should have as title 'paramCSQuotation'`, () => {
    expect(component.title).toEqual('paramCSQuotation');
  });

  it('should set isLoginPage to true when on login page', () => {
    spyOn(router.events, 'pipe').and.returnValue(of(new NavigationEnd(1, '/login', '/login')));
    component.ngOnInit();
    expect(component.isLoginPage).toBeTruthy();
  });

  it('should set isLoginPage to false when not on login page', () => {
    spyOn(router.events, 'pipe').and.returnValue(of(new NavigationEnd(1, '/home', '/home')));
    component.ngOnInit();
    expect(component.isLoginPage).toBeFalsy();
  });
});
