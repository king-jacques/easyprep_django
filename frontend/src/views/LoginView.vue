<template>
    <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-white-500/20 to-gray-500/20">
      <div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
        <h1 class="text-3xl font-bold mb-6 text-center text-gray-800">Log In</h1>
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div class="space-y-2">
            <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
            <input
              id="email"
              v-model="email"
              type="email"
              placeholder="johndoe@example.com"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div class="space-y-2">
            <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
            <div class="relative">
              <input
                id="password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="••••••••"
                required
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <button
                type="button"
                class="absolute right-3 top-1/2 transform -translate-y-1/2"
                @click="togglePasswordVisibility"
              >
                <eye-icon v-if="!showPassword" class="h-5 w-5 text-gray-400" />
                <eye-off-icon v-else class="h-5 w-5 text-gray-400" />
              </button>
            </div>
          </div>
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <input
                id="remember-me"
                v-model="rememberMe"
                type="checkbox"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label for="remember-me" class="ml-2 block text-sm text-gray-700">
                Remember me
              </label>
            </div>
            <div class="text-sm">
              <RouterLink to="/forgot-password" class="font-medium text-blue-600 hover:text-blue-500">
                Forgot your password?
              </RouterLink>
            </div>
          </div>
          <div v-if="errorMessage" style="color:red"> {{ errorMessage }}</div>
          <button
            type="submit"
            class="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Log In
          </button>
        </form>
        <p class="mt-4 text-center text-sm text-gray-600">
          Don't have an account?
          <RouterLink to="/signup" class="font-medium text-blue-600 hover:text-blue-500">
            Sign up
          </RouterLink>
        </p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { useRouter, RouterLink } from 'vue-router';
  import { ref } from 'vue'
  import { EyeIcon, EyeOffIcon } from 'lucide-vue-next'
  import axios from "axios";
  import { useUserStore } from '@/stores/user';
  import { storeToRefs } from 'pinia';
  import { API_URL } from '@/utils/constants';
  import {useToast} from 'vue-toastification';
  const userStore = useUserStore()
  const email = ref('')
  const password = ref('')
  const showPassword = ref(false)
  const rememberMe = ref(false)
  
  const togglePasswordVisibility = () => {
    showPassword.value = !showPassword.value
  }

  const toast = useToast()
  const errorMessage = ref("");
  const router = useRouter();
  
    const handleSubmit = async () => {
      try {
        const loginResponse = await axios.post(`${API_URL}/auth/login/`, {
          email: email.value,
          password: password.value,
        });

        if (loginResponse.status === 200) {
            const {user, token} = loginResponse.data;
            userStore.login(user, token)
            router.push("/dashboard"); // Redirect after login
        }
      } catch (error) {
        errorMessage.value = error.response?.data?.message;
        toast.error(error.response?.data?.message || 'Something went wrong. Login failed')
        console.log(error.response?.data?.message);
      }
    };


  </script>
  
  <style scoped>

  </style>