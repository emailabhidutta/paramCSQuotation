import { ComponentFixture, TestBed } from '@angular/core/testing';

import { QuotesCancelledComponent } from './quotes-cancelled.component';

describe('QuotesCancelledComponent', () => {
  let component: QuotesCancelledComponent;
  let fixture: ComponentFixture<QuotesCancelledComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [QuotesCancelledComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(QuotesCancelledComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
