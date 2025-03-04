// Расширение типов для Vue Router
import 'vue-router';

/* Объявления типов для Vue Router */
declare module 'vue-router' {
  interface RouteMeta {
    requiresAuth?: boolean;
    requiresAdmin?: boolean;
  }
} 