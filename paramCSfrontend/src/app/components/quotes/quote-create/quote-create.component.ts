import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { QuotationService } from '../../../services/quotation.service';

@Component({
  selector: 'app-quote-create',
  templateUrl: './quote-create.component.html',
  styleUrls: ['./quote-create.component.scss']  // Changed to .scss
})
export class QuoteCreateComponent implements OnInit {
  quotationForm: FormGroup;
  loading = false;
  quotationStatuses: any[] = [];

  constructor(
    private fb: FormBuilder,
    private quotationService: QuotationService
  ) {
    // Initialize the form in the constructor
    this.quotationForm = this.fb.group({
      customerNumber: ['', Validators.required],
      customerEmail: ['', [Validators.required, Validators.email]],
      customerInquiryNo: [''],
      quoteValidFrom: ['', Validators.required],
      quoteValidUntil: ['', Validators.required],
      statusId: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    this.loadQuotationStatuses();
  }

  loadQuotationStatuses(): void {
    this.quotationService.getQuotationStatuses().subscribe({
      next: (statuses) => {
        this.quotationStatuses = statuses;
      },
      error: (error) => {
        console.error('Error loading quotation statuses', error);
      }
    });
  }

  onSubmit(): void {
    if (this.quotationForm.valid) {
      this.loading = true;
      this.quotationService.createQuotation(this.quotationForm.value).subscribe({
        next: (response) => {
          console.log('Quotation created successfully', response);
          this.loading = false;
          // Add logic to navigate to the quotation list or show a success message
        },
        error: (error) => {
          console.error('Error creating quotation', error);
          this.loading = false;
          // Add logic to show an error message
        }
      });
    }
  }
}
