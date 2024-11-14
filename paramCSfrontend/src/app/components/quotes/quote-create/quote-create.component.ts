import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormArray } from '@angular/forms';
import { QuotationService } from '../../../services/quotation.service'; // Update this path as needed

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
    this.quotationForm = this.fb.group({}); // Initialize here
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

    this.addLineItem(); // Add an initial line item
  }

  getDefaultValidToDate(): string {
    const date = new Date();
    date.setMonth(date.getMonth() + 1);
    return date.toISOString().split('T')[0];
  }

  loadQuotationStatuses(): void {
    // TODO: Load quotation statuses from API
    this.quotationStatuses = [
      { QStatusID: '1', QStatusName: 'Draft' },
      { QStatusID: '2', QStatusName: 'Submitted' },
      { QStatusID: '3', QStatusName: 'Approved' },
      { QStatusID: '4', QStatusName: 'Rejected' }
    ];
  }

  get lineItems() {
    return this.quotationForm.get('lineItems') as FormArray;
  }

  addLineItem() {
    const lineItem = this.createLineItem();
    this.lineItems.push(lineItem);
  }

  createLineItem(): FormGroup {
    return this.fb.group({
      item: [''],
      materialNo: [''],
      materialDescription: [''],
      perPrice: [0],
      per: [1],
      uom: [''],
      discountValue: [0],
      surchargeValue: [0],
      orderQuantity: [0],
      orderValue: [0],
      itemText: [''],
      usage: [''],
      projectId: ['']
    });
  }

  removeLineItem(index: number) {
    this.lineItems.removeAt(index);
    this.calculateTotalSalesValue();
  }

  calculateOrderValue(index: number) {
    const item = this.lineItems.at(index);
    const perPrice = item.get('perPrice')?.value ?? 0;
    const quantity = item.get('orderQuantity')?.value ?? 0;
    const discount = item.get('discountValue')?.value ?? 0;
    const surcharge = item.get('surchargeValue')?.value ?? 0;

    const orderValue = (perPrice - discount + surcharge) * quantity;
    item.patchValue({ orderValue: orderValue });

    this.calculateTotalSalesValue();
  }

  calculateTotalSalesValue() {
    this.totalSalesValue = this.lineItems.controls.reduce((total, item) => {
      return total + (item.get('orderValue')?.value ?? 0);
    }, 0);
  }

  onSubmit(): void {
    if (this.quotationForm.valid) {
      this.loading = true;
      this.quotationService.createQuotation(this.quotationForm.value).subscribe(
        (response: any) => {
          console.log('Quotation created successfully', response);
          this.loading = false;
          // Handle success (e.g., show success message, navigate to quotation list)
        },
        (error: any) => {
          console.error('Error creating quotation', error);
          this.loading = false;
          // Handle error (e.g., show error message)
        }
      );
    }
  }
}
