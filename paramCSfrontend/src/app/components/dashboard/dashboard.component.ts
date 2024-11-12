import { Component, OnInit, ViewChild } from '@angular/core';
import { DashboardService } from '../../services/dashboard.service';
import { ChartConfiguration } from 'chart.js';
import { BaseChartDirective } from 'ng2-charts';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  @ViewChild(BaseChartDirective) chart?: BaseChartDirective;

  dashboardData: any = {
    totalQuotes: 0,
    acceptedQuotes: 0,
    pendingQuotes: 0,
    totalValue: 0
  };
  recentQuotes: any[] = [];
  topCustomers: any[] = [];
  currentYear: number = new Date().getFullYear();
  loading: boolean = true;
  error: string | null = null;

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
        this.topCustomers = data.topCustomers;
        this.updateChartData(data.monthlyQuotes);
        this.loading = false;
      },
      error => {
        console.error('Error fetching dashboard data', error);
        this.error = 'Failed to load dashboard data. Please try again later.';
        this.loading = false;
      }
    );
  }

  updateChartData(monthlyData: any[]): void {
    this.lineChartData.datasets[0].data = monthlyData.map(item => item.count);
    this.lineChartData.labels = monthlyData.map(item => item.month);
    this.chart?.update();
  }

  getStatusColor(status: string): string {
    switch (status.toLowerCase()) {
      case 'accepted':
        return 'success';
      case 'pending':
        return 'warning';
      case 'rejected':
        return 'danger';
      default:
        return 'primary';
    }
  }

  formatCurrency(value: number): string {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value);
  }

  refreshDashboard(): void {
    this.loadDashboardData();
  }
}
