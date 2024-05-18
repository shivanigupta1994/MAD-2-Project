<template>
  <div>
    <!-- Top Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
      <div class="container">
        <!-- Logo and Name -->
        <router-link to="/librarian" class="navbar-brand" @click="toggleSidebar">
          <h1>🏛️ Library 🏛️ </h1>
        </router-link>



        <!-- Logout Button -->
        <button @click="logout" class="btn btn-danger ml-auto">Logout</button>

        <!-- Mobile Menu Button -->
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav"
          aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
      </div>
    </nav>

    <!-- Sidebar Menu -->
    <div v-if="sidebarVisible" class="sidebar">
      <div class="sidebar-header">
        <router-link to="/librarian/stats_and_graphs" class="text-decoration-none text-muted">
          <h2>📈 Dashboard</h2>
        </router-link>
      </div>
      <div class="sidebar-header">
        <router-link to="/librarian/sections" class="text-decoration-none text-muted">
          <h2>📚 Sections</h2>
        </router-link>
      </div>
      <div class="sidebar-header">
        <router-link to="/librarian/books" class="text-decoration-none text-muted">
          <h2>📒 Books</h2>
        </router-link>
      </div>

      <div class="sidebar-header">
        <router-link to="/librarian/requests" class="text-decoration-none text-muted">
          <h2>📩 Requests</h2>
        </router-link>
      </div>
      <div class="sidebar-header">
        <router-link to="/librarian/accesslogs" class="text-decoration-none text-muted">
          <h2>📝 Access Logs</h2>
        </router-link>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content" :style="{ marginLeft: sidebarVisible ? '250px' : '0' }">
      <router-view></router-view>
      <div v-if="$route.path === '/librarian'">
        <h1 class="m-2">Welcome to the Library</h1>
        <hr>
        <p class="h2">You can manage sections, books, access logs, requests, and view stats and graphs from the sidebar.
        </p>
        <br><br><br><br>

        <h3 class="m-1 h1">📚 Policy:</h3>
        <p class="m-5 h2"> ⚝ User can borrow a maximum of 5 books at a time.</p>
        <p class="m-5 h2">⚝ User can keep the books for a maximum of 7 days.</p>


      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      sidebarVisible: false,
    };
  },
  methods: {
    toggleSidebar() {
      this.sidebarVisible = !this.sidebarVisible;
    },
    logout() {
      localStorage.clear();
      location.reload();
    }
  }
};
</script>

<style scoped>
/* Add your custom styles here */
.img {
  max-width: 40px;
  margin-right: 10px;
}

.search-box {
  width: 300px;
}

.sidebar {
  width: 250px;
  background-color: #9eabb4;
  position: fixed;
  height: 100%;
  overflow-y: auto;
  padding-top: 30px;
  margin-top: 0;
  z-index: 1000;
}

.sidebar-visible {
  display: block;
}

.sidebar-header {
  text-align: left;
  padding-bottom: 20px;
  margin-left: 20px;
}

.main-content {
  transition: margin-left 0.3s;
  padding: 20px;
  margin-top: 60px;
}
</style>
