<template>
    <div class="min-h-screen bg-gray-100">
      <!-- Header -->
      <header class="bg-white shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 class="text-2xl font-semibold text-gray-900">Dashboard</h1>
          <div class="flex items-center">
            <button class="p-2 rounded-full bg-gray-200 text-gray-600 hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500">
              <bell-icon class="h-6 w-6" />
            </button>
            <div class="ml-3 relative">
              <div>
                <button class="flex items-center focus:outline-none">
                  <img class="h-8 w-8 rounded-full" src="" alt="User avatar" />
                  <span class="ml-2 text-sm font-medium text-gray-700">John Doe</span>
                  <chevron-down-icon class="ml-1 h-4 w-4 text-gray-400" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </header>
  
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <!-- Stats Card -->
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0 bg-purple-500 rounded-md p-3">
                  <users-icon class="h-6 w-6 text-white" />
                </div>
                <div class="ml-5 w-0 flex-1">
                  <dl>
                    <dt class="text-sm font-medium text-gray-500 truncate">Total Users</dt>
                    <dd class="text-3xl font-semibold text-gray-900">10,897</dd>
                  </dl>
                </div>
              </div>
            </div>
            <div class="bg-gray-50 px-5 py-3">
              <div class="text-sm">
                <a href="#" class="font-medium text-purple-600 hover:text-purple-500">View all</a>
              </div>
            </div>
          </div>
  
          <!-- Chart Card -->
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <h3 class="text-lg leading-6 font-medium text-gray-900">User Growth</h3>
              <div class="mt-2 flex items-center justify-between">
                <div class="flex items-center">
                  <span class="text-2xl font-semibold text-gray-900">+5.36%</span>
                  <trend-up-icon class="ml-2 h-5 w-5 text-green-500" />
                </div>
                <div class="text-sm text-gray-500">vs last month</div>
              </div>
              <div class="mt-4 h-24">
                <!-- Placeholder for chart -->
                <div class="w-full h-full bg-gray-200 rounded flex items-center justify-center text-gray-400">
                  Chart Placeholder
                </div>
              </div>
            </div>
          </div>
  
          <!-- Tasks Card -->
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <h3 class="text-lg leading-6 font-medium text-gray-900">Recent Tasks</h3>
              <ul class="mt-4 space-y-4">
                <li v-for="task in tasks" :key="task.id" class="flex items-center">
                  <input :id="task.id" :checked="task.completed" type="checkbox" class="h-4 w-4 text-purple-600 focus:ring-purple-500 border-gray-300 rounded" />
                  <label :for="task.id" class="ml-3 text-sm text-gray-700">{{ task.title }}</label>
                </li>
              </ul>
            </div>
            <div class="bg-gray-50 px-5 py-3">
              <div class="text-sm">
                <a href="#" class="font-medium text-purple-600 hover:text-purple-500">View all tasks</a>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Recent Activity -->
        <div class="mt-8">
          <h2 class="text-lg leading-6 font-medium text-gray-900">Recent Activity</h2>
          <div class="mt-4 bg-white shadow overflow-hidden sm:rounded-md">
            <ul role="list" class="divide-y divide-gray-200">
              <li v-for="activity in recentActivity" :key="activity.id">
                <a href="#" class="block hover:bg-gray-50">
                  <div class="px-4 py-4 sm:px-6">
                    <div class="flex items-center justify-between">
                      <p class="text-sm font-medium text-purple-600 truncate">{{ activity.title }}</p>
                      <div class="ml-2 flex-shrink-0 flex">
                        <p class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                          {{ activity.type }}
                        </p>
                      </div>
                    </div>
                    <div class="mt-2 sm:flex sm:justify-between">
                      <div class="sm:flex">
                        <p class="flex items-center text-sm text-gray-500">
                          <user-icon class="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" />
                          {{ activity.user }}
                        </p>
                      </div>
                      <div class="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                        <clock-icon class="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" />
                        <p>
                          {{ activity.date }}
                        </p>
                      </div>
                    </div>
                  </div>
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { BellIcon, ChevronDownIcon, UsersIcon, UserIcon, ClockIcon } from 'lucide-vue-next'
  
  const tasks = ref([
    { id: 'task1', title: 'Review new user signups', completed: true },
    { id: 'task2', title: 'Prepare monthly report', completed: false },
    { id: 'task3', title: 'Update privacy policy', completed: false },
  ])
  
  const recentActivity = ref([
    { id: 1, title: 'New user registered', type: 'User', user: 'Alice Johnson', date: '2 hours ago' },
    { id: 2, title: 'Project milestone completed', type: 'Project', user: 'Bob Smith', date: '4 hours ago' },
    { id: 3, title: 'New feature deployed', type: 'Development', user: 'Charlie Brown', date: 'Yesterday at 1:25 PM' },
  ])
  </script>
  
  <style scoped>
  /* Add any additional component-specific styles here */
  </style>