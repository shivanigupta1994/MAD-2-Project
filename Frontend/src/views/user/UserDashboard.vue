User

<template>
  <div>
    <!-- Top Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
      <div class="container">
        <!-- Logo and Name -->
        <router-link to="/user" class="navbar-brand" @click="toggleSidebar">
          <!-- Correct path to the image within the public folder -->
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
        <router-link to="/user/books" class="text-decoration-none text-muted">
          <h2>📖 Books</h2>
        </router-link>
      </div>
      <div class="sidebar-header">
        <router-link to="/user/profile" class="text-decoration-none text-muted">
          <h2>👤 Profile</h2>
        </router-link>
      </div>
      <div class="sidebar-header">
        <router-link to="/user/space" class="text-decoration-none text-muted">
          <h2>🚀 My Space</h2>
        </router-link>
      </div>

    </div>

    <!-- Main Content -->
    <div class="main-content " :style="{ marginLeft: sidebarVisible ? '250px' : '0' }">
      <router-view></router-view>
      <div class="text-muted" v-if="$route.path === '/user'">
        <h1 class="m-2">Welcome to the Library</h1>
        <hr>
        <p class="h2">You can search for books, view your profile, and manage your space from the sidebar.</p>
        <br>
        <!-- Search Box -->
        <div class="container mt-5 ">
          <div class="row">
            <div class="col-md-12">
              <form @submit.prevent="searchBooks" class="form-inline w-50">
                <div class="form-group">
                  <label for="searchCriteria"><b>Search by:</b></label>
                  <select v-model="searchCriteria" class="form-control" id="searchCriteria">
                    <option value="category">Category</option>
                    <option value="author">Author Name</option>
                    <option value="name">Book Name</option>
                  </select>
                </div>
                <br />
                <div v-if="searchCriteria === 'category'" class="form-group">
                  <label for="category"><b>Category:</b></label>
                  <select v-model="searchValue" class="form-control" id="category" :placeholder="'Select a category'"
                    required>
                    <option value="" disabled>Select a category</option>
                    <option v-for="category in categories" :key="category.id" :value="category.id">
                      {{ category.name }}
                    </option>
                  </select>
                </div>
                <div v-else class="form-group col-md-7">
                  <label :for="searchCriteria">{{ capitalize(searchCriteria) }}:</label>
                  <input :type="inputType" v-model="searchValue" class="form-control" :id="searchCriteria"
                    :placeholder="'Enter ' + capitalize(searchCriteria)" required />
                </div>
                <button type="submit" class="btn btn-primary mt-3">Search</button>
              </form>
            </div>
          </div>
        </div>
        <br><br><br><br>

        <h3 class="m-1 h1">📚 Policy:</h3>
        <p class="m-5 h2"> ⚝ You can borrow a maximum of 5 books at a time.</p>
        <p class="m-5 h2">⚝ You can keep the books for a maximum of 7 days.</p>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios'

export default {
  data() {
    return {
      sidebarVisible: false,
      searchCriteria: 'category',
      searchValue: '',
      categories: [], // New property to store categories
      role: localStorage['role']
    }
  },
  created() {
    this.fetchCategories()
  },
  methods: {
    async fetchCategories() {
      try {
        const response = await this.$axios.get('/section')
        this.categories = response.data
      } catch (error) {
        console.error('Error fetching categories:', error)
      }
    },
    searchBooks() {
      // Define the query parameter keys based on the selected search criteria
      const queryParamKeys = {
        category: 'category',
        author: 'author',
        name: 'name'
      }
      // alert(this.searchCriteria)

      const params = {
        [queryParamKeys[this.searchCriteria]]: this.searchValue
      }
      // Redirect to the same page with the updated query params
      this.$router.push({ name: 'UserBooks', query: params })
    },
    capitalize(str) {
      return str.charAt(0).toUpperCase() + str.slice(1)
    },
    toggleSidebar() {
      this.sidebarVisible = !this.sidebarVisible;
    },
    logout() {
      localStorage.clear();
      location.reload();
    },

  }
}
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