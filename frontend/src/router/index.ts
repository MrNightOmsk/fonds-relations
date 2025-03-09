// @ts-ignore
import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

// Ленивая загрузка компонентов для оптимизации
const Login = () => import('@/views/LoginView.vue');
const Dashboard = () => import('@/views/DashboardView.vue');
const DashboardTest = () => import('@/views/DashboardTestView.vue');
const NotFound = () => import('@/views/NotFoundView.vue');
const Admin = () => import('@/views/AdminView.vue');
const PlayersManagement = () => import('@/components/admin/PlayersManagement.vue');
const CasesManagement = () => import('@/components/admin/CasesManagement.vue');
const PlayerDetail = () => import('@/views/players/PlayerDetail.vue');
const PlayersList = () => import('@/views/players/PlayersListView.vue');
const CaseDetail = () => import('@/views/cases/CaseDetail.vue');
const CasesList = () => import('@/views/cases/CasesListView.vue');
const SearchIndexManagement = () => import('@/views/admin/SearchIndexView.vue');

// @ts-ignore
const routes = [
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
    path: '/dashboard-test',
    name: 'DashboardTest',
    component: DashboardTest,
    meta: { requiresAuth: true }
  },
  {
    path: '/cases',
    name: 'CasesList',
    component: CasesList,
    meta: { requiresAuth: true }
  },
  {
    path: '/players',
    name: 'PlayersList',
    component: PlayersList,
    meta: { requiresAuth: true }
  },
  {
    path: '/players/:id',
    name: 'PlayerDetail',
    component: PlayerDetail,
    meta: { requiresAuth: true },
    props: true
  },
  {
    path: '/cases/:id',
    name: 'CaseDetail',
    component: CaseDetail,
    meta: { requiresAuth: true },
    props: true
  },
  {
    path: '/admin',
    component: Admin,
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: '',
        name: 'Admin',
        meta: { requiresAuth: true, requiresAdmin: true }
      },
      {
        path: 'players',
        name: 'AdminPlayers',
        component: PlayersManagement,
        meta: { requiresAuth: true, requiresAdmin: true }
      },
      {
        path: 'cases',
        name: 'AdminCases',
        component: CasesManagement,
        meta: { requiresAuth: true, requiresAdmin: true }
      },
      {
        path: 'poker-rooms',
        component: () => import('../components/admin/PokerRoomsManagement.vue'),
        meta: { requiresAuth: true, requiresAdmin: true }
      },
      {
        path: 'search-index',
        name: 'SearchIndexManagement',
        component: SearchIndexManagement,
        meta: { requiresAuth: true, requiresAdmin: true }
      }
    ]
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
  
  console.log('Переход на маршрут:', to.path);
  console.log('Требуется аутентификация:', to.meta.requiresAuth);
  console.log('Требуется админ:', to.meta.requiresAdmin);
  console.log('Пользователь аутентифицирован:', authStore.isAuthenticated);
  console.log('Пользователь является админом:', authStore.isAdmin);

  // Маршрут требует аутентификации
  const requiresAuth = to.meta.requiresAuth !== false;
  const requiresAdmin = to.meta.requiresAdmin === true;

  if (requiresAuth && !authStore.isAuthenticated) {
    console.log('Перенаправление на /login: пользователь не аутентифицирован');
    next('/login');
  } else if (requiresAdmin && !authStore.isAdmin) {
    console.log('Перенаправление на /dashboard: пользователь не является администратором', 
                'isAdmin =', authStore.isAdmin);
    next('/dashboard');
  } else if (to.path === '/login' && authStore.isAuthenticated) {
    console.log('Перенаправление на /dashboard: пользователь уже аутентифицирован');
    next('/dashboard');
  } else {
    console.log('Разрешен доступ к маршруту:', to.path);
    next();
  }
});

export default router; 