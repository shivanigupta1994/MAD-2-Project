<template>
  <div class="image-container" :style="{ backgroundImage: 'url(' + backgroundImage + ')' }">
    <div class="form-container">
      <div class="card" :class="{ 'login-form': isLoginForm, 'register-form': !isLoginForm }" ref="card">
        <div class="card-header text-white bold-header" @mouseover="onHeaderHover(true)" @mouseout="onHeaderHover(false)">
          {{ isLoginForm ? 'Login' : 'Register' }}
        </div>
        <div class="card-body" @mouseover="onFormHover(true)" @mouseout="onFormHover(false)">
          <div class="mb-3 form-check form-switch">
            <input
              class="form-check-input"
              type="checkbox"
              id="toggleForm"
              v-model="isLoginForm"
              @change="changeBackgroundImage"
            />
            <label class="form-check-label common-text" for="toggleForm" :style="{ color: toggleButtonTextColor, fontWeight: 'bold' }">
              {{ isLoginForm ? 'Switch to Register' : 'Switch to Login' }}
            </label>
          </div>
          <form @submit.prevent="isLoginForm ? login : register" :style="{ border: 'none' }">
            <div class="mb-3">
              <label for="email" class="form-label text-white">Email address</label>
              <input v-model="email" type="email" class="form-control" id="email" required>
            </div>
            <div v-if="!isLoginForm" class="mb-3">
              <label for="username" class="form-label text-white">Username</label>
              <input v-model="username" type="text" class="form-control" id="username" required>
            </div>
            <div class="mb-3">
              <label for="password" class="form-label text-white">Password</label>
              <input v-model="password" type="password" class="form-control" id="password" required>
            </div>
            <!-- <button type="submit" class="btn btn-success submit-btn" @mouseover="onFormHover(true)" @mouseout="onFormHover(false)" :style="{ backgroundColor: toggleButtonColor, borderColor: toggleButtonColor }">
              {{ isLoginForm ? 'Login' : 'Register' }}
            </button> -->
            <button type="submit" class="btn btn-success submit-btn" @click="login" v-if="isLoginForm" @mouseover="onFormHover(true)" @mouseout="onFormHover(false)" :style="{ backgroundColor: toggleButtonColor, borderColor: toggleButtonColor }">
              Login
            </button>
            <button type="submit" class="btn btn-success submit-btn" @click="register" v-else @mouseover="onFormHover(true)" @mouseout="onFormHover(false)" :style="{ backgroundColor: toggleButtonColor, borderColor: toggleButtonColor }">
              Register
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isLoginForm: true,
      email: '',
      username: '',
      password: '',
      backgroundImage: '',
      formBorderStyle: '2px solid transparent',
    };
  },
  mounted() {
    this.changeBackgroundImage();
  },
  methods: {
    async login() {
      try {
        const response = await this.$axios.post('http://127.0.0.1:5000/login', {
          email: this.email,
          password: this.password
        });
        console.log('Login successful:', response.data);

        // Save user information to local storage
        this.saveUserInfo(response.data);

        // Redirect to the dashboard or another page
        this.redirectBasedOnRole(response.data.role);
      } catch (error) {
        alert(error.response.data.message)
        console.error('Login failed:', error);
      }
    },
    async register() {
      try {
        const response = await this.$axios.post('http://127.0.0.1:5000/register', {
          email: this.email,
          username: this.username,
          password: this.password
        });
        alert(response.data.message)
        // Handle registration success, e.g., show a success message

        // Automatically switch to the login form after successful registration
        this.isLoginForm = true;
      } catch (error) {
        console.error('Registration failed:', error);
        alert(error.response.data.message)
      }
    },
    saveUserInfo(data) {
      // Save user information to local storage
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('email', data.email);
      localStorage.setItem('username', data.username);
      localStorage.setItem('role', data.role);
      localStorage.setItem('user_id', data.user_id);
    },
    redirectBasedOnRole(role) {
      // Redirect based on user role
      if (role === 'librarian') {
        this.$router.push('/librarian');
      } else if (role === 'user') {
        this.$router.push('/user');
      }
    }, 
    async changeBackgroundImage() {
      try {
        const response = await fetch('https://source.unsplash.com/1600x900/?library');
        this.backgroundImage = response.url;

        this.updateFormColor();
      } catch (error) {
        console.error('Error fetching background image:', error);
      }
    },
    async updateFormColor() {
      const img = new Image();
      img.crossOrigin = 'Anonymous';

      img.onload = () => {
        const canvas = document.createElement('canvas');
        canvas.width = img.width;
        canvas.height = img.height;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, img.width, img.height);

        const data = ctx.getImageData(0, 0, img.width, img.height).data;
        const color = this.getDominantColor(data);

        // Update the background color dynamically based on the form type
        if (!this.isLoginForm) {
          this.$refs.card.style.backgroundColor = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
        }
      };

      img.src = this.backgroundImage;
    },
    getDominantColor(data) {
      let r = 0;
      let g = 0;
      let b = 0;

      for (let i = 0; i < data.length; i += 4) {
        r += data[i];
        g += data[i + 1];
        b += data[i + 2];
      }

      const totalPixels = data.length / 4;
      r = Math.round(r / totalPixels);
      g = Math.round(g / totalPixels);
      b = Math.round(b / totalPixels);

      return [r, g, b];
    },
    onFormHover(isHovered) {
      this.formBorderStyle = isHovered ? '2px solid #ffffff' : '2px solid transparent';
    },
    onHeaderHover(isHovered) {
      // Add any specific header hover behavior if needed
    },
  },
  computed: {
    toggleButtonColor() {
      return this.isLoginForm ? '#db6334' : '#e73ca0';
    },
    toggleButtonTextColor() {
      return this.isLoginForm ? '#db6334' : '#e73ca0';
    },
  },
};
</script>

<style scoped>
body {
  margin: 0;
  padding: 0;
}

.image-container {
  height: 100vh;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.form-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.card {
  width: 400px;
  transition: background-color 0.5s ease-in-out;
}

.login-form {
  background-color: #deb461;
}

.register-form {
  background-color: #72ade9; /* Default color, can be overridden dynamically */
}

.card-body {
  padding: 20px;
  transition: color 0.5s ease-in-out;
}

.form-check-label {
  transition: color 0.5s ease-in-out;
  color: #2980b9; /* Change the color of the "Switch to Register" or "Switch to Login" text */
}

.form-control {
  transition: background-color 0.5s ease-in-out, border-color 0.5s ease-in-out;
}

.submit-btn {
  width: 30%;
  margin-top: 10px;
  margin-left: 37.5%;
  transition: background-color 0.5s ease-in-out, border-color 0.5s ease-in-out;
}

.common-text {
  /* Common style for both Login and Register text */
  color: #2980b9; /* Change the color */
  font-style: italic; /* Add some italic style */
}
</style>
