<template>
  <div>
    <h2 class="text-lg font-medium mb-4">Социальные сети</h2>
    <div v-if="player && player.social_media && player.social_media.length > 0">
      <div v-for="(social, index) in player.social_media" :key="index" class="mb-4 p-3 border rounded">
        <h3 class="font-semibold">{{ social.platform || 'Соцсеть' }}</h3>
        <p v-if="social.url"><strong>Ссылка:</strong> <a :href="social.url" target="_blank" class="text-blue-500 hover:underline">{{ social.url }}</a></p>
        <p v-if="social.username"><strong>Имя пользователя:</strong> {{ social.username }}</p>
        <p v-if="social.description"><strong>Описание:</strong> {{ social.description }}</p>
        <p><strong>Добавлена:</strong> {{ formatDate(social.created_at) }}</p>
      </div>
    </div>
    <div v-else class="text-center py-8 text-gray-500">
      Социальные сети не найдены
    </div>
  </div>
</template>

<script>
export default {
  name: 'SocialMediaTab',
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