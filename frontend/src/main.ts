import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';

// Импорт Tailwind CSS
import './assets/styles/main.css';

// Создание экземпляра приложения
const app = createApp(App);

// Добавление Pinia для управления состоянием
app.use(createPinia());

// Добавление маршрутизации
app.use(router);

// Монтирование приложения
app.mount('#app'); 