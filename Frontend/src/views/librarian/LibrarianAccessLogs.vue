<template>
  <div class="container mt-3">
    <!-- Display Access Logs and Filter -->
    <div class="card mt-4">
      <div class="card-header">Access Logs</div>
      <div class="card-body">
        <!-- Filter by Action -->
        <div class="mb-2">
          <label for="actionFilter" class="form-label">Filter by Action:</label>
          <select v-model="actionFilter" class="form-select" id="actionFilter">
            <option value="">All</option>
            <option value="Issued">Issued</option>
            <option value="Returned">Returned</option>
            <option value="Revoked">Revoked</option>
          </select>
        </div>

        <!-- Display Access Logs Table -->
        <table class="table table-bordered">
          <thead class="bg-secondary text-white">
            <tr>
              <th>ID</th>
              <th>User ID</th>
              <th>Book ID</th>
              <th>Status</th>
              <th>Issue Date</th>
              <th>Due Date</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="log in filteredLogs" :key="log.id">
              <td>{{ log.id }}</td>
              <td>{{ log.user_id }}</td>
              <td>{{ log.book_id }}</td>
              <td>{{ log.status }}</td>
              <td>{{ log.issue_date }}</td>
              <td v-if="log.due_date">{{ log.due_date }}</td>
              <td v-else>N/A</td>
              <td>
                <!-- <button v-if="log.status === 'Issued'" class="btn btn-danger btn-sm" @click="revokeAccesss(log.id)">Revoke</button>
                <button v-else class="btn btn-danger btn-sm" disabled>Revoke</button> -->
                <template v-if="log.status === 'Issued'">
                  <button class="btn btn-danger btn-sm" @click="revokeAccesss(log.id)">Revoke</button>
                </template>

                <template v-else-if="log.status === 'Returned'">
                  <span class="returned-date">Returned on {{ log.return_date }}</span>
                </template>

                <template v-else-if="log.status === 'Revoked'">
                  <span class="revoked-date">Revoked on {{ log.revoke_date }}</span>
                </template>

                <template v-else>
                  N/A
                </template>
              </td>
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
      logs: [],
      actionFilter: ''
    }
  },
  mounted() {
    this.getAllAccessLogs()
  },
  computed: {
    filteredLogs() {
      // Filter logs based on selected action
      return this.actionFilter
        ? this.logs.filter((log) => log.status === this.actionFilter)
        : this.logs
    }
  },
  methods: {
    async getAllAccessLogs() {
      try {
        const response = await this.$axios.get('/book/access')
        this.logs = response.data
      } catch (error) {
        console.error('Get Access Logs failed:', error)
      }
    },
    async revokeAccesss(id) {
      try {
        await this.$axios.put(`/book/access`, { id: id, revoke: 'True' })
        this.getAllAccessLogs()
      } catch (error) {
        console.error('Revoke Access failed:', error)
      }
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
}

.card {
  margin-top: 20px;
  border: 3px solid #ad9191;
  border-radius: 5px;
  overflow: hidden;
}

.card-header {
  background-color: #75aeba;
  font-weight: bold;
  color: rgb(21, 8, 84);
  text-align: center;
  width: 100%;
}

.form-label {
  font-weight: bold;
  color: rgb(183, 45, 162);
}

.form-select {
  width: 200px;
}

.table thead th {
  vertical-align: bottom;
  border-bottom: 2px solid #7b2bbc;
  border-top: 2px solid #7b2bbc;
  border-left: 2px solid #7b2bbc;
  border-right: 2px solid #7b2bbc;
  border-style: double;
}

.table td {
  /* background-color: #b3cdd5; */
  color: rgb(27, 8, 84);
  text-align: center;
  margin: auto;
  padding: auto;
}

.table th {
  background-color: #ea9d77;
  color: rgb(115, 73, 187);
  text-align: center;
  padding: auto;
}

.table-bordered td {
  border: 2px solid #ba96ab;
  border-style: dashed;
}

.table tbody {
  border-bottom: 2px solid #7b2bbc;
  border-top: 2px solid #7b2bbc;
  border-left: 2px solid #7b2bbc;
  border-right: 2px solid #7b2bbc;
}

.btn-danger {
  background-color: #b57d7f;
  border-color: #5500ff;
  color: #6f1318;
  font-weight: bold;
  text-align: center;
  display: inline-block;
  width: 100%;
  box-sizing: border-box;
  margin-left: auto;
}

.returned-date {
  color: #4CAF50;
  /* Green */
  font-weight: bold;
}

.revoked-date {
  color: #ff00f2;
  /* Red */
  font-weight: bold;
}
</style>
