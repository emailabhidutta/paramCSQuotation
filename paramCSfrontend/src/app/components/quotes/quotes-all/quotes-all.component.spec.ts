import { ComponentFixture, TestBed } from '@angular/core/testing';

import { QuotesAllComponent } from './quotes-all.component';

describe('QuotesAllComponent', () => {
  let component: QuotesAllComponent;
  let fixture: ComponentFixture<QuotesAllComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [QuotesAllComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(QuotesAllComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
