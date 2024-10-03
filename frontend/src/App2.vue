<script setup>

  import { ref, onMounted } from 'vue';
  // using the composition api you can just do your stuff directly here using ref
  const name = ref('John Doe');
  const status = ref('active');
  const tasks = ref(['task1', 'task2', 'task3'])
  const newTask = ref('')
  const toggleStatus = () => {
    // if (status.value == 'active')
    // status.value = 'inactive'
    // else status.value = 'active'
    status.value == 'active' ? 'inactive' : 'active'
  }

  const addTask = () =>{
    if (newTask.value.trim() !== ''){
      tasks.value.push(newTask.value);
      newTask.value = '';
    }
  }

  const deleteTask = (index) => {
    tasks.value.splice(index, 1);
  }

  onMounted(async () => {
    try{
      const response = await fetch('https://jsonplaceholder.typicode.com/todos');
      const data = await response.json()
      tasks.value = data.map( (task) => task.title);
    }
    catch (error){
      console.log('ERROR fetching tasks')
    }
    
  })
</script>
<template>
  <h1> Prep Tools</h1>
  <h1> {{ name }}</h1>
  <p v-if="status"> User is active</p>

  <form @submit.prevent="addTask">
    <label for="newTask"> Add Task</label>
    <input type="text" id="newTask" name="newTask" v-model="newTask"/>
    <button type="submit"></button>
  </form> 
  <h3>Tasks: </h3>
  <ul>
    <li v-for="task in tasks"  :key="task"> 
      <span>
        <button @click="deleteTask(index)">x</button>
        {{task}}
      </span>
    </li>
  </ul>
  <button @click="toggleStatus"> Change Status</button>
</template>

