<template>
  <div class="case-evidences">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-lg font-medium">Доказательства ({{ evidences.length }})</h2>
      
      <button 
        @click="showAddEvidence = true" 
        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
      >
        Добавить доказательство
      </button>
    </div>
    
    <!-- Список доказательств -->
    <div v-if="loading" class="text-center py-8">
      <div class="inline-block animate-spin h-6 w-6 border-2 border-blue-500 rounded-full border-t-transparent mb-2"></div>
      <p class="text-gray-600">Загрузка доказательств...</p>
    </div>
    
    <div v-else-if="evidences.length === 0" class="py-10 text-center text-gray-500">
      <p>Нет доказательств по этому делу.</p>
      <button 
        @click="showAddEvidence = true" 
        class="mt-3 text-blue-600 hover:underline"
      >
        Добавить первое доказательство
      </button>
    </div>
    
    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div 
        v-for="evidence in evidences" 
        :key="evidence.id" 
        class="bg-white p-4 rounded-lg shadow-sm border"
      >
        <div class="flex justify-between items-start mb-3">
          <div>
            <h3 class="font-medium">{{ evidence.title }}</h3>
            <p class="text-sm text-gray-500">
              Добавлено {{ formatDate(evidence.created_at) }} 
              <span v-if="evidence.user_name">пользователем {{ evidence.user_name }}</span>
            </p>
          </div>
          
          <button 
            v-if="canDelete(evidence)" 
            @click="confirmDelete(evidence)" 
            class="text-red-500 hover:text-red-700 ml-2"
          >
            <span>✕</span>
          </button>
        </div>
        
        <p v-if="evidence.description" class="text-gray-700 mb-3">{{ evidence.description }}</p>
        
        <!-- Превью файла -->
        <div class="mb-3">
          <div v-if="isImage(evidence.file_type)" class="mb-2">
            <img 
              :src="evidence.file_url" 
              :alt="evidence.title" 
              class="max-w-full h-auto rounded-md"
              @click="openPreview(evidence)"
            />
          </div>
          <div v-else-if="isDocument(evidence.file_type)" class="p-3 bg-gray-100 rounded-md flex items-center">
            <span class="text-lg mr-2">📄</span>
            <span class="truncate flex-1">{{ evidence.file_name }}</span>
          </div>
          <div v-else class="p-3 bg-gray-100 rounded-md flex items-center">
            <span class="text-lg mr-2">📎</span>
            <span class="truncate flex-1">{{ evidence.file_name }}</span>
          </div>
        </div>
        
        <div class="flex justify-end space-x-2">
          <a 
            :href="evidence.file_url" 
            target="_blank"
            class="text-blue-600 hover:text-blue-800 text-sm"
          >
            Просмотреть
          </a>
          <a 
            :href="evidence.file_url" 
            download
            class="text-blue-600 hover:text-blue-800 text-sm"
          >
            Скачать
          </a>
        </div>
      </div>
    </div>
    
    <!-- Модальное окно добавления доказательства -->
    <div 
      v-if="showAddEvidence" 
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white p-6 rounded-lg max-w-lg w-full">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-medium">Добавить доказательство</h3>
          <button 
            @click="showAddEvidence = false" 
            class="text-gray-500 hover:text-gray-700"
          >
            <span>✕</span>
          </button>
        </div>
        
        <form @submit.prevent="addEvidence" class="space-y-4">
          <div>
            <label for="title" class="block text-sm font-medium text-gray-700 mb-1">Название</label>
            <input 
              type="text" 
              id="title" 
              v-model="newEvidence.title" 
              class="w-full px-3 py-2 border rounded-md text-gray-800" 
              required
            />
          </div>
          
          <div>
            <label for="description" class="block text-sm font-medium text-gray-700 mb-1">Описание</label>
            <textarea 
              id="description" 
              v-model="newEvidence.description" 
              rows="3" 
              class="w-full px-3 py-2 border rounded-md text-gray-800"
            ></textarea>
          </div>
          
          <div>
            <label for="file" class="block text-sm font-medium text-gray-700 mb-1">Файл</label>
            <div 
              class="border-dashed border-2 border-gray-300 rounded-md p-6 text-center"
              :class="{'bg-blue-50': isDragging}"
              @dragover.prevent="isDragging = true"
              @dragleave.prevent="isDragging = false"
              @drop.prevent="handleFileDrop"
            >
              <input 
                type="file" 
                id="file" 
                ref="fileInput"
                @change="handleFileChange" 
                class="hidden"
              />
              
              <div v-if="selectedFile">
                <p class="mb-2 font-medium">Выбранный файл:</p>
                <p class="text-sm text-gray-800">{{ selectedFile.name }} ({{ formatFileSize(selectedFile.size) }})</p>
                <button 
                  type="button" 
                  @click="resetFile" 
                  class="mt-2 text-sm text-red-600 hover:text-red-800"
                >
                  Удалить
                </button>
              </div>
              
              <div v-else>
                <p class="mb-2">Перетащите файл сюда или</p>
                <button 
                  type="button" 
                  @click="$refs.fileInput.click()" 
                  class="px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700"
                >
                  Выберите файл
                </button>
              </div>
            </div>
          </div>
          
          <div class="flex justify-end space-x-3 pt-2">
            <button 
              type="button" 
              @click="showAddEvidence = false" 
              class="px-4 py-2 border rounded text-gray-700"
            >
              Отмена
            </button>
            <button 
              type="submit" 
              :disabled="submitting || !selectedFile"
              class="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="submitting">Загрузка...</span>
              <span v-else>Добавить</span>
            </button>
          </div>
        </form>
      </div>
    </div>
    
    <!-- Модальное окно просмотра изображения -->
    <div 
      v-if="previewEvidence && isImage(previewEvidence.file_type)" 
      class="fixed inset-0 bg-black bg-opacity-90 flex items-center justify-center z-50"
      @click="previewEvidence = null"
    >
      <div class="max-w-4xl max-h-[90vh]">
        <img 
          :src="previewEvidence.file_url" 
          :alt="previewEvidence.title" 
          class="max-w-full max-h-[90vh] object-contain"
        />
      </div>
    </div>
    
    <!-- Модальное окно подтверждения удаления -->
    <div 
      v-if="showDeleteModal" 
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white p-6 rounded-lg max-w-md w-full">
        <h3 class="text-lg font-medium mb-3">Подтверждение удаления</h3>
        <p class="mb-4">Вы уверены, что хотите удалить это доказательство? Это действие нельзя отменить.</p>
        
        <div class="flex justify-end space-x-3">
          <button 
            @click="showDeleteModal = false" 
            class="px-4 py-2 border rounded text-gray-700"
          >
            Отмена
          </button>
          <button 
            @click="deleteEvidence" 
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
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';

