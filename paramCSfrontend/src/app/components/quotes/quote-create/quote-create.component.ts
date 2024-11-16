import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormArray, Validators, AbstractControl } from '@angular/forms';
import { Router } from '@angular/router';
import { QuotationService } from '../../../services/quotation.service';
import { CustomerService } from '../../../services/customer.service';
import { MaterialService } from '../../../services/material.service';
import { Quotation, QuotationStatus, SalesOrganization, Currency, CustomerMaster, MaterialMaster, MaterialDisplayOption, ApprovalStatus } from '../../../models/quotation.model';
import { Observable, forkJoin, of } from 'rxjs';
import { debounceTime, distinctUntilChanged, switchMap, catchError, finalize } from 'rxjs/operators';

@Component({
  selector: 'app-quote-create',
  templateUrl: './quote-create.component.html',
  styleUrls: ['./quote-create.component.css']
})
export class QuoteCreateComponent implements OnInit {
  quotationForm!: FormGroup;
  quotationStatuses: QuotationStatus[] = [];
  salesOrganizations: SalesOrganization[] = [];
  currencies: Currency[] = [];
  materialDescriptionOptions = Object.values(MaterialDisplayOption);
  loading = false;
  error: string | null = null;

  constructor(
    private fb: FormBuilder,
    private quotationService: QuotationService,
    private customerService: CustomerService,
    private materialService: MaterialService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.initForm();
    this.loadInitialData();
  }

  initForm(): void {
    this.quotationForm = this.fb.group({
      QuotationNo: [''],
      CustomerNumber: ['', Validators.required],
      LastRevision: ['00'],
      CustomerInquiryNo: [''],
      Date: [new Date().toISOString().split('T')[0], Validators.required],
      CreationDate: [{ value: new Date().toISOString().split('T')[0], disabled: true }],
      QStatusID: ['', Validators.required],
      QuoteValidFrom: ['', Validators.required],
      QuoteValidUntil: ['', Validators.required],
      CustomerEmail: ['', [Validators.email]],
      Version: [1],
      Remarks: [''],
      GSTVATValue: [0, [Validators.required, Validators.min(0)]],
      TotalDiscount: [0, [Validators.required, Validators.min(0)]],
      total_value: [{ value: 0, disabled: true }],
      details: this.fb.array([this.createDetailForm()])
    });

    // Add listeners for GSTVATValue and TotalDiscount
    this.quotationForm.get('GSTVATValue')?.valueChanges.subscribe(() => this.calculateTotals());
    this.quotationForm.get('TotalDiscount')?.valueChanges.subscribe(() => this.calculateTotals());
  }

  createDetailForm(): FormGroup {
    return this.fb.group({
      QuoteRevisionNo: ['01'],
      QuoteRevisionDate: [new Date().toISOString().split('T')[0]],
      SalesOrganization: ['', Validators.required],
      CustomerInquiryNo: [''],
      SoldToCustomerNumber: [''],
      ShipToCustomerNumber: [''],
      SalesGroup: [''],
      Customer: [''],
      CustomerName: [''],
      CustomerName2: [''],
      IndustryCode1: [''],
      CustPriceProcedure: [''],
      MaterialDisplay: [MaterialDisplayOption.Full],
      TermOfPayment: [''],
      Incoterms: [''],
      IncotermsPart2: [''],
      TradingCurrency: ['', Validators.required],
      SalesEmployeeNo: [''],
      DeliveryDate: [''],
      CustomerPONumber: [''],
      ApprovalStatus: [ApprovalStatus.Pending],
      Version: [1],
      PaymentTerms: [''],
      DeliveryMethod: [''],
      items: this.fb.array([this.createItemForm()])
    });
  }

  createItemForm(): FormGroup {
    return this.fb.group({
      MaterialNumber: ['', Validators.required],
      CustomerMatNumber: [''],
      FullMaterialDescription: [''],
      MaterialDescription: ['', Validators.required],
      BasicMaterialText: [''],
      DrawingNo: [''],
      PricePer: [0, [Validators.required, Validators.min(0)]],
      Per: [1, [Validators.required, Validators.min(1)]],
      UnitOfMeasure: ['', Validators.required],
      DiscountValue: [0, [Validators.required, Validators.min(0)]],
      SurchargeValue: [0, [Validators.required, Validators.min(0)]],
      OrderQuantity: [0, [Validators.required, Validators.min(0)]],
      OrderValue: [{ value: 0, disabled: true }],
      ItemText: [''],
      Usage: [''],
      IsDeleted: [false]
    });
  }

  get details(): FormArray {
    return this.quotationForm.get('details') as FormArray;
  }

  addDetail(): void {
    this.details.push(this.createDetailForm());
  }

  removeDetail(index: number): void {
    this.details.removeAt(index);
    this.calculateTotals();
  }

  getItems(detailIndex: number): FormArray {
    return this.details.at(detailIndex).get('items') as FormArray;
  }

  addItem(detailIndex: number): void {
    const items = this.getItems(detailIndex);
    items.push(this.createItemForm());
  }

  removeItem(detailIndex: number, itemIndex: number): void {
    const items = this.getItems(detailIndex);
    items.removeAt(itemIndex);
    this.calculateTotals();
  }

  loadInitialData(): void {
    this.loading = true;
    this.error = null;
    forkJoin({
      statuses: this.quotationService.getQuotationStatuses(),
      organizations: this.quotationService.getSalesOrganizations(),
      currencies: this.quotationService.getCurrencies()
    }).pipe(
      catchError(error => {
        console.error('Error loading initial data', error);
        this.error = 'Failed to load initial data. Please try again.';
        return of({ statuses: [], organizations: [], currencies: [] });
      }),
      finalize(() => this.loading = false)
    ).subscribe(({ statuses, organizations, currencies }) => {
      this.quotationStatuses = statuses;
      this.salesOrganizations = organizations;
      this.currencies = currencies;
    });
  }

