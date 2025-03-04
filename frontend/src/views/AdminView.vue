<template>
  <div class="container mx-auto px-4 py-6">
    <h1 class="text-2xl font-bold mb-6">Панель администратора</h1>
    
    <!-- Панель навигации -->
    <div class="flex mb-6 border-b">
      <button @click="activeTab = 'users'" 
        :class="['px-4 py-2 mr-2', activeTab === 'users' ? 'border-b-2 border-primary text-primary font-semibold' : 'text-gray-600']">
        Пользователи
      </button>
      <button @click="activeTab = 'funds'" 
        :class="['px-4 py-2 mr-2', activeTab === 'funds' ? 'border-b-2 border-primary text-primary font-semibold' : 'text-gray-600']">
        Фонды
      </button>
    </div>

    <!-- Содержимое вкладки -->
    <div v-if="activeTab === 'users'">
      <UsersManagement />
    </div>
    <div v-else-if="activeTab === 'funds'">
      <FundsManagement />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import UsersManagement from '@/components/admin/UsersManagement.vue';
import FundsManagement from '@/components/admin/FundsManagement.vue';

const activeTab = ref('users');
</script> 