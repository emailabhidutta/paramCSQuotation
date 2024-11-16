import { Component, Input, Output, EventEmitter } from '@angular/core';
import { FormGroup, FormArray, FormBuilder, Validators, AbstractControl } from '@angular/forms';
import { MaterialDisplayOption } from '../../models/quotation.model';

@Component({
  selector: 'app-quote-line-items',
  templateUrl: './quote-line-items.component.html',
  styleUrls: ['./quote-line-items.component.scss']
})
export class QuoteLineItemsComponent {
  @Input() parentForm!: FormGroup;
  @Input() detailIndex!: number;
  @Output() itemsChanged = new EventEmitter<void>();

  materialDescriptionOptions = Object.values(MaterialDisplayOption);

  constructor(private fb: FormBuilder) { }

  get items(): FormArray {
    return this.parentForm.get('details')?.get(this.detailIndex.toString())?.get('items') as FormArray;
  }

  addItem(): void {
    this.items.push(this.createItemForm());
    this.itemsChanged.emit();
  }

  removeItem(index: number): void {
    this.items.removeAt(index);
    this.itemsChanged.emit();
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

  calculateOrderValue(index: number): void {
    const item = this.items.at(index);
    if (item instanceof FormGroup) {
      const pricePer = item.get('PricePer')?.value || 0;
      const quantity = item.get('OrderQuantity')?.value || 0;
      const discount = item.get('DiscountValue')?.value || 0;
      const surcharge = item.get('SurchargeValue')?.value || 0;
      const orderValue = (pricePer * quantity) - discount + surcharge;
      item.patchValue({ OrderValue: orderValue });
      this.itemsChanged.emit();
    }
  }

  updateMaterialDescription(materialDisplay: MaterialDisplayOption): void {
    this.items.controls.forEach((control: AbstractControl) => {
      if (control instanceof FormGroup) {
        let description = '';
        switch (materialDisplay) {
          case MaterialDisplayOption.Full:
            description = control.get('FullMaterialDescription')?.value || '';
            break;
          case MaterialDisplayOption.FourDigit:
            description = (control.get('MaterialDescription')?.value || '').substring(0, 4);
            break;
          case MaterialDisplayOption.Basic:
            description = control.get('BasicMaterialText')?.value || '';
            break;
          case MaterialDisplayOption.Drawing:
            description = control.get('DrawingNo')?.value || '';
            break;
        }
        control.patchValue({ MaterialDescription: description });
      }
    });
    this.itemsChanged.emit();
  }
}