interface Evidence {
  id: string;
  case_id: string;
  user_id: string;
  user_name?: string;
  title: string;
  description?: string;
  file_url: string;
  file_name: string;
  file_type: string;
  file_size: number;
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
const evidences = ref<Evidence[]>([]);
const loading = ref(false);
const submitting = ref(false);
const showAddEvidence = ref(false);
const showDeleteModal = ref(false);
const isDragging = ref(false);
const selectedFile = ref<File | null>(null);
const fileInput = ref<HTMLInputElement | null>(null);
const evidenceToDelete = ref<Evidence | null>(null);
const previewEvidence = ref<Evidence | null>(null);

const newEvidence = ref({
  title: '',
  description: ''
});

// Методы
const fetchEvidences = async () => {
  loading.value = true;
  
  try {
    // В реальном приложении здесь был бы API-запрос
    // const response = await fetch(`/api/cases/${props.caseId}/evidences`);
    // evidences.value = await response.json();
    
    // Имитация загрузки данных
    setTimeout(() => {
      evidences.value = [
        {
          id: '1',
          case_id: props.caseId,
          user_id: '1',
          user_name: 'Администратор',
          title: 'Скриншот переписки',
          description: 'Скриншот переписки с игроком, где он признает долг',
          file_url: 'https://via.placeholder.com/800x600.png?text=Скриншот+переписки',
          file_name: 'screenshot.png',
          file_type: 'image/png',
          file_size: 256000,
          created_at: '2023-03-01T10:30:00Z'
        },
        {
          id: '2',
          case_id: props.caseId,
          user_id: '2',
          user_name: 'Иванов И.В.',
          title: 'Выписка из банка',
          description: 'Подтверждение транзакции от игрока',
          file_url: 'https://via.placeholder.com/800x1000.png?text=Выписка+из+банка',
          file_name: 'bank_statement.pdf',
          file_type: 'application/pdf',
          file_size: 512000,
          created_at: '2023-03-02T14:45:00Z'
        }
      ];
      
      loading.value = false;
    }, 500);
  } catch (error) {
    console.error('Ошибка при загрузке доказательств:', error);
    loading.value = false;
  }
};

const handleFileChange = (event: Event) => {
  const input = event.target as HTMLInputElement;
  if (input.files && input.files.length > 0) {
    selectedFile.value = input.files[0];
  }
};

const handleFileDrop = (event: DragEvent) => {
  isDragging.value = false;
  
  if (event.dataTransfer?.files.length) {
    selectedFile.value = event.dataTransfer.files[0];
  }
};

const resetFile = () => {
  selectedFile.value = null;
  if (fileInput.value) {
    fileInput.value.value = '';
  }
};

const addEvidence = async () => {
  if (!selectedFile.value || submitting.value) {
    return;
  }
  
  submitting.value = true;
  
  try {
    // В реальном приложении здесь был бы API-запрос для загрузки файла
    // const formData = new FormData();
    // formData.append('file', selectedFile.value);
    // formData.append('title', newEvidence.value.title);
    // formData.append('description', newEvidence.value.description);
    // 
    // const response = await fetch(`/api/cases/${props.caseId}/evidences`, {
    //   method: 'POST',
    //   body: formData
    // });
    // const result = await response.json();
    
    // Имитация добавления доказательства
    setTimeout(() => {
      const file = selectedFile.value!;
      const newEvidenceObj: Evidence = {
        id: Date.now().toString(),
        case_id: props.caseId,
        user_id: authStore.userId,
        user_name: 'Вы',
        title: newEvidence.value.title,
        description: newEvidence.value.description,
        file_url: URL.createObjectURL(file), // Временный URL для локального файла
        file_name: file.name,
        file_type: file.type,
        file_size: file.size,
        created_at: new Date().toISOString()
      };
      
      evidences.value.unshift(newEvidenceObj);
      
      // Сброс формы
      newEvidence.value.title = '';
      newEvidence.value.description = '';
      resetFile();
      showAddEvidence.value = false;
      submitting.value = false;
      
      emit('updated');
    }, 1000);
  } catch (error) {
    console.error('Ошибка при добавлении доказательства:', error);
    submitting.value = false;
  }
};

const confirmDelete = (evidence: Evidence) => {
  evidenceToDelete.value = evidence;
  showDeleteModal.value = true;
};

const deleteEvidence = async () => {
  if (!evidenceToDelete.value) return;
  
  try {
    // В реальном приложении здесь был бы API-запрос
    // await fetch(`/api/evidences/${evidenceToDelete.value.id}`, {
    //   method: 'DELETE'
    // });
    
    // Имитация удаления доказательства
    setTimeout(() => {
      evidences.value = evidences.value.filter(e => e.id !== evidenceToDelete.value!.id);
      showDeleteModal.value = false;
      evidenceToDelete.value = null;
      
      emit('updated');
    }, 300);
  } catch (error) {
    console.error('Ошибка при удалении доказательства:', error);
  }
};

const openPreview = (evidence: Evidence) => {
  if (isImage(evidence.file_type)) {
    previewEvidence.value = evidence;
  }
};

const canDelete = (evidence: Evidence): boolean => {
  // Может удалять свои доказательства или администратор может удалять любые
  return evidence.user_id === authStore.userId || authStore.isAdmin;
};

const isImage = (fileType: string): boolean => {
  return fileType.startsWith('image/');
};

const isDocument = (fileType: string): boolean => {
  return fileType === 'application/pdf' || 
         fileType.includes('word') || 
         fileType.includes('excel') || 
         fileType.includes('powerpoint') || 
         fileType.includes('text');
};

const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) {
    return bytes + ' Б';
  } else if (bytes < 1048576) {
    return (bytes / 1024).toFixed(1) + ' КБ';
  } else {
    return (bytes / 1048576).toFixed(1) + ' МБ';
  }
};

const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

// Загрузка доказательств при монтировании компонента
onMounted(fetchEvidences);
</script>

<style scoped>
.case-evidences {
  width: 100%;
}
</style> 