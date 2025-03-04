<template>
  <div class="min-h-screen flex flex-col items-center justify-center text-center px-4">
    <h1 class="text-6xl font-bold text-primary mb-4">404</h1>
    <h2 class="text-2xl font-semibold mb-6">Страница не найдена</h2>
    <p class="text-gray-600 dark:text-gray-400 mb-8">
      Запрашиваемая страница не существует или была перемещена.
    </p>
    <router-link to="/" class="btn-primary">
      Вернуться на главную
    </router-link>
  </div>
</template> 