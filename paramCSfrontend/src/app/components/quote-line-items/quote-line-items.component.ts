import { Component, Input, OnInit } from '@angular/core';
import { FormArray, FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-quote-line-items',
  templateUrl: './quote-line-items.component.html',
  styleUrls: ['./quote-line-items.component.scss']
})
export class QuoteLineItemsComponent implements OnInit {
  @Input() parentForm!: FormGroup;

  constructor(private fb: FormBuilder) { }

  ngOnInit() {
    if (!this.parentForm) {
      console.error('ParentForm is not provided to QuoteLineItemsComponent');
    }
  }

  get lineItems(): FormArray {
    return this.parentForm.get('lineItems') as FormArray;
  }

  addLineItem() {
    const lineItem = this.fb.group({
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

    this.lineItems.push(lineItem);
  }

  removeLineItem(index: number) {
    this.lineItems.removeAt(index);
  }

  calculateOrderValue(index: number) {
    const item = this.lineItems.at(index);
    const perPrice = item.get('perPrice')?.value ?? 0;
    const quantity = item.get('orderQuantity')?.value ?? 0;
    const discount = item.get('discountValue')?.value ?? 0;
    const surcharge = item.get('surchargeValue')?.value ?? 0;

    const orderValue = (perPrice - discount + surcharge) * quantity;
    item.patchValue({ orderValue: orderValue });
  }
}
