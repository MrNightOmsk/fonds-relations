<template>
  <div class="case-evidences">
    <h3 class="text-lg font-medium mb-2">Доказательства</h3>

    <!-- Список доказательств -->
    <div v-if="loading" class="text-center py-4">
      <div class="animate-spin h-8 w-8 border-4 border-blue-500 rounded-full border-t-transparent mx-auto"></div>
      <p class="mt-2 text-gray-600">Загрузка доказательств...</p>
    </div>

    <div v-else-if="evidences.length" class="mb-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div 
        v-for="evidence in evidences" 
        :key="evidence.id" 
        class="border rounded-lg overflow-hidden shadow-sm bg-white"
      >
        <div class="relative group">
          <!-- Изображение с заглушкой для неизображений -->
          <div v-if="isImage(evidence.file_type)" class="h-40 overflow-hidden bg-gray-100">
            <img :src="evidence.file_url" :alt="evidence.title || 'Доказательство'" class="w-full h-full object-cover">
          </div>
          <div v-else class="h-40 flex items-center justify-center bg-gray-100">
            <div class="text-center p-4">
              <div class="text-3xl text-gray-400 mb-2">
                <span v-if="isDocument(evidence.file_type)">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </span>
                <span v-else>
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </span>
              </div>
              <div class="text-sm font-medium">{{ getFileTypeName(evidence.file_type) }}</div>
            </div>
          </div>
          
          <!-- Действия для редактирования -->
          <div v-if="editable" class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
            <button 
              @click="deleteEvidence(evidence.id)"
              class="p-1 bg-red-500 text-white rounded-full hover:bg-red-600" 
              title="Удалить"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
        
        <div class="p-4">
          <div class="font-medium">{{ evidence.title || 'Без названия' }}</div>
          <div class="text-sm text-gray-500 mb-2">
            Добавлено {{ formatDate(evidence.created_at) }}
          </div>
          <div v-if="evidence.description" class="text-sm text-gray-600 mb-3">
            {{ evidence.description }}
          </div>
          <div>
            <a 
              :href="evidence.file_url" 
              target="_blank" 
              class="text-blue-600 hover:text-blue-800 text-sm font-medium inline-flex items-center"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z" />
                <path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z" />
              </svg>
              Открыть файл
            </a>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-gray-500 mb-4 p-3 bg-gray-50 rounded-lg text-center">
      Нет доказательств
    </div>

    <!-- Форма добавления доказательства -->
    <div v-if="editable" class="border rounded-lg p-4 bg-gray-50">
      <h4 class="font-medium mb-3">Добавить доказательство</h4>
      <div class="grid gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Заголовок</label>
          <input 
            v-model="newEvidence.title" 
            type="text" 
            class="w-full p-2 border rounded"
            placeholder="Название файла"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Описание (опционально)</label>
          <textarea 
            v-model="newEvidence.description" 
            class="w-full p-2 border rounded"
            rows="2"
            placeholder="Дополнительная информация"
          ></textarea>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Файл</label>
          <input 
            type="file" 
            ref="fileInput"
            @change="handleFileChange"
            class="block w-full text-sm text-gray-500
                  file:mr-4 file:py-2 file:px-4
                  file:rounded file:border-0
                  file:text-sm file:font-medium
                  file:bg-blue-50 file:text-blue-700
                  hover:file:bg-blue-100"
          />
          <p class="mt-1 text-xs text-gray-500">Максимальный размер: 10MB</p>
        </div>
        <div>
          <button 
            @click="uploadEvidence" 
            class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            :disabled="!selectedFile || !newEvidence.title || uploading"
          >
            <span v-if="uploading">
              <span class="inline-block h-4 w-4 border-2 border-white rounded-full border-t-transparent animate-spin mr-2 align-middle"></span>
              Загрузка...
            </span>
            <span v-else>Загрузить файл</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import type { CaseEvidence } from '@/types/models';

const props = defineProps<{
  caseId: string;
  editable?: boolean;
}>();

const emit = defineEmits<{
  (e: 'evidence-added', evidence: CaseEvidence): void;
  (e: 'evidence-deleted', evidenceId: string): void;
}>();

