import { Component, OnInit } from '@angular/core';
import { DashboardService } from '../../services/dashboard.service';
import { ChartData, ChartOptions } from 'chart.js';

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

  currentYear: number = new Date().getFullYear();

  // Initialize with default values
  lineChartData: ChartData<'line'> = {
    labels: [],
    datasets: []
  };
  lineChartOptions: ChartOptions = {};

  pieChartData: ChartData<'pie'> = {
    labels: [],
    datasets: []
  };
  pieChartOptions: ChartOptions = {};

  constructor(private dashboardService: DashboardService) { }

  ngOnInit(): void {
    this.loadDashboardData();
    this.initializeCharts();
  }

  loadDashboardData(): void {
    this.loading = true;
    this.error = null;
    this.dashboardService.getDashboardData().subscribe(
      (data: any) => {
        this.dashboardData = data.summary;
        this.recentQuotes = data.recentQuotes;
        this.loading = false;
        this.updateChartData();
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

  initializeCharts(): void {
    this.lineChartData = {
      labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
      datasets: [
        {
          label: 'Monthly Quotes',
          data: [0, 0, 0, 0, 0, 0, 0],
          fill: false,
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1
        }
      ]
    };

    this.lineChartOptions = {
      responsive: true,
      maintainAspectRatio: false
    };

    this.pieChartData = {
      labels: ['Accepted', 'Pending', 'Rejected'],
      datasets: [{
        data: [0, 0, 0],
        backgroundColor: ['#36A2EB', '#FFCE56', '#FF6384']
      }]
    };

    this.pieChartOptions = {
      responsive: true,
      maintainAspectRatio: false
    };
  }

  updateChartData(): void {
    // Update line chart data (example - replace with actual data)
    this.lineChartData.datasets[0].data = [
      this.dashboardData.totalQuotes,
      this.dashboardData.acceptedQuotes,
      this.dashboardData.pendingQuotes,
      this.dashboardData.totalValue,
      0, 0, 0
    ];

    // Update pie chart data
    this.pieChartData.datasets[0].data = [
      this.dashboardData.acceptedQuotes,
      this.dashboardData.pendingQuotes,
      this.dashboardData.totalQuotes - this.dashboardData.acceptedQuotes - this.dashboardData.pendingQuotes
    ];
  }
}
