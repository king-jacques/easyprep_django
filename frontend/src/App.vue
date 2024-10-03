<script setup>
  import Navbar from './components/Navbar.vue';
  import { RouterView } from 'vue-router';
  import { ref } from 'vue';
  // using the composition api you can just do your stuff directly here using ref
  const name = ref('John Doe');
  const status = ref('active');
  const tasks = ref(['task1', 'task2', 'task3'])
  const toggleStatus = () => {
    status.value = 'inactive'
  }

</script>
<template>
  <Navbar/>
  <RouterView/>
</template>

