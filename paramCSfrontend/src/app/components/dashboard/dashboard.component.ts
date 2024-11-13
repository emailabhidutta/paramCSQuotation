import { Component, OnInit } from '@angular/core';
import { DashboardService } from '../../services/dashboard.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  dashboardData: any = {
    totalQuotes: 0,
    acceptedQuotes: 0,
    pendingQuotes: 0,
    totalValue: 0
  };
  recentQuotes: any[] = [];
  loading: boolean = true;
  error: string | null = null;

  constructor(private dashboardService: DashboardService) { }

  ngOnInit(): void {
    this.loadDashboardData();
  }

  loadDashboardData(): void {
    this.loading = true;
    this.error = null;
    this.dashboardService.getDashboardData().subscribe(
      (data: any) => {
        this.dashboardData = data.summary;
        this.recentQuotes = data.recentQuotes;
        this.loading = false;
      },
      error => {
        console.error('Error fetching dashboard data', error);
        this.error = 'Failed to load dashboard data. Please try again later.';
        this.loading = false;
      }
    );
  }

  getStatusColor(status: string): string {
    switch (status.toLowerCase()) {
      case 'accepted':
        return 'text-success';
      case 'pending':
        return 'text-warning';
      case 'rejected':
        return 'text-danger';
      default:
        return 'text-secondary';
    }
  }

  formatCurrency(value: number): string {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value);
  }
}