const evidences = ref<CaseEvidence[]>([]);
const loading = ref(false);
const uploading = ref(false);
const error = ref<string | null>(null);
const fileInput = ref<HTMLInputElement | null>(null);
const selectedFile = ref<File | null>(null);

const newEvidence = ref({
  title: '',
  description: '',
  case_id: props.caseId
});

onMounted(async () => {
  await fetchEvidences();
});

async function fetchEvidences() {
  loading.value = true;
  error.value = null;
  
  try {
    // Здесь нужно заменить на реальный API-вызов
    // evidences.value = await api.fetchCaseEvidences(props.caseId);
    evidences.value = []; // Временно, пока не реализован API-запрос
  } catch (err) {
    error.value = 'Не удалось загрузить доказательства';
    console.error('Error fetching evidences:', err);
  } finally {
    loading.value = false;
  }
}

function handleFileChange(event: Event) {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    selectedFile.value = target.files[0];
    if (!newEvidence.value.title) {
      newEvidence.value.title = selectedFile.value.name;
    }
  } else {
    selectedFile.value = null;
  }
}

async function uploadEvidence() {
  if (!selectedFile.value || !newEvidence.value.title) return;
  
  uploading.value = true;
  error.value = null;
  
  try {
    // Здесь нужно заменить на реальный API-вызов для загрузки файла
    // const formData = new FormData();
    // formData.append('file', selectedFile.value);
    // formData.append('title', newEvidence.value.title);
    // formData.append('description', newEvidence.value.description || '');
    // formData.append('case_id', props.caseId);
    // const uploadedEvidence = await api.uploadCaseEvidence(formData);
    
    // Временный код, который симулирует загрузку файла
    const uploadedEvidence: CaseEvidence = {
      id: Math.random().toString(36).substring(2, 9),
      case_id: props.caseId,
      title: newEvidence.value.title,
      description: newEvidence.value.description || '',
      file_url: URL.createObjectURL(selectedFile.value),
      file_type: selectedFile.value.type,
      file_size: selectedFile.value.size,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };
    
    evidences.value.unshift(uploadedEvidence);
    emit('evidence-added', uploadedEvidence);
    
    // Сброс формы
    newEvidence.value.title = '';
    newEvidence.value.description = '';
    selectedFile.value = null;
    if (fileInput.value) {
      fileInput.value.value = '';
    }
  } catch (err) {
    error.value = 'Не удалось загрузить файл';
    console.error('Error uploading evidence:', err);
  } finally {
    uploading.value = false;
  }
}

function deleteEvidence(evidenceId: string) {
  if (!evidenceId) return;
  
  // Здесь должен быть реальный API-вызов для удаления
  // api.deleteCaseEvidence(evidenceId).then(() => {
  //   evidences.value = evidences.value.filter(e => e.id !== evidenceId);
  //   emit('evidence-deleted', evidenceId);
  // }).catch(err => {
  //   console.error('Error deleting evidence:', err);
  // });
  
  // Временный код
  evidences.value = evidences.value.filter(e => e.id !== evidenceId);
  emit('evidence-deleted', evidenceId);
}

function isImage(mimeType: string): boolean {
  return mimeType.startsWith('image/');
}

function isDocument(mimeType: string): boolean {
  return mimeType.includes('pdf') || 
         mimeType.includes('document') || 
         mimeType.includes('spreadsheet') || 
         mimeType.includes('presentation');
}

function getFileTypeName(mimeType: string): string {
  if (mimeType.includes('pdf')) return 'PDF';
  if (mimeType.includes('document')) return 'Документ';
  if (mimeType.includes('spreadsheet')) return 'Таблица';
  if (mimeType.includes('presentation')) return 'Презентация';
  if (mimeType.startsWith('image/')) return 'Изображение';
  if (mimeType.startsWith('video/')) return 'Видео';
  if (mimeType.startsWith('audio/')) return 'Аудио';
  return 'Файл';
}

function formatDate(dateString: string): string {
  if (!dateString) return '';
  
  const date = new Date(dateString);
  return date.toLocaleString('ru-RU', { 
    day: '2-digit', 
    month: '2-digit', 
    year: 'numeric'
  });
}
</script> 