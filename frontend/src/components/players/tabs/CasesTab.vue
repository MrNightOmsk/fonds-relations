<template>
  <div>
    <h2 class="text-lg font-medium mb-4">Дела игрока</h2>
    
    <div v-if="loading" class="text-center py-8">
      <div class="animate-spin h-8 w-8 border-4 border-blue-500 rounded-full border-t-transparent mx-auto"></div>
      <p class="mt-2 text-gray-600">Загрузка дел...</p>
    </div>
    
    <div v-else-if="cases && cases.length" class="space-y-4">
      <div 
        v-for="case_item in cases" 
        :key="case_item.id" 
        class="border rounded-lg p-4 hover:bg-gray-50"
      >
        <div class="flex justify-between items-start">
          <div>
            <div class="flex items-center">
              <span 
                class="px-2 py-1 rounded-full text-xs font-medium mr-2"
                :class="getStatusClass(case_item.status)"
              >
                {{ getStatusName(case_item.status) }}
              </span>
              <h3 class="font-medium">
                {{ case_item.title }}
              </h3>
            </div>
            <p class="text-sm text-gray-600 mt-1">
              Дело #{{ case_item.case_number }} - {{ formatDate(case_item.created_at) }}
            </p>
          </div>
          <router-link 
            :to="`/cases/${case_item.id}`" 
            class="text-blue-600 hover:text-blue-800"
          >
            Подробнее
          </router-link>
        </div>
        <div class="mt-2">
          <p class="text-gray-700">
            {{ case_item.description }}
          </p>
        </div>
      </div>
    </div>
    
    <div v-else class="text-center py-8 text-gray-500">
      У игрока нет дел
    </div>
  </div>
</template>

<script>
export default {
  name: 'CasesTab',
  props: {
    player: {
      type: Object,
      required: true
    },
    cases: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
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
    },
    getStatusName(status) {
      const statuses = {
        'open': 'Открыто',
        'in_progress': 'В работе',
        'resolved': 'Разрешено',
        'closed': 'Закрыто'
      };
      return statuses[status] || status;
    },
    getStatusClass(status) {
      const classes = {
        'open': 'bg-yellow-100 text-yellow-800',
        'in_progress': 'bg-blue-100 text-blue-800',
        'resolved': 'bg-green-100 text-green-800',
        'closed': 'bg-gray-100 text-gray-800'
      };
      return classes[status] || 'bg-gray-100 text-gray-800';
    }
  }
}
</script> 