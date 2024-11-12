import { ComponentFixture, TestBed } from '@angular/core/testing';

import { QuotesAcceptedComponent } from './quotes-accepted.component';

describe('QuotesAcceptedComponent', () => {
  let component: QuotesAcceptedComponent;
  let fixture: ComponentFixture<QuotesAcceptedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [QuotesAcceptedComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(QuotesAcceptedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
