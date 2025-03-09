<template>
  <div>
    <div class="mb-4">
      <h3 class="font-semibold mb-2">Адрес</h3>
      <div class="grid grid-cols-1 gap-4">
        <p>
          {{ player && player.locations && player.locations.length > 0 
             ? formatAddress(player.locations[0])
             : 'Адрес не указан' }}
        </p>
      </div>
    </div>

    <div class="mb-4">
      <h3 class="font-semibold mb-2">Контакты</h3>
      <div v-if="player && player.contacts && player.contacts.length > 0">
        <div v-for="(contact, index) in player.contacts" :key="index" class="mb-2">
          <strong>{{ formatContactType(contact.type) }}:</strong> {{ contact.value }}
          <span v-if="contact.description" class="text-sm text-gray-500 ml-2">({{ contact.description }})</span>
        </div>
      </div>
      <div v-else class="text-gray-500">
        Контакты не указаны
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'InformationTab',
  props: {
    player: {
      type: Object,
      required: true
    }
  },
  methods: {
    formatAddress(location) {
      if (!location) return '';
      
      const parts = [];
      if (location.country) parts.push(location.country);
      if (location.city) parts.push(location.city);
      if (location.address) parts.push(location.address);
      
      return parts.join(', ') || 'Адрес не указан';
    },
    
    formatContactType(type) {
      const types = {
        'email': 'Email',
        'phone': 'Телефон',
        'skype': 'Skype',
        'telegram': 'Telegram',
        'whatsapp': 'WhatsApp',
        'viber': 'Viber',
        'discord': 'Discord'
      };
      
      return types[type] || type;
    }
  }
}
</script> 