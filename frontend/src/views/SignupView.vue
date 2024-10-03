<template>
    <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-white-500/20 to-gray-500/20">
      <div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
        <h1 class="text-3xl font-bold mb-6 text-center text-gray-800">Create an Account</h1>
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div class="space-y-2">
            <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
            <input
              id="username"
              v-model="username"
              type="text"
              placeholder="Username"
              required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
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
            <div class="mt-2">
              <div class="h-1 w-full bg-gray-200 rounded-full overflow-hidden">
                <div
                  class="h-full transition-all duration-300 ease-out"
                  :class="passwordStrengthClass"
                  :style="{ width: `${passwordStrength}%` }"
                ></div>
              </div>
              <p class="text-sm text-gray-600 mt-1">
                Password strength: {{ passwordStrengthText }}
              </p>
            </div>
          </div>
          <button
            type="submit"
            class="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Sign Up
          </button>
        </form>
        <p class="mt-4 text-center text-sm text-gray-600">
          Already have an account?
          <RouterLink to="/login" class="font-medium text-blue-600 hover:text-blue-500">
            Log in
          </RouterLink>
        </p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  import { EyeIcon, EyeOffIcon } from 'lucide-vue-next'
  import { RouterLink, useRouter } from 'vue-router';
  import axios from "axios";
  import { storeToRefs } from 'pinia';
  import PulseLoader from 'vue-spinner/src/PulseLoader.vue';
import { useUserStore } from '@/stores/user';
  
  const username = ref('')
  const email = ref('')
  const password = ref('')
  const showPassword = ref(false)
  
  const togglePasswordVisibility = () => {
    showPassword.value = !showPassword.value
  }
  
  console.log(storeToRefs(useUserStore).user)
  const userStore = useUserStore()
  const {user} = storeToRefs(userStore)

  const calculatePasswordStrength = (password) => {
    let strength = 0
    if (password.length > 6) strength += 20
    if (password.match(/[A-Z]/)) strength += 20
    if (password.match(/[a-z]/)) strength += 20
    if (password.match(/[0-9]/)) strength += 20
    if (password.match(/[^A-Za-z0-9]/)) strength += 20
    return strength
  }
  
  const passwordStrength = computed(() => calculatePasswordStrength(password.value))
  
  const passwordStrengthClass = computed(() => {
    if (passwordStrength.value <= 40) return 'bg-red-500'
    if (passwordStrength.value <= 80) return 'bg-yellow-500'
    return 'bg-green-500'
  })
  
  const passwordStrengthText = computed(() => {
    if (passwordStrength.value <= 40) return 'Weak'
    if (passwordStrength.value <= 80) return 'Medium'
    return 'Strong'
  })
  
  const handleSignup = () => {
    // Handle form submission here
    console.log('Form submitted:', { name: username.value, email: email.value, password: password.value })
  }

    const errorMessage = ref("");
    const router = useRouter();

    const handleSubmit = async () => {
      try {
        const signupResponse = await axios.post("api/auth/signup/", {
          username: username.value,
          email: email.value,
          password: password.value,
        });

        if (signupResponse.status === 201) {
            const {user, token} = signupResponse.data;
            userStore.login(user, token)
            // localStorage.setItem("authToken", token);
            router.push("/dashboard"); // Redirect after login
        }
      } catch (error) {
        errorMessage.value = "Sign up failed. Please try again.";
        console.error(error);
      }
    };
  </script>
  
  <style scoped>
  /* Add any additional component-specific styles here */
  </style>