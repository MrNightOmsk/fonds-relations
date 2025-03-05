<template>
  <div class="case-comments">
    <h3 class="text-lg font-medium mb-2">Комментарии</h3>

    <!-- Список комментариев -->
    <div v-if="loading" class="text-center py-4">
      <div class="animate-spin h-8 w-8 border-4 border-blue-500 rounded-full border-t-transparent mx-auto"></div>
      <p class="mt-2 text-gray-600">Загрузка комментариев...</p>
    </div>

    <div v-else-if="comments.length" class="mb-4 space-y-3">
      <div 
        v-for="comment in sortedComments" 
        :key="comment.id" 
        class="p-4 bg-white border rounded-lg shadow-sm"
      >
        <div class="flex justify-between items-start">
          <div class="flex items-start">
            <div class="avatar w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center text-gray-700 font-medium mr-3">
              {{ getInitials(comment.created_by_name) }}
            </div>
            <div>
              <div class="font-medium">{{ comment.created_by_name }}</div>
              <div class="text-sm text-gray-500">
                {{ formatDate(comment.created_at) }}
              </div>
            </div>
          </div>
        </div>
        <div class="mt-3 text-gray-800 whitespace-pre-line">
          {{ comment.text }}
        </div>
      </div>
    </div>

    <div v-else class="text-gray-500 mb-4 p-3 bg-gray-50 rounded-lg text-center">
      Нет комментариев
    </div>

    <!-- Форма добавления комментария -->
    <div class="border rounded-lg p-4 bg-gray-50">
      <h4 class="font-medium mb-3">Добавить комментарий</h4>
      <div class="grid gap-4">
        <div>
          <textarea 
            v-model="newComment.text" 
            class="w-full p-3 border rounded"
            rows="3"
            placeholder="Введите комментарий..."
            :disabled="submitting"
          ></textarea>
        </div>
        <div class="flex justify-end">
          <button 
            @click="addComment" 
            class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            :disabled="!newComment.text || submitting"
          >
            <span v-if="submitting">
              <span class="inline-block h-4 w-4 border-2 border-white rounded-full border-t-transparent animate-spin mr-2 align-middle"></span>
              Отправка...
            </span>
            <span v-else>Добавить комментарий</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import type { CaseComment } from '@/types/models';
import { useAuthStore } from '@/stores/auth';

const props = defineProps<{
  caseId: string;
}>();

const emit = defineEmits<{
  (e: 'comment-added', comment: CaseComment): void;
}>();

const authStore = useAuthStore();
const comments = ref<CaseComment[]>([]);
const loading = ref(false);
const submitting = ref(false);
const error = ref<string | null>(null);

const newComment = ref({
  text: '',
  case_id: props.caseId
});

const sortedComments = computed(() => {
  return [...comments.value].sort((a, b) => {
    return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
  });
});

onMounted(async () => {
  await fetchComments();
});

async function fetchComments() {
  loading.value = true;
  error.value = null;
  
  try {
    // Здесь нужно заменить на реальный API-вызов
    // comments.value = await api.fetchCaseComments(props.caseId);
    comments.value = []; // Временно, пока не реализован API-запрос
  } catch (err) {
    error.value = 'Не удалось загрузить комментарии';
    console.error('Error fetching comments:', err);
  } finally {
    loading.value = false;
  }
}

async function addComment() {
  if (!newComment.value.text) return;
  
  submitting.value = true;
  error.value = null;
  
  try {
    // Здесь нужно заменить на реальный API-вызов
    // const createdComment = await api.createCaseComment({
    //   ...newComment.value,
    //   case_id: props.caseId
    // });
    
    // Временный код, который симулирует создание комментария
    const createdComment: CaseComment = {
      id: Math.random().toString(36).substring(2, 9),
      case_id: props.caseId,
      text: newComment.value.text,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      created_by: authStore.userId || '',
      created_by_name: authStore.userName || 'Пользователь'
    };
    
    comments.value.unshift(createdComment);
    emit('comment-added', createdComment);
    
    // Сброс формы
    newComment.value.text = '';
  } catch (err) {
    error.value = 'Не удалось добавить комментарий';
    console.error('Error adding comment:', err);
  } finally {
    submitting.value = false;
  }
}

function getInitials(name: string): string {
  if (!name) return '';
  
  return name
    .split(' ')
    .map(part => part[0])
    .join('')
    .toUpperCase()
    .substring(0, 2);
}

function formatDate(dateString: string): string {
  if (!dateString) return '';
  
  const date = new Date(dateString);
  return date.toLocaleString('ru-RU', { 
    day: '2-digit', 
    month: '2-digit', 
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}
</script> 