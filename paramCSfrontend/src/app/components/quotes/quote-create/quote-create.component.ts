import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormArray } from '@angular/forms';
import { QuotationService } from '../../../services/quotation.service';

@Component({
  selector: 'app-quote-create',
  templateUrl: './quote-create.component.html',
  styleUrls: ['./quote-create.component.css']
})
export class QuoteCreateComponent implements OnInit {
  quotationForm: FormGroup;
  quotationStatuses: any[] = [];
  loading = false;
  totalSalesValue = 0;

  constructor(
    private fb: FormBuilder,
    private quotationService: QuotationService
  ) {
    this.quotationForm = this.fb.group({});
  }

  ngOnInit(): void {
    this.initForm();
    this.loadQuotationStatuses();
  }

  initForm(): void {
    this.quotationForm = this.fb.group({
      sapQuotationNo: [''],
      revNo: ['00'],
      creationDate: [new Date().toISOString().split('T')[0], Validators.required],
      customerInquiryNo: [''],
      customer: ['', Validators.required],
      customerName1: [''],
      customerName2: [''],
      customerAddress: [''],
      custPriceProc: [''],
      paymentTerm: [''],
      tradingCurrency: [''],
      incoterm: [''],
      incotermPort: [''],
      deliveryDate: [''],
      validFromDate: [new Date().toISOString().split('T')[0], Validators.required],
      validToDate: [this.getDefaultValidToDate(), Validators.required],
      headerText: [''],
      materialDetailsPrint: ['full'],
      salesPerson: [''],
      salesPersonEmail: ['', Validators.email],
      salesPersonPhone: [''],
      lineItems: this.fb.array([]),
      headerTotalDiscount: [0],
      gstVatValue: [0]
    });
  }

  getDefaultValidToDate(): string {
    const date = new Date();
    date.setMonth(date.getMonth() + 1);
    return date.toISOString().split('T')[0];
  }

  loadQuotationStatuses(): void {
    this.quotationService.getQuotationStatuses().subscribe(
      (statuses) => {
        this.quotationStatuses = statuses;
      },
      (error) => {
        console.error('Error loading quotation statuses', error);
      }
    );
  }

  get lineItems(): FormArray {
    return this.quotationForm.get('lineItems') as FormArray;
  }

  onLineItemsChanged(): void {
    this.calculateTotalSalesValue();
  }

  calculateTotalSalesValue(): void {
    let total = 0;
    for (let item of this.lineItems.controls) {
      total += item.get('orderValue')?.value ?? 0;
    }
    total -= this.quotationForm.get('headerTotalDiscount')?.value ?? 0;
    total += this.quotationForm.get('gstVatValue')?.value ?? 0;
    this.totalSalesValue = total;
  }

  onSubmit(): void {
    if (this.quotationForm.valid) {
      this.loading = true;
      this.quotationService.createQuotation(this.quotationForm.value).subscribe(
        (response) => {
          console.log('Quotation created successfully', response);
          this.loading = false;
          // TODO: Navigate to quotation list or show success message
        },
        (error) => {
          console.error('Error creating quotation', error);
          this.loading = false;
          // TODO: Show error message to user
        }
      );
    }
  }
}
