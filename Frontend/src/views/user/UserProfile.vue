<template>
    <div>
      <div class="profile-container">
        <h2><i class="fas fa-user-circle"></i>User Profile</h2>
        <form @submit.prevent="updateProfile" class="mt-4">
          <div class="form-group">
            <label for="username">Username</label>
            <div class="input-group">
              <div class="input-group-prepend">
                <span class="input-group-text"><i class="fas fa-user"></i></span>
              </div>
              <input type="text" v-model="username" class="form-control" id="username" required>
            </div>
          </div>
          <div class="form-group">
            <label for="email">Email</label>
            <div class="input-group">
              <div class="input-group-prepend">
                <span class="input-group-text"><i class="fas fa-envelope"></i></span>
              </div>
              <input type="email" v-model="email" class="form-control" id="email" required>
            </div>
          </div>
          <button type="submit" class="btn btn-primary"><i class="fas fa-save"></i> Update Profile</button>
        </form>
  
        <button @click="deleteProfile" class="btn btn-danger mt-3"><i class="fas fa-trash"></i> Delete Profile</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username: "",
        email: "",
        userId: localStorage.getItem('user_id')
      };
    },
    mounted() {
      // Fetch user data when the component is mounted
      this.fetchUserProfile();
    },
    methods: {
      fetchUserProfile() {
        this.$axios.get(`/profile/${this.userId}`)
            .then(response => {
                const userData = response.data;
                this.username = userData.username;
                this.email = userData.email;
            })
            .catch(error => {
                console.error("Error fetching user profile:", error);
            });
      },
      updateProfile() {
        const data = {
          id: this.userId,
          username: this.username,
          email: this.email,
        };
  
        this.$axios.put(`/profile/${this.userId}`, data)
          .then(response => {
            alert(response.data.message);
          })
          .catch(error => {
            console.error("Error updating user profile:", error);
          });
      },
      deleteProfile() {
        // Send a DELETE request to delete the user profile
        const data = {
          id: this.userId,
        };
  
        if (window.confirm("Are you sure you want to delete your profile?")) {
          this.$axios.delete(`/profile/${this.userId}`, { data })
            .then(response => {
              console.log(response.data.message);

              // Optionally, redirect the user to a login page or another route
              alert(response.data.message);
              this.$router.push('/login');
              localStorage.clear();

            })
            .catch(error => {
              console.error("Error deleting user profile:", error);
            });
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .profile-container {
  max-width: 400px;
  margin: auto;
  margin-top: 5%;
  padding: 20px;
  border: 5px ridge #58aac8;
  border-radius: 20px;
  box-shadow: 0 0 10px rgba(197, 64, 155, 0.1);
  text-align: justify;
  }

  h2 {
    color: #b17071;
    text-align: center;
    font-weight: bold;
    text-decoration: underline;  
  }

  .form-group {
    margin-bottom: 1.5rem;
  }

  label {
    font-weight: bold;
    color: #bf217d;
  }

  .form-control {
    width: 100%;
    padding: 8px;
    margin-top: 5px;
    box-sizing: border-box;
    border: 1px solid #0fa9b7;
    border-radius: 8px;
  }

  .btn {
    cursor: pointer;
    display: inline-block;
    padding: 10px 20px;
    font-size: 16px;
    text-align: center;
    text-decoration:solid;
    outline: none;
    color: #311fa7;
    background-color: #71c2ab;
    border: 2px solid #007bff;
    font-weight: bold;
    border-radius: 5px;
    transition: background-color 0.3s;

  }

  .btn-danger {
    background-color: #c66aa3;
    border: 1px solid #dc3545;
    transition: background-color 0.3s;
  }

  .btn:hover {
    background-color: #96af68;
  }

  .btn i {
    margin-right: 2px;
  }
  </style>
  