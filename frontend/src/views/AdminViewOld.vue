<template>
    <div class="min-h-screen bg-gray-100">
      <!-- Header -->
      <header class="bg-white shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 class="text-2xl font-semibold text-gray-900">Admin Dashboard</h1>
          <div class="flex items-center">
            <button class="p-2 rounded-full bg-gray-200 text-gray-600 hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500">
              <bell-icon class="h-6 w-6" />
            </button>
            <div class="ml-3 relative">
              <div>
                <button class="flex items-center focus:outline-none">
                  <img class="h-8 w-8 rounded-full" src="" alt="Admin avatar" />
                  <span class="ml-2 text-sm font-medium text-gray-700">Admin User</span>
                  <chevron-down-icon class="ml-1 h-4 w-4 text-gray-400" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </header>
  
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
          <!-- User Management Card -->
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center justify-between">
                <h3 class="text-lg leading-6 font-medium text-gray-900">User Management</h3>
                <users-icon class="h-6 w-6 text-purple-500" />
              </div>
              <div class="mt-4">
                <p class="text-sm text-gray-500">Manage user accounts, permissions, and roles.</p>
              </div>
            </div>
            <div class="bg-gray-50 px-5 py-3">
              <button @click="activeTab = 'users'" class="text-sm font-medium text-purple-600 hover:text-purple-500">
                Manage Users
              </button>
            </div>
          </div>
  
          <!-- Analytics Card -->
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center justify-between">
                <h3 class="text-lg leading-6 font-medium text-gray-900">Analytics</h3>
                <bar-chart-icon class="h-6 w-6 text-purple-500" />
              </div>
              <div class="mt-4">
                <p class="text-sm text-gray-500">View detailed analytics and generate reports.</p>
              </div>
            </div>
            <div class="bg-gray-50 px-5 py-3">
              <button @click="activeTab = 'analytics'" class="text-sm font-medium text-purple-600 hover:text-purple-500">
                View Analytics
              </button>
            </div>
          </div>
  
          <!-- System Settings Card -->
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-5">
              <div class="flex items-center justify-between">
                <h3 class="text-lg leading-6 font-medium text-gray-900">System Settings</h3>
                <settings-icon class="h-6 w-6 text-purple-500" />
              </div>
              <div class="mt-4">
                <p class="text-sm text-gray-500">Configure system-wide settings and preferences.</p>
              </div>
            </div>
            <div class="bg-gray-50 px-5 py-3">
              <button @click="activeTab = 'settings'" class="text-sm font-medium text-purple-600 hover:text-purple-500">
                Manage Settings
              </button>
            </div>
          </div>
        </div>
  
        <!-- Active Tab Content -->
        <div class="mt-8 bg-white shadow overflow-hidden sm:rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <div v-if="activeTab === 'users'">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">User Management</h3>
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="user in users" :key="user.id">
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ user.name }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ user.email }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ user.role }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button class="text-purple-600 hover:text-purple-900 mr-2">Edit</button>
                      <button class="text-red-600 hover:text-red-900">Delete</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-else-if="activeTab === 'analytics'">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Analytics</h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="bg-gray-50 p-4 rounded-lg">
                  <h4 class="text-sm font-medium text-gray-500 mb-2">Total Users</h4>
                  <p class="text-3xl font-semibold text-gray-900">{{ analytics.totalUsers }}</p>
                </div>
                <div class="bg-gray-50 p-4 rounded-lg">
                  <h4 class="text-sm font-medium text-gray-500 mb-2">Active Users</h4>
                  <p class="text-3xl font-semibold text-gray-900">{{ analytics.activeUsers }}</p>
                </div>
                <div class="bg-gray-50 p-4 rounded-lg">
                  <h4 class="text-sm font-medium text-gray-500 mb-2">Revenue</h4>
                  <p class="text-3xl font-semibold text-gray-900">${{ analytics.revenue.toLocaleString() }}</p>
                </div>
                <div class="bg-gray-50 p-4 rounded-lg">
                  <h4 class="text-sm font-medium text-gray-500 mb-2">Conversion Rate</h4>
                  <p class="text-3xl font-semibold text-gray-900">{{ analytics.conversionRate }}%</p>
                </div>
              </div>
            </div>
            <div v-else-if="activeTab === 'settings'">
              <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">System Settings</h3>
              <form @submit.prevent="saveSettings" class="space-y-4">
                <div>
                  <label for="site-name" class="block text-sm font-medium text-gray-700">Site Name</label>
                  <input type="text" id="site-name" v-model="settings.siteName" class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-purple-500 focus:border-purple-500 sm:text-sm" />
                </div>
                <div>
                  <label for="maintenance-mode" class="block text-sm font-medium text-gray-700">Maintenance Mode</label>
                  <select id="maintenance-mode" v-model="settings.maintenanceMode" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm rounded-md">
                    <option value="off">Off</option>
                    <option value="on">On</option>
                  </select>
                </div>
                <div>
                  <label for="default-language" class="block text-sm font-medium text-gray-700">Default Language</label>
                  <select id="default-language" v-model="settings.defaultLanguage" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-purple-500 focus:border-purple-500 sm:text-sm rounded-md">
                    <option value="en">English</option>
                    <option value="es">Spanish</option>
                    <option value="fr">French</option>
                  </select>
                </div>
                <div>
                  <button type="submit" class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500">
                    Save Settings
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { BellIcon, ChevronDownIcon, UsersIcon, BarChartIcon, SettingsIcon } from 'lucide-vue-next'
  
  const activeTab = ref('users')
  
  const users = ref([
    { id: 1, name: 'John Doe', email: 'john@example.com', role: 'Admin' },
    { id: 2, name: 'Jane Smith', email: 'jane@example.com', role: 'Editor' },
    { id: 3, name: 'Bob Johnson', email: 'bob@example.com', role: 'User' },
  ])
  
  const analytics = ref({
    totalUsers: 10897,
    activeUsers: 8234,
    revenue: 125000,
    conversionRate: 3.2,
  })
  
  const settings = ref({
    siteName: 'My Awesome Site',
    maintenanceMode: 'off',
    defaultLanguage: 'en',
  })
  
  const saveSettings = () => {
    // Implement save settings logic here
    console.log('Settings saved:', settings.value)
  }
  </script>
  
  <style scoped>
  /* Add any additional component-specific styles here */
  </style>