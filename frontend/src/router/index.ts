import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

// Ленивая загрузка компонентов для оптимизации
const Login = () => import('@/views/LoginView.vue');
const Dashboard = () => import('@/views/DashboardView.vue');
const NotFound = () => import('@/views/NotFoundView.vue');
const Admin = () => import('@/views/AdminView.vue');

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Защита маршрутов
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const requiresAuth = to.meta.requiresAuth !== false;
  const requiresAdmin = to.meta.requiresAdmin === true;

  if (requiresAuth && !authStore.isAuthenticated) {
    next('/login');
  } else if (requiresAdmin && authStore.user?.role !== 'admin') {
    next('/dashboard'); // Перенаправляем на дашборд, если пользователь не админ
  } else {
    next();
  }
});

export default router; 