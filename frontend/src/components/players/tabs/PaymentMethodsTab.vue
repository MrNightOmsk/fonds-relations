<template>
  <div>
    <h2 class="text-lg font-medium mb-4">Методы оплаты</h2>
    <div v-if="player && player.payment_methods && player.payment_methods.length > 0">
      <div v-for="(method, index) in player.payment_methods" :key="index" class="mb-4 p-3 border rounded">
        <h3 class="font-semibold">{{ method.type || 'Метод оплаты' }}</h3>
        <p><strong>Значение:</strong> {{ method.value || 'Нет данных' }}</p>
        <p v-if="method.description"><strong>Описание:</strong> {{ method.description }}</p>
        <p><strong>Добавлен:</strong> {{ formatDate(method.created_at) }}</p>
      </div>
    </div>
    <div v-else class="text-center py-8 text-gray-500">
      Методы оплаты не найдены
    </div>
  </div>
</template>

<script>
export default {
  name: 'PaymentMethodsTab',
  props: {
    player: {
      type: Object,
      required: true
    }
  },
  methods: {
    formatDate(dateString) {
      if (!dateString) return 'Нет данных';
      const date = new Date(dateString);
      return new Intl.DateTimeFormat('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date);
    }
  }
}
</script> 