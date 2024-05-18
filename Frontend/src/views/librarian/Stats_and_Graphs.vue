<template>
  <div id="wrapper">
    <div class="d-flex flex-column" id="content-wrapper">
      <div id="content">
        <div class="container-fluid">
          <div class="d-sm-flex justify-content-between align-items-center mb-4"></div>
          <div class="row">
            <div class="col-md-6 col-xl-3 mb-4">
              <div class="card shadow border-start-primary py-2">
                <div class="card-body">
                  <div class="row align-items-center no-gutters">
                    <div class="col me-2">
                      <div class="text-uppercase text-primary fw-bold text-xs mb-1">
                        <span class="fs-5">Total Issued Books</span>
                      </div>
                      <div class="text-dark fw-bold h5 mb-0">
                        <span> {{ res.total_issued_books }}</span>
                      </div>
                    </div>
                    <div class="col-auto">
                      <i class="fas fa-calendar fa-2x text-gray-300"></i>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-md-6 col-xl-3 mb-4">
              <div class="card shadow border-start-success py-2">
                <div class="card-body">
                  <div class="row align-items-center no-gutters">
                    <div class="col me-2">
                      <div class="text-uppercase text-success fw-bold text-xs mb-1">
                        <span class="fs-5">Total Sections: </span>
                      </div>
                      <div class="text-dark fw-bold h5 mb-0">
                        <span>{{ res.total_sections }}</span>
                      </div>
                    </div>
                    <div class="col-auto">
                      <i class="fas fa-dollar-sign fa-2x text-gray-300"></i>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-md-6 col-xl-3 mb-4">
              <div class="card shadow border-start-info py-2">
                <div class="card-body">
                  <div class="row align-items-center no-gutters">
                    <div class="col me-2">
                      <div class="text-uppercase text-info fw-bold text-xs mb-1">
                        <span class="fs-5">Books</span>
                      </div>
                      <div class="row g-0 align-items-center">
                        <div class="col-auto">
                          <div class="text-dark fw-bold h5 mb-0 me-3">
                            <span>{{ res.total_books }} </span>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="col-auto">
                      <i class="fas fa-clipboard-list fa-2x text-gray-300"></i>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-md-6 col-xl-3 mb-4">
              <div class="card shadow border-start-warning py-2">
                <div class="card-body">
                  <div class="row align-items-center no-gutters">
                    <div class="col me-2">
                      <div class="text-uppercase text-warning fw-bold text-xs mb-1">
                        <span class="fs-5">User's Count</span>
                      </div>
                      <div class="text-dark fw-bold h5 mb-0">
                        <span>{{ res.total_users }}</span>
                      </div>
                    </div>
                    <div class="col-auto">
                      <i class="fas fa-comments fa-2x text-gray-300"></i>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-lg-7 col-xl-4">
              <div class="card shadow mb-4">
                <div class="card-header d-flex justify-content-between align-items-center">
                  <h6 class="text-primary fw-bold m-1">Top 5 most issued books</h6>
                </div>
                <div class="card-body m-2">
                  <div class="chart-area" style="width: 100%; height: 100%">
                    <canvas id="barchart"></canvas>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-lg-5 col-xl-8">
              <div class="card shadow mb-4">
                <div class="card-header d-flex justify-content-between align-items-center">
                  <h6 class="text-primary fw-bold m-1">Number of books in each section</h6>
                </div>
                <div class="card-body">
                  <div class="chart-area" style="width: 100%; height: 100%">
                    <canvas id="polar-chart"></canvas>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Chart from 'chart.js/auto';

export default {
  data() {
    return {
      materials: [],
      res: {} // Initialize an empty object to store the dictionary
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get('http://localhost:5000/summary')
        console.log('Response:', response.data);
        this.materials = Object.entries(response.data).map(([name, value]) => ({ name, value }))

        // Convert materials to a dictionary
        this.res = this.materials.reduce((obj, material) => {
          obj[material.name] = material.value
          return obj
        }, {})
        this.renderPieChart()
        this.renderBarChart()
      } catch (error) {
        console.error(error)
      }
    },

    renderBarChart() {
      const ctx = document.getElementById('polar-chart').getContext('2d');
      const sections = this.res.section_wise_book_count;

      const colors = [
        'rgba(255, 99, 132, 0.2)',   // Red
        'rgba(54, 162, 235, 0.2)',    // Blue
        'rgba(255, 206, 86, 0.2)',    // Yellow
        'rgba(75, 192, 192, 0.2)',    // Green
        'rgba(153, 102, 255, 0.2)',   // Purple
        'rgba(255, 159, 64, 0.2)',    // Orange
        'rgba(255, 0, 0, 0.2)',       // Bright Red
        'rgba(0, 255, 0, 0.2)',       // Bright Green
        'rgba(0, 0, 255, 0.2)',       // Bright Blue
        'rgba(255, 255, 0, 0.2)',     // Yellow
        'rgba(255, 0, 255, 0.2)',     // Magenta
        'rgba(0, 255, 255, 0.2)',     // Cyan
        'rgba(128, 0, 128, 0.2)',     // Purple
        'rgba(255, 140, 0, 0.2)',     // Dark Orange
        'rgba(0, 128, 128, 0.2)'      // Teal
      ];


      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: Object.keys(sections),
          datasets: [{
            data: Object.values(sections),
            borderWidth: 1,
            backgroundColor: colors,
            borderColor: colors,
            label: 'Books Count in each section'
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true,
              precision: 0,
              ticks: {
                stepSize: 0.25
              }
            }
          }
        }
      });

    },
    renderPieChart() {
      const ctx = document.getElementById('barchart').getContext('2d');
      const books = this.res.top_books;

      new Chart(ctx, {
        type: 'pie',
        data: {
          labels: books.map(book => book.book_name),
          datasets: [{
            label: 'Issued',
            data: books.map(book => book.average_rating),
            borderWidth: 5
          }]
        }
      });

    }
  }
}
</script>
