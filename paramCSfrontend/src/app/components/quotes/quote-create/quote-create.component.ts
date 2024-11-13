import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { QuotationService } from '../../../services/quotation.service';

@Component({
  selector: 'app-quote-create',
  templateUrl: './quote-create.component.html',
  styleUrls: ['./quote-create.component.css']
})
export class QuoteCreateComponent implements OnInit {
  quotationForm: FormGroup;
  loading = false;
  quotationStatuses: any[] = [];

  constructor(
    private fb: FormBuilder,
    private quotationService: QuotationService
  ) { }

  ngOnInit() {
    this.quotationForm = this.fb.group({
      customerNumber: ['', Validators.required],
      customerEmail: ['', Validators.email],
      customerInquiryNo: [''],
      quoteValidFrom: [''],
      quoteValidUntil: [''],
      statusId: ['', Validators.required]
    });

    this.loadQuotationStatuses();
  }

  loadQuotationStatuses() {
    this.quotationService.getQuotationStatuses().subscribe(
      (statuses) => {
        this.quotationStatuses = statuses;
      },
      (error) => {
        console.error('Error loading quotation statuses', error);
      }
    );
  }

  onSubmit() {
    if (this.quotationForm.valid) {
      this.loading = true;
      this.quotationService.createQuotation(this.quotationForm.value).subscribe(
        (response) => {
          console.log('Quotation created successfully', response);
          this.loading = false;
          // Add logic to navigate to the quotation list or show a success message
        },
        (error) => {
          console.error('Error creating quotation', error);
          this.loading = false;
          // Add logic to show an error message
        }
      );
    }
  }
}
