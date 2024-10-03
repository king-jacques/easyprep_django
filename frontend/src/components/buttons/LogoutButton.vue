<template>
    <div>
      <!-- Your other components -->
      <button class="hover:bg-gray-900 hover:text-white text-white rounded-md px-3 py-2"@click="handleLogout">Sign Out</button>
    </div>
  </template>
  
  <script setup>
  import { useUserStore } from '@/stores/user';
  import { RouterLink, useRouter } from 'vue-router';
  const router = useRouter()
  
  
    const userStore = useUserStore();
  
    const handleLogout = () => {
    userStore.logout();
    
    router.push('/');
    };
  
  </script>
  
  <!-- <style scoped>
    button {
    background-color: gray; /* Example color */
    color: white;
    border: none;
    padding: 10px 15px;
    cursor: pointer;
    border-radius: 5px;
    }

    button:hover {
    background-color: #d32f2f; /* Darker shade on hover */
    }
</style> -->
