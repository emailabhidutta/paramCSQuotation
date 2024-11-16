import { Component, OnInit } from '@angular/core';
import { QuotationService } from '../../../services/quotation.service';
import { Quotation, QuotationStatus } from '../../../models/quotation.model';

interface QuotationResponse {
  quotations: Quotation[];
  totalCount: number;
}

@Component({
  selector: 'app-quotation-list',
  templateUrl: './quotation-list.component.html',
  styleUrls: ['./quotation-list.component.css']
})
export class QuotationListComponent implements OnInit {
  quotations: Quotation[] = [];
  quotationStatuses: QuotationStatus[] = [];
  loading = false;
  error: string | null = null;

  // Pagination
  currentPage = 1;
  pageSize = 10;
  totalQuotations = 0;

  // Filtering
  selectedStatus: string | null = null;

  constructor(private quotationService: QuotationService) { }

  ngOnInit(): void {
    this.loadQuotationStatuses();
    this.loadQuotations();
  }

  loadQuotationStatuses(): void {
    this.quotationService.getQuotationStatuses().subscribe(
      statuses => this.quotationStatuses = statuses,
      error => {
        console.error('Error loading quotation statuses', error);
        this.error = 'Error loading quotation statuses. Please try again.';
      }
    );
  }

  loadQuotations(): void {
    this.loading = true;
    this.error = null;
    this.quotationService.getQuotations(this.currentPage, this.pageSize, this.selectedStatus || undefined).subscribe(
      (response: QuotationResponse) => {
        this.quotations = response.quotations;
        this.totalQuotations = response.totalCount;
        this.loading = false;
      },
      (error) => {
        this.error = 'Error loading quotations. Please try again.';
        this.loading = false;
        console.error('Error loading quotations', error);
      }
    );
  }

  onPageChange(page: number): void {
    this.currentPage = page;
    this.loadQuotations();
  }

  onStatusChange(): void {
    this.currentPage = 1; // Reset to first page when changing filter
    this.loadQuotations();
  }

  deleteQuotation(id: string): void {
    if (confirm('Are you sure you want to delete this quotation?')) {
      this.quotationService.deleteQuotation(id).subscribe(
        () => {
          this.quotations = this.quotations.filter(q => q.QuoteId !== id);
          this.loadQuotations(); // Reload to get accurate counts
        },
        (error) => {
          console.error('Error deleting quotation', error);
          this.error = 'Error deleting quotation. Please try again.';
        }
      );
    }
  }
}
