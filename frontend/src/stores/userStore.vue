<template>
  <div>
    <p v-if="isAuthenticated">Welcome, {{ user.username }}</p>
    <p v-else>Please log in</p>
    <button @click="login">Login</button>
    <button @click="logout">Logout</button>
  </div>
</template>

<script>
import { useUserStore } from './stores/user'; // Import the store

export default {
  setup() {
    const userStore = useUserStore(); // Use the store
    const login = () => {
      userStore.login({ username: 'john_doe' }); // Login action
    };
    const logout = () => {
      userStore.logout(); // Logout action
    };

    return {
      user: userStore.user,
      isAuthenticated: userStore.isAuthenticated,
      login,
      logout
    };
  }
};
</script>
