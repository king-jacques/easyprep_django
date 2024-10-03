import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignupView from '@/views/SignupView.vue'
import LoginView from '@/views/LoginView.vue'
import NotFoundView from '@/views/NotFoundView.vue'
import Dashboard from '@/views/Dashboard.vue'
import AdminView from '@/views/AdminView.vue'
import AdminToolsView from '@/views/AdminToolsView.vue'
import { useUserStore } from '@/stores/user'
import { storeToRefs } from 'pinia'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      // beforeEnter: (to, from, next) => {
      //   const userStore = useUserStore();
      //   if (userStore.isAuthenticated) {
      //     next('/dashboard'); // Redirect to dashboard if authenticated
      //   } else {
      //     next(); // Allow access to the home page
      //   }
      // },
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    },
    {
      path: '/tools',
      name: 'not-found',
      component: NotFoundView
    },
    {
      path: '/webscraper/:id',
      name: 'not-found',
      component: NotFoundView,
      meta: { requiresAuth: true}
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: Dashboard,
      meta: { requiresAuth: true}
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminView,
      meta: { requiresAuth: true}
    },
    {
      path: '/admintools',
      name: 'admintools',
      component: AdminToolsView,
      meta: { requiresAuth: true}
    },
    {
      path: '/:catchAll(.*)',
      name: 'not-found',
      component: NotFoundView,
    },
  ]
});

router.beforeEach((to, from, next) => {
  const userStore = useUserStore();

  if (userStore.isAuthenticated) {
    if (to.path === '/'){
      next('/dashboard')
    }
    else{
      next();
    }
    
  } else if (to.meta.requiresAuth) {
    // If the route requires authentication and the user is not logged in
    next('/login');  // Redirect to the login page
  } else {
    // Otherwise, allow navigation
    next();
  }
})

export default router