  searchCustomer = (text$: Observable<string>) =>
    text$.pipe(
      debounceTime(300),
      distinctUntilChanged(),
      switchMap(term => term.length < 2 ? of([]) : this.customerService.searchCustomers(term)),
      catchError(() => {
        this.error = 'Error searching for customers. Please try again.';
        return of([]);
      })
    )

  onCustomerSelect(customer: CustomerMaster): void {
    this.quotationForm.patchValue({
      CustomerNumber: customer.CustomerNumber,
      CustomerEmail: customer.Email
    });
    // Update other fields based on the selected customer
    const firstDetail = this.details.at(0);
    if (firstDetail) {
      firstDetail.patchValue({
        SoldToCustomerNumber: customer.CustomerNumber,
        CustomerName: customer.CustomerName1,
        CustomerName2: customer.CustomerName2,
        CustPriceProcedure: customer.CustPriceProcedure,
        TermOfPayment: customer.PaymentTerm,
        Incoterms: customer.Incoterms
      });
    }
  }

  searchMaterial = (text$: Observable<string>) =>
    text$.pipe(
      debounceTime(300),
      distinctUntilChanged(),
      switchMap(term => term.length < 2 ? of([]) : this.materialService.searchMaterials(term)),
      catchError(() => {
        this.error = 'Error searching for materials. Please try again.';
        return of([]);
      })
    )

  onMaterialSelect(material: MaterialMaster, detailIndex: number, itemIndex: number): void {
    const items = this.getItems(detailIndex);
    const item = items.at(itemIndex);
    if (item) {
      item.patchValue({
        MaterialNumber: material.MaterialNumber,
        MaterialDescription: material.MaterialDescription,
        FullMaterialDescription: material.FullMaterialDescription,
        BasicMaterialText: material.BasicMaterialText,
        DrawingNo: material.DrawingNumber,
        UnitOfMeasure: material.UnitOfMeasure,
        PricePer: material.BasePrice || 0
      });
      this.calculateOrderValue(detailIndex, itemIndex);
    }
  }

  calculateOrderValue(detailIndex: number, itemIndex: number): void {
    const items = this.getItems(detailIndex);
    const item = items.at(itemIndex);
    if (item) {
      const pricePer = item.get('PricePer')?.value || 0;
      const quantity = item.get('OrderQuantity')?.value || 0;
      const discount = item.get('DiscountValue')?.value || 0;
      const surcharge = item.get('SurchargeValue')?.value || 0;
      const orderValue = (pricePer * quantity) - discount + surcharge;
      item.patchValue({ OrderValue: orderValue });
      this.calculateTotals();
    }
  }

  calculateTotals(): void {
    let totalValue = 0;

    this.details.controls.forEach((detail: AbstractControl) => {
      const items = (detail as FormGroup).get('items') as FormArray;
      if (items) {
        items.controls.forEach((item: AbstractControl) => {
          totalValue += (item as FormGroup).get('OrderValue')?.value || 0;
        });
      }
    });

    // Get the manually entered GSTVATValue and TotalDiscount
    const gstVatValue = this.quotationForm.get('GSTVATValue')?.value || 0;
    const totalDiscount = this.quotationForm.get('TotalDiscount')?.value || 0;

    // Calculate the final total value
    const finalTotalValue = totalValue - totalDiscount + gstVatValue;

    this.quotationForm.patchValue({
      total_value: finalTotalValue
    });
  }

  onSubmit(): void {
    if (this.quotationForm.valid) {
      this.loading = true;
      this.error = null;
      const formValue = this.quotationForm.getRawValue();
      this.quotationService.createQuotation(formValue).pipe(
        catchError(error => {
          console.error('Error creating quotation', error);
          this.error = 'Failed to create quotation. Please try again.';
          return of(null);
        }),
        finalize(() => this.loading = false)
      ).subscribe(response => {
        if (response) {
          console.log('Quotation created successfully', response);
          this.router.navigate(['/quotations', response.QuoteId]);
        }
      });
    } else {
      this.error = 'Please fill in all required fields correctly.';
      this.markFormGroupTouched(this.quotationForm);
    }
  }

  markFormGroupTouched(formGroup: FormGroup | FormArray) {
    Object.values(formGroup.controls).forEach(control => {
      if (control instanceof FormGroup || control instanceof FormArray) {
        this.markFormGroupTouched(control);
      } else {
        control.markAsTouched();
      }
    });
  }

  updateMaterialDescription(detailIndex: number): void {
    const detail = this.details.at(detailIndex);
    if (detail) {
      const materialDisplay = detail.get('MaterialDisplay')?.value;
      const items = this.getItems(detailIndex);
      items.controls.forEach((item: AbstractControl) => {
        let description = '';
        switch (materialDisplay) {
          case MaterialDisplayOption.Full:
            description = (item as FormGroup).get('FullMaterialDescription')?.value || '';
            break;
          case MaterialDisplayOption.FourDigit:
            description = ((item as FormGroup).get('MaterialDescription')?.value || '').substring(0, 4);
            break;
          case MaterialDisplayOption.Basic:
            description = (item as FormGroup).get('BasicMaterialText')?.value || '';
            break;
          case MaterialDisplayOption.Drawing:
            description = (item as FormGroup).get('DrawingNo')?.value || '';
            break;
        }
        (item as FormGroup).patchValue({ MaterialDescription: description });
      });
    }
  }
}
