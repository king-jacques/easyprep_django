<script setup>
import logo from '@/assets/img/logo.png';
import { RouterLink, useRoute } from 'vue-router';
import LogoutButton from './buttons/LogoutButton.vue';
import { useUserStore } from '@/stores/user';
import { computed } from 'vue';
const userStore = useUserStore()
const isAuthenticated = computed(() => userStore.isAuthenticated)
const isActiveLink = (routePath) => {
  const route = useRoute();
  return route.path === routePath;

}
</script>

<template>
    <nav class="bg-gray-700 border-b border-gray-500">
      <div class="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
        <div class="flex h-20 items-center justify-between">
          <div
            class="flex flex-1 items-center justify-center md:items-stretch md:justify-start"
          >
            <!-- Logo -->
            <RouterLink class="flex flex-shrink-0 items-center mr-4" to="/">
              <img class="h-10 w-auto" :src="logo" alt="Vue Jobs" />
              <span class="hidden md:block text-white text-2xl font-bold ml-2"
                >Tools</span
              >
            </RouterLink>
            <div class="md:ml-auto">
              <div class="flex space-x-2">
                <RouterLink
                  to="/"
                  :class="[isActiveLink('/') ? 'bg-gray-900' : 'hover:bg-gray-900 hover:text-white', 'text-white', 'rounded-md', 'px-3', 'py-2']"
                  >Home</RouterLink>
                <template v-if="!isAuthenticated">
                  <RouterLink
                    to="/login"
                    :class="[isActiveLink('/login') ? 'bg-gray-900' : 'hover:bg-gray-900 hover:text-white', 'text-white', 'rounded-md', 'px-3', 'py-2']"

                    >Log in</RouterLink>
                  <RouterLink
                    to="signup"
                    :class="[isActiveLink('/signup') ? 'bg-gray-900' : 'hover:bg-gray-900 hover:text-white', 'text-white', 'rounded-md', 'px-3', 'py-2']"

                    >Sign up</RouterLink>
                </template>
                <template v-if="isAuthenticated">
                  <RouterLink
                    to="admintools"
                    :class="[isActiveLink('/admintools') ? 'bg-gray-900' : 'hover:bg-gray-900 hover:text-white', 'text-white', 'rounded-md', 'px-3', 'py-2']"

                    >Admin Tools</RouterLink>
                  <LogoutButton />

                </template>
                  
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>
</template>