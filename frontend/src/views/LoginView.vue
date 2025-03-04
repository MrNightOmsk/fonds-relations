<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900 dark:text-white">
          Вход в систему
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600 dark:text-gray-400">
          Fonds Relations - система для обмена информацией о недобросовестных игроках
        </p>
      </div>
      
      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="email" class="sr-only">Email</label>
            <input
              id="email"
              v-model="credentials.username"
              name="email"
              type="email"
              autocomplete="email"
              required
              class="form-input rounded-t-md"
              placeholder="Email"
            />
          </div>
          <div>
            <label for="password" class="sr-only">Пароль</label>
            <input
              id="password"
              v-model="credentials.password"
              name="password"
              type="password"
              autocomplete="current-password"
              required
              class="form-input rounded-b-md"
              placeholder="Пароль"
            />
          </div>
        </div>

        <div v-if="authStore.error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
          <span class="block sm:inline">{{ authStore.error }}</span>
        </div>

        <div>
          <button
            type="submit"
            class="btn-primary w-full"
            :disabled="authStore.loading"
          >
            <span v-if="authStore.loading">Вход...</span>
            <span v-else>Войти</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();

const credentials = reactive({
  username: '',
  password: ''
});

const handleLogin = async () => {
  await authStore.login(credentials);
};
</script> 