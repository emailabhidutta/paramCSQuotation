import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { QuotationService } from '../../../services/quotation.service';

@Component({
  selector: 'app-quote-create',
  templateUrl: './quote-create.component.html',
  styleUrls: ['./quote-create.component.css']
})
export class QuoteCreateComponent implements OnInit {
  quoteForm: FormGroup;
  loading = false;
  error = '';

  constructor(
    private fb: FormBuilder,
    private quotationService: QuotationService,
    private router: Router
  ) {
    this.quoteForm = this.fb.group({
      CustomerNumber: ['', Validators.required],
      CustomerInquiryNo: [''],
      Date: ['', Validators.required],
      // Add more form controls as needed
    });
  }

  ngOnInit(): void { }

  onSubmit(): void {
    if (this.quoteForm.valid) {
      this.loading = true;
      this.quotationService.createQuotation(this.quoteForm.value).subscribe(
        (response) => {
          this.loading = false;
          this.router.navigate(['/quotes/all']);
        },
        (error) => {
          this.loading = false;
          this.error = 'Failed to create quotation. Please try again.';
          console.error('Error creating quotation:', error);
        }
      );
    }
  }
}
