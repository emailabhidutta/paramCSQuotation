import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router, ParamMap } from '@angular/router';
import { QuotationService } from '../../../services/quotation.service';
import { Quotation, QuotationDetails, QuotationItemDetails, ApprovalStatus } from '../../../models/quotation.model';
import { catchError, finalize, switchMap, tap } from 'rxjs/operators';
import { forkJoin, of, Observable } from 'rxjs';

@Component({
  selector: 'app-quotation-detail',
  templateUrl: './quotation-detail.component.html',
  styleUrls: ['./quotation-detail.component.css']
})
export class QuotationDetailComponent implements OnInit {
  quotation: Quotation | null = null;
  quotationDetails: QuotationDetails[] = [];
  loading = false;
  error: string | null = null;
  rejectionReason = '';
  ApprovalStatus = ApprovalStatus; // Make enum available in template

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private quotationService: QuotationService
  ) { }

  ngOnInit(): void {
    this.route.paramMap.pipe(
      switchMap((params: ParamMap) => {
        const quoteId = params.get('id');
        if (quoteId) {
          this.loading = true;
          return this.loadQuotationData(quoteId);
        } else {
          this.error = 'No quotation ID provided';
          return of(null);
        }
      }),
      catchError(error => {
        console.error('Error in quotation detail initialization', error);
        this.error = 'An error occurred while loading the quotation. Please try again.';
        return of(null);
      }),
      finalize(() => this.loading = false)
    ).subscribe();
  }

  loadQuotationData(quoteId: string): Observable<any> {
    return forkJoin({
      quotation: this.quotationService.getQuotationById(quoteId),
      details: this.quotationService.getQuotationDetails(quoteId)
    }).pipe(
      tap(({ quotation, details }) => {
        this.quotation = quotation;
        this.quotationDetails = details;
      }),
      catchError(error => {
        console.error('Error loading quotation data', error);
        this.error = 'Error loading quotation data. Please try again.';
        return of(null);
      })
    );
  }

  approveQuotation(): void {
    if (!this.quotation) return;

    this.loading = true;
    this.error = null;
    this.quotationService.approveQuotation(this.quotation.QuoteId).pipe(
      catchError(error => {
        console.error('Error approving quotation', error);
        this.error = 'Error approving quotation. Please try again.';
        return of(null);
      }),
      finalize(() => this.loading = false)
    ).subscribe(updatedQuotation => {
      if (updatedQuotation) {
        this.quotation = updatedQuotation;
      }
    });
  }

  rejectQuotation(): void {
    if (!this.quotation) return;
    if (!this.rejectionReason.trim()) {
      this.error = 'Please provide a rejection reason.';
      return;
    }

    this.loading = true;
    this.error = null;
    this.quotationService.rejectQuotation(this.quotation.QuoteId, this.rejectionReason).pipe(
      catchError(error => {
        console.error('Error rejecting quotation', error);
        this.error = 'Error rejecting quotation. Please try again.';
        return of(null);
      }),
      finalize(() => this.loading = false)
    ).subscribe(updatedQuotation => {
      if (updatedQuotation) {
        this.quotation = updatedQuotation;
        this.rejectionReason = '';
      }
    });
  }

  reviseQuotation(): void {
    if (!this.quotation) return;

    this.loading = true;
    this.error = null;
    this.quotationService.reviseQuotation(this.quotation.QuoteId).pipe(
      catchError(error => {
        console.error('Error revising quotation', error);
        this.error = 'Error revising quotation. Please try again.';
        return of(null);
      }),
      finalize(() => this.loading = false)
    ).subscribe(updatedQuotation => {
      if (updatedQuotation) {
        this.quotation = updatedQuotation;
      }
    });
  }

  calculateTotalValue(): number {
    return this.quotationDetails.reduce((total, detail) =>
      total + detail.items.reduce((itemTotal, item) => itemTotal + item.OrderValue, 0)
      , 0);
  }

  calculateTotalDiscount(): number {
    return this.quotationDetails.reduce((total, detail) =>
      total + detail.items.reduce((itemTotal, item) => itemTotal + (item.DiscountValue || 0), 0)
      , 0);
  }

  calculateTotalSurcharge(): number {
    return this.quotationDetails.reduce((total, detail) =>
      total + detail.items.reduce((itemTotal, item) => itemTotal + (item.SurchargeValue || 0), 0)
      , 0);
  }

  canApprove(): boolean {
    return this.quotation?.QStatusID.QStatusName !== ApprovalStatus.Approved;
  }

  canReject(): boolean {
    return this.quotation?.QStatusID.QStatusName !== ApprovalStatus.Rejected;
  }

  canRevise(): boolean {
    return this.quotation?.QStatusID.QStatusName !== ApprovalStatus.Pending;
  }

  navigateToEdit(): void {
    if (this.quotation) {
      this.router.navigate(['/quotations', this.quotation.QuoteId, 'edit']);
    }
  }
}
