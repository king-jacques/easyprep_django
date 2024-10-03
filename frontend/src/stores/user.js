// stores/user.js
import { defineStore } from 'pinia';
import axios from 'axios';

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null, // Stores user info
    token: null, // Stores JWT token
  }),
  persist: true,
  actions: {
    async login(user, token) {
      try {
        // // Send login request to the backend
        // const response = await axios.post('http://localhost:8000/auth/login', credentials);

        // // Extract the JWT token and user data from the response
        // const token = response.data.token;
        // const user = response.data.user;

        // Save token and user info in the store
        this.token = token;
        this.user = user;

        // Store the JWT token in localStorage for persistence
        // localStorage.setItem('token', token);

        // Set the default Authorization header for all Axios requests
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      } catch (error) {
        throw new Error('Login failed');
      }
    },

    logout() {
      // Clear the token and user info from the store
      this.token = null;
      this.user = null;

      // Remove the token from localStorage
      localStorage.removeItem('token');

      // Remove the Authorization header
      delete axios.defaults.headers.common['Authorization'];
    },

    // // Restore user info from the JWT token stored in localStorage
    // initializeStore() {
    //   const token = localStorage.getItem('token');
    //   if (token) {
    //     this.token = token;
    //     axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    //     // Optionally, you can also load user data using the token if your backend supports it
    //   }
    // }
  },
  
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
});
