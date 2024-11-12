import { ComponentFixture, TestBed } from '@angular/core/testing';

import { QuotesRejectedComponent } from './quotes-rejected.component';

describe('QuotesRejectedComponent', () => {
  let component: QuotesRejectedComponent;
  let fixture: ComponentFixture<QuotesRejectedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [QuotesRejectedComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(QuotesRejectedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
