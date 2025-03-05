<template>
  <div class="social-media">
    <h3 class="text-lg font-medium mb-2">Социальные сети</h3>

    <!-- Список социальных сетей -->
    <div v-if="socialMedias.length" class="mb-4 space-y-2">
      <div 
        v-for="media in socialMedias" 
        :key="media.id" 
        class="p-3 bg-white border rounded-lg shadow-sm"
      >
        <div class="flex justify-between items-start">
          <div>
            <div class="flex items-center">
              <span 
                class="px-2 py-1 rounded-full text-xs font-medium mr-2"
                :class="getPlatformClass(media.platform)"
              >
                {{ getPlatformName(media.platform) }}
              </span>
              <a 
                :href="getMediaUrl(media.platform, media.username)" 
                target="_blank" 
                class="font-medium text-blue-600 hover:underline"
              >
                {{ media.username }}
              </a>
            </div>
            <div v-if="media.description" class="text-sm text-gray-600 mt-1">
              {{ media.description }}
            </div>
          </div>
          <div v-if="editable" class="flex space-x-2">
            <button 
              @click="deleteMedia(media.id)"
              class="text-red-500 hover:text-red-700" 
              title="Удалить"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="text-gray-500 mb-4 p-3 bg-gray-50 rounded-lg text-center">
      У игрока нет связанных социальных сетей
    </div>

    <!-- Форма добавления социальной сети -->
    <div v-if="editable" class="border rounded-lg p-4 bg-gray-50">
      <h4 class="font-medium mb-3">Добавить социальную сеть</h4>
      <div class="grid gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Платформа</label>
          <select v-model="newMedia.platform" class="w-full p-2 border rounded">
            <option value="telegram">Telegram</option>
            <option value="vk">ВКонтакте</option>
            <option value="instagram">Instagram</option>
            <option value="facebook">Facebook</option>
            <option value="twitter">Twitter</option>
            <option value="other">Другое</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Имя пользователя</label>
          <input 
            v-model="newMedia.username" 
            type="text" 
            class="w-full p-2 border rounded"
            placeholder="@username или ссылка"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Описание (опционально)</label>
          <textarea 
            v-model="newMedia.description" 
            class="w-full p-2 border rounded"
            rows="2"
            placeholder="Дополнительная информация"
          ></textarea>
        </div>
        <div>
          <button 
            @click="addMedia" 
            class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            :disabled="!newMedia.username"
          >
            Добавить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import type { PlayerSocialMedia } from '@/types/models';

const props = defineProps<{
  modelValue: PlayerSocialMedia[];
  playerId: string;
  editable?: boolean;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', medias: PlayerSocialMedia[]): void;
  (e: 'add', media: Partial<PlayerSocialMedia>): void;
  (e: 'delete', mediaId: string): void;
}>();

const socialMedias = computed({
  get: () => props.modelValue || [],
  set: (value) => emit('update:modelValue', value)
});

const newMedia = ref<Partial<PlayerSocialMedia>>({
  player_id: props.playerId,
  platform: 'telegram',
  username: '',
  description: ''
});

watch(() => props.playerId, (newPlayerId) => {
  newMedia.value.player_id = newPlayerId;
});

function getPlatformName(platform: string): string {
  const platforms: Record<string, string> = {
    'telegram': 'Telegram',
    'vk': 'ВКонтакте',
    'instagram': 'Instagram',
    'facebook': 'Facebook',
    'twitter': 'Twitter',
    'other': 'Другое'
  };
  return platforms[platform] || platform;
}

function getPlatformClass(platform: string): string {
  const classes: Record<string, string> = {
    'telegram': 'bg-blue-100 text-blue-800',
    'vk': 'bg-indigo-100 text-indigo-800',
    'instagram': 'bg-pink-100 text-pink-800',
    'facebook': 'bg-blue-100 text-blue-800',
    'twitter': 'bg-sky-100 text-sky-800', 
    'other': 'bg-gray-100 text-gray-800'
  };
  return classes[platform] || 'bg-gray-100 text-gray-800';
}

function getMediaUrl(platform: string, username: string): string {
  if (username.startsWith('http')) return username;
  
  const baseUrls: Record<string, string> = {
    'telegram': 'https://t.me/',
    'vk': 'https://vk.com/',
    'instagram': 'https://instagram.com/',
    'facebook': 'https://facebook.com/',
    'twitter': 'https://twitter.com/'
  };
  
  const baseUrl = baseUrls[platform] || '#';
  const formattedUsername = username.startsWith('@') ? username.substring(1) : username;
  
  return `${baseUrl}${formattedUsername}`;
}

function addMedia() {
  if (!newMedia.value.username) return;
  
  emit('add', { ...newMedia.value });
  
  // Сброс формы
  newMedia.value = {
    player_id: props.playerId,
    platform: 'telegram',
    username: '',
    description: ''
  };
}

function deleteMedia(mediaId: string) {
  if (!mediaId) return;
  emit('delete', mediaId);
}
</script> 