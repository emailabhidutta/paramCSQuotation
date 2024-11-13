import { Component, OnInit, OnDestroy, ViewChild } from '@angular/core';
import { DashboardService } from '../../services/dashboard.service';
import { ChartConfiguration, ChartData } from 'chart.js';
import { BaseChartDirective } from 'ng2-charts';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

interface DashboardSummary {
  totalQuotes: number;
  acceptedQuotes: number;
  pendingQuotes: number;
  totalValue: number;
}

interface Quote {
  id: string;
  customerName: string;
  amount: number;
  status: string;
  date: string;
}

interface Customer {
  id: string;
  name: string;
  totalQuotes: number;
  totalValue: number;
}

interface MonthlyQuoteData {
  month: string;
  count: number;
}

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit, OnDestroy {
  @ViewChild(BaseChartDirective) chart?: BaseChartDirective;

  dashboardData: DashboardSummary = {
    totalQuotes: 0,
    acceptedQuotes: 0,
    pendingQuotes: 0,
    totalValue: 0
  };
  recentQuotes: Quote[] = [];
  topCustomers: Customer[] = [];
  currentYear: number = new Date().getFullYear();
  loading: boolean = true;
  error: string | null = null;

  private unsubscribe$ = new Subject<void>();

  // Pagination
  currentPage: number = 1;
  pageSize: number = 10;
  totalQuotes: number = 0;

  // Date range filter
  startDate: string = '';
  endDate: string = '';

  // Line chart configuration
  lineChartData: ChartConfiguration['data'] = {
    datasets: [
      {
        data: [],
        label: 'Quotes',
        backgroundColor: 'rgba(0, 123, 255, 0.2)',
        borderColor: 'rgba(0, 123, 255, 1)',
        pointBackgroundColor: 'rgba(0, 123, 255, 1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(0, 123, 255, 0.8)',
        fill: 'origin',
      }
    ],
    labels: []
  };

  lineChartOptions: ChartConfiguration['options'] = {
    responsive: true,
    elements: {
      line: {
        tension: 0.5
      }
    },
    scales: {
      x: {},
      y: {
        position: 'left',
        beginAtZero: true
      }
    },
    plugins: {
      legend: { display: true },
      tooltip: { mode: 'index', intersect: false }
    }
  };

  // Pie chart for quote status distribution
  pieChartData: ChartData<'pie', number[], string | string[]> = {
    labels: ['Accepted', 'Pending', 'Rejected'],
    datasets: [{
      data: []
    }]
  };

  pieChartOptions: ChartConfiguration['options'] = {
    responsive: true,
    plugins: {
      legend: {
        display: true,
        position: 'top',
      }
    }
  };

  constructor(private dashboardService: DashboardService) { }

  ngOnInit(): void {
    this.loadDashboardData();
  }

  ngOnDestroy(): void {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }

  loadDashboardData(): void {
    this.loading = true;
    this.error = null;
    this.dashboardService.getDashboardData(this.startDate, this.endDate, this.currentPage, this.pageSize)
      .pipe(takeUntil(this.unsubscribe$))
      .subscribe(
        (data: any) => {
          this.dashboardData = data.summary;
          this.recentQuotes = data.recentQuotes;
          this.topCustomers = data.topCustomers;
          this.updateChartData(data.monthlyQuotes);
          this.updatePieChartData();
          this.totalQuotes = data.totalQuotes;
          this.loading = false;
        },
        error => {
          console.error('Error fetching dashboard data', error);
          this.error = 'Failed to load dashboard data. Please try again later.';
          this.loading = false;
        }
      );
  }

  updateChartData(monthlyData: MonthlyQuoteData[]): void {
    this.lineChartData.datasets[0].data = monthlyData.map(item => item.count);
    this.lineChartData.labels = monthlyData.map(item => item.month);
    this.chart?.update();
  }

  updatePieChartData(): void {
    this.pieChartData.datasets[0].data = [
      this.dashboardData.acceptedQuotes,
      this.dashboardData.pendingQuotes,
      this.dashboardData.totalQuotes - (this.dashboardData.acceptedQuotes + this.dashboardData.pendingQuotes)
    ];
  }

  onPageChange(page: number): void {
    this.currentPage = page;
    this.loadDashboardData();
  }

  onDateRangeChange(): void {
    this.loadDashboardData();
  }

  refreshDashboard(): void {
    this.loadDashboardData();
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
