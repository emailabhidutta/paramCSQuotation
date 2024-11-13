import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { QuotationService, Quotation } from '../../../services/quotation.service';

@Component({
  selector: 'app-quotation-detail',
  templateUrl: './quotation-detail.component.html',
  styleUrls: ['./quotation-detail.component.css']
})
export class QuotationDetailComponent implements OnInit {
  quotation: Quotation | null = null;
  loading = true;
  error = '';

  constructor(
    private route: ActivatedRoute,
    private quotationService: QuotationService
  ) { }

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.loadQuotation(id);
    } else {
      this.error = 'Invalid quotation ID';
      this.loading = false;
    }
  }

  loadQuotation(id: string): void {
    this.quotationService.getQuotationById(id).subscribe(
      (data) => {
        this.quotation = data;
        this.loading = false;
      },
      (error) => {
        this.error = 'Failed to load quotation details';
        this.loading = false;
        console.error('Error loading quotation:', error);
      }
    );
  }
}
