import { Component, OnInit } from '@angular/core';
import { QuotationService } from '../../../services/quotation.service';

@Component({
  selector: 'app-quotes-all',
  templateUrl: './quotes-all.component.html',
  styleUrls: ['./quotes-all.component.css']
})
export class QuotesAllComponent implements OnInit {
  quotations: any[] = [];
  loading: boolean = false;
  error: string = '';

  constructor(private quotationService: QuotationService) { }

  ngOnInit(): void {
    this.loadQuotations();
  }

  loadQuotations(): void {
    this.loading = true;
    this.error = '';
    this.quotationService.getQuotations().subscribe(
      (data: any[]) => {
        this.quotations = data;
        this.loading = false;
      },
      error => {
        console.error('Error fetching quotations', error);
        this.error = 'Failed to load quotations. Please try again.';
        this.loading = false;
      }
    );
  }

  deleteQuotation(id: string): void {
    if (confirm('Are you sure you want to delete this quotation?')) {
      this.quotationService.deleteQuotation(id).subscribe(
        () => {
          this.quotations = this.quotations.filter(q => q.QuoteId !== id);
        },
        error => {
          console.error('Error deleting quotation', error);
          this.error = 'Failed to delete quotation. Please try again.';
        }
      );
    }
  }
}
