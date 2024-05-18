<template>
  <div class="container mt-3">
    <!-- Display Requests -->
    <div class="card mt-4">
      <div class="card-header">All Requests</div>
      <div class="card-body">
        <!-- Table for Pending Requests -->
        <table class="table table-bordered table-hover">
          <thead class="thead">
            <tr>
              <th>ID</th>
              <th>User</th>
              <th>Book</th>
              <th>Request Date</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in pendingRequests" :key="request.id">
              <td>{{ request.id }}</td>
              <td>{{ request.username }}</td>
              <td>{{ request.book_name }}</td>
              <td>{{ request.request_date }}</td>
              <td>{{ request.status }}</td>
              <td>
                <button @click="acceptRequest(request.id)" class="btn btn-warning btn-sm m-1">
                  Accept
                </button>
                <button @click="rejectRequest(request.id)" class="btn btn-danger btn-sm m-1">
                  Reject
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Display Approved/Rejected Requests (Request Logs) -->
    <div class="card mt-4">
      <div class="card-header">Request Logs</div>
      <div class="card-body">
        <!-- Table for Approved/Rejected Requests -->
        <table class="table table-bordered table-hover">
          <thead class="thead">
            <tr>
              <th>ID</th>
              <th>User</th>
              <th>Book</th>
              <th>Request Date</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in approvedRejectedRequests" :key="request.id">
              <td>{{ request.id }}</td>
              <td>{{ request.username }}</td>
              <td>{{ request.book_name }}</td>
              <td>{{ request.request_date }}</td>
              <td>{{ request.status }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      requests: [],
    };
  },
  computed: {
    pendingRequests() {
      return this.requests.filter(request => request.status === 'Pending');
    },
    approvedRejectedRequests() {
      return this.requests.filter(request => request.status === 'Approved' || request.status === 'Rejected');
    },
  },
  mounted() {
    this.getAllRequests();
  },
  methods: {
    async getAllRequests() {
      try {
        const response = await this.$axios.get('/book/request');
        this.requests = response.data;
      } catch (error) {
        console.error('Get Requests failed:', error);
      }
    },
    async acceptRequest(requestId) {
      try {
        const response = await this.$axios.put(`/book/request`, { id: requestId, approved: 'True' });
        alert(response.data.message);
        this.getAllRequests();
      } catch (error) {
        console.error('Accept Request failed:', error);
      }
    },
    async rejectRequest(requestId) {
      try {
        const response = await this.$axios.put(`/book/request`, {
          id: requestId,
          approved: 'False',
        });
        alert(response.data.message);
        this.getAllRequests();
      } catch (error) {
        console.error('Reject Request failed:', error);
      }
    },
    async cancelRequest(requestId) {
      try {
        await this.$axios.delete(`/request/${requestId}`);
        this.getAllRequests();
      } catch (error) {
        console.error('Cancel Request failed:', error);
      }
    },
    formatRequestDate(dateString) {
      const options = { year: 'numeric', month: 'short', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('en-US', options);
    },
  },
};
</script>


<style>
.card-header{
  background-color: #8eeca7;
  font-weight: bold;
  color: rgb(148, 18, 102);
  text-align: center;
  width: 100%;
}

.table {
    width: 90%;
    margin-bottom: 1rem;
    color: #e0e085;
    border-collapse: collapse;
    margin: 0 auto;
  }
  
  .table thead th {
    vertical-align: bottom;
    border-bottom: 2px solid #25977c;
    border-top: 2px solid #25977c;
    border-left: 2px solid #25977c;
    border-right: 2px solid #25977c;
    border-style: double;
    background-color: #c6d466;
    color: rgb(11, 111, 19);
    text-align: center;
  }
  
  .table-bordered {
    border: 2px solid #25977c;
  }
  
  .table-bordered th,
  .table-bordered td {
    border: 2px solid #25977c;
    border-style: dashed;
  }

  .table th{
    text-align: center;
  }

  .table td{
    text-align: center;
  }

.btn {
  cursor: pointer;
  transition: opacity 0.3s ease-in-out;
  border-radius: 10px;
  padding: 6px 16px;
}

.btn:hover {
  opacity: 0.8;
}

</style>
