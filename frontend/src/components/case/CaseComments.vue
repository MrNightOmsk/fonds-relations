<template>
  <div class="case-comments">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-lg font-medium">Комментарии ({{ comments.length }})</h2>
      
      <div>
        <select 
          v-model="filter" 
          class="p-2 border rounded-md text-sm"
        >
          <option value="all">Все комментарии</option>
          <option value="user">Только мои</option>
          <option value="important">Важные</option>
        </select>
      </div>
    </div>
    
    <!-- Форма добавления комментария -->
    <div class="bg-blue-50 p-4 rounded-lg mb-6">
      <h3 class="text-md font-medium mb-2">Добавить комментарий</h3>
      <div class="space-y-3">
        <textarea 
          v-model="newComment.text" 
          rows="3" 
          placeholder="Введите текст комментария"
          class="w-full p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-800"
        ></textarea>
        
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <input 
              type="checkbox" 
              id="important" 
              v-model="newComment.important"
              class="mr-2"
            />
            <label for="important" class="text-sm cursor-pointer">Отметить как важное</label>
          </div>
          
          <button 
            @click="addComment" 
            :disabled="!newComment.text.trim() || submitting"
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="submitting">Добавление...</span>
            <span v-else>Добавить комментарий</span>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Список комментариев -->
    <div v-if="filteredComments.length === 0" class="py-10 text-center text-gray-500">
      <p v-if="filter === 'all'">Нет комментариев. Будьте первым, кто оставит комментарий!</p>
      <p v-else-if="filter === 'user'">Вы еще не оставили ни одного комментария.</p>
      <p v-else-if="filter === 'important'">Нет важных комментариев.</p>
    </div>
    
    <div v-else class="space-y-4">
      <div 
        v-for="comment in filteredComments" 
        :key="comment.id" 
        class="bg-white p-4 rounded-lg shadow-sm border-l-4" 
        :class="comment.important ? 'border-yellow-500' : 'border-gray-200'"
      >
        <div class="flex justify-between items-start mb-2">
          <div class="flex items-center">
            <div class="w-8 h-8 bg-blue-100 text-blue-700 rounded-full flex items-center justify-center font-medium mr-2">
              {{ getUserInitials(comment.user_name) }}
            </div>
            <div>
              <span class="font-medium">{{ comment.user_name }}</span>
              <span class="text-sm text-gray-500 ml-2">{{ formatCommentDate(comment.created_at) }}</span>
            </div>
          </div>
          
          <div class="flex items-center">
            <span v-if="comment.important" class="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full mr-2">
              Важно
            </span>
            <button 
              v-if="canDelete(comment)" 
              @click="confirmDelete(comment)" 
              class="text-red-500 hover:text-red-700"
            >
              <span>✕</span>
            </button>
          </div>
        </div>
        
        <div class="pl-10 whitespace-pre-line">{{ comment.text }}</div>
      </div>
    </div>
    
    <!-- Модальное окно подтверждения удаления -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-lg max-w-md w-full">
        <h3 class="text-lg font-medium mb-3">Подтверждение удаления</h3>
        <p class="mb-4">Вы уверены, что хотите удалить этот комментарий? Это действие нельзя отменить.</p>
        
        <div class="flex justify-end space-x-3">
          <button 
            @click="showDeleteModal = false" 
            class="px-4 py-2 border rounded text-gray-700"
          >
            Отмена
          </button>
          <button 
            @click="deleteComment" 
            class="px-4 py-2 bg-red-600 text-white rounded"
          >
            Удалить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';

interface Comment {
  id: string;
  case_id: string;
  user_id: string;
  user_name: string;
  text: string;
  important: boolean;
  created_at: string;
}

const props = defineProps({
  caseId: {
    type: String,
    required: true
  }
});

const emit = defineEmits(['updated']);

// Состояние
const authStore = useAuthStore();
const comments = ref<Comment[]>([]);
const filter = ref('all');
const newComment = ref({
  text: '',
  important: false
});
const submitting = ref(false);
const loading = ref(false);
const showDeleteModal = ref(false);
const commentToDelete = ref<Comment | null>(null);

