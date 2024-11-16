import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { FormGroup, FormArray, FormBuilder, Validators, AbstractControl } from '@angular/forms';
import { MaterialDisplayOption } from '../../models/quotation.model';
import { Observable } from 'rxjs';
import { debounceTime, distinctUntilChanged, map } from 'rxjs/operators';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { NgbTypeaheadModule } from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-quote-line-items',
  templateUrl: './quote-line-items.component.html',
  styleUrls: ['./quote-line-items.component.scss'],
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, NgbTypeaheadModule]
})
export class QuoteLineItemsComponent implements OnInit {
  @Input() parentForm!: FormGroup;
  @Input() detailIndex!: number;
  @Output() itemsChanged = new EventEmitter<void>();

  materialDescriptionOptions = Object.values(MaterialDisplayOption);
  materials: any[] = []; // Replace with your actual material data

  constructor(private fb: FormBuilder) { }

  ngOnInit() {
    // Initialize your component, fetch materials data if needed
  }

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

  // Add these methods for typeahead functionality
  searchMaterials = (text$: Observable<string>) =>
    text$.pipe(
      debounceTime(200),
      distinctUntilChanged(),
      map(term => term.length < 2 ? []
        : this.materials.filter(v => v.name.toLowerCase().indexOf(term.toLowerCase()) > -1).slice(0, 10))
    )

  formatMaterialResult = (result: any) => result.name;

  onMaterialSelected(event: any, index: number) {
    // Handle material selection
    console.log('Material selected:', event, 'at index:', index);
    // Update the form control with the selected material
    const item = this.items.at(index);
    if (item instanceof FormGroup) {
      item.patchValue({
        MaterialNumber: event.item.id,
        FullMaterialDescription: event.item.name,
        // Update other fields as necessary
      });
      this.calculateOrderValue(index);
    }
  }
}