// Отфильтрованные комментарии
const filteredComments = computed(() => {
  if (filter.value === 'all') {
    return comments.value;
  }
  
  if (filter.value === 'user') {
    return comments.value.filter(comment => comment.user_id === authStore.userId);
  }
  
  if (filter.value === 'important') {
    return comments.value.filter(comment => comment.important);
  }
  
  return comments.value;
});

// Методы
const fetchComments = async () => {
  loading.value = true;
  
  try {
    // В реальном приложении здесь был бы API-запрос
    // const response = await fetch(`/api/cases/${props.caseId}/comments`);
    // comments.value = await response.json();
    
    // Имитация загрузки данных
    setTimeout(() => {
      comments.value = [
        {
          id: '1',
          case_id: props.caseId,
          user_id: '1',
          user_name: 'Администратор',
          text: 'Дело открыто и назначено на рассмотрение.',
          important: true,
          created_at: '2023-03-01T10:30:00Z'
        },
        {
          id: '2',
          case_id: props.caseId,
          user_id: '2',
          user_name: 'Иванов И.В.',
          text: 'Запросил дополнительную информацию от игрока по этому делу.',
          important: false,
          created_at: '2023-03-02T14:45:00Z'
        },
        {
          id: '3',
          case_id: props.caseId,
          user_id: authStore.userId,
          user_name: 'Вы',
          text: 'Отправил запрос на предоставление дополнительных доказательств.',
          important: false,
          created_at: '2023-03-03T09:20:00Z'
        }
      ];
      
      loading.value = false;
    }, 500);
  } catch (error) {
    console.error('Ошибка при загрузке комментариев:', error);
    loading.value = false;
  }
};

const addComment = async () => {
  if (!newComment.value.text.trim() || submitting.value) {
    return;
  }
  
  submitting.value = true;
  
  try {
    // В реальном приложении здесь был бы API-запрос
    // const response = await fetch(`/api/cases/${props.caseId}/comments`, {
    //   method: 'POST',
    //   headers: { 'Content-Type': 'application/json' },
    //   body: JSON.stringify({
    //     text: newComment.value.text,
    //     important: newComment.value.important
    //   })
    // });
    // const result = await response.json();
    
    // Имитация добавления комментария
    setTimeout(() => {
      const newCommentObject: Comment = {
        id: Date.now().toString(),
        case_id: props.caseId,
        user_id: authStore.userId,
        user_name: 'Вы',
        text: newComment.value.text,
        important: newComment.value.important,
        created_at: new Date().toISOString()
      };
      
      comments.value.unshift(newCommentObject);
      newComment.value.text = '';
      newComment.value.important = false;
      submitting.value = false;
      
      emit('updated');
    }, 500);
  } catch (error) {
    console.error('Ошибка при добавлении комментария:', error);
    submitting.value = false;
  }
};

const confirmDelete = (comment: Comment) => {
  commentToDelete.value = comment;
  showDeleteModal.value = true;
};

const deleteComment = async () => {
  if (!commentToDelete.value) return;
  
  try {
    // В реальном приложении здесь был бы API-запрос
    // await fetch(`/api/comments/${commentToDelete.value.id}`, {
    //   method: 'DELETE'
    // });
    
    // Имитация удаления комментария
    setTimeout(() => {
      comments.value = comments.value.filter(c => c.id !== commentToDelete.value!.id);
      showDeleteModal.value = false;
      commentToDelete.value = null;
      
      emit('updated');
    }, 300);
  } catch (error) {
    console.error('Ошибка при удалении комментария:', error);
  }
};

const canDelete = (comment: Comment): boolean => {
  // Может удалять свои комментарии или администратор может удалять любые
  return comment.user_id === authStore.userId || authStore.isAdmin;
};

const getUserInitials = (name: string): string => {
  const parts = name.split(' ');
  if (parts.length >= 2) {
    return `${parts[0][0]}${parts[1][0]}`.toUpperCase();
  }
  return name.substring(0, 2).toUpperCase();
};

const formatCommentDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

// Загрузка комментариев при монтировании компонента
onMounted(fetchComments);
</script>

<style scoped>
.case-comments {
  width: 100%;
}
</style> 