<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-8 text-text-light dark:text-text-dark">UI Компоненты</h1>
    
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Кнопки -->
      <Card title="Кнопки">
        <div class="space-y-4">
          <div class="flex flex-wrap gap-2">
            <Button variant="primary">Основная</Button>
            <Button variant="secondary">Вторичная</Button>
            <Button variant="success">Успех</Button>
            <Button variant="warning">Предупреждение</Button>
            <Button variant="danger">Опасность</Button>
          </div>
          
          <div class="flex flex-wrap gap-2">
            <Button variant="outline">Контурная</Button>
            <Button variant="ghost">Призрак</Button>
            <Button variant="link">Ссылка</Button>
          </div>
          
          <div class="flex flex-wrap gap-2">
            <Button size="sm">Маленькая</Button>
            <Button>Средняя</Button>
            <Button size="lg">Большая</Button>
          </div>
          
          <div class="flex flex-wrap gap-2">
            <Button loading>Загрузка</Button>
            <Button disabled>Отключена</Button>
          </div>
        </div>
      </Card>
      
      <!-- Значки -->
      <Card title="Значки">
        <div class="space-y-4">
          <div class="flex flex-wrap gap-2">
            <Badge variant="primary">Основной</Badge>
            <Badge variant="secondary">Вторичный</Badge>
            <Badge variant="success">Успех</Badge>
            <Badge variant="warning">Предупреждение</Badge>
            <Badge variant="danger">Опасность</Badge>
            <Badge variant="info">Информация</Badge>
          </div>
          
          <div class="flex flex-wrap gap-2">
            <Badge variant="primary" outline>Основной</Badge>
            <Badge variant="secondary" outline>Вторичный</Badge>
            <Badge variant="success" outline>Успех</Badge>
            <Badge variant="warning" outline>Предупреждение</Badge>
            <Badge variant="danger" outline>Опасность</Badge>
          </div>
          
          <div class="flex flex-wrap gap-2">
            <Badge size="sm">Маленький</Badge>
            <Badge>Средний</Badge>
            <Badge size="lg">Большой</Badge>
          </div>
        </div>
      </Card>
      
      <!-- Аватары -->
      <Card title="Аватары">
        <div class="space-y-4">
          <div class="flex flex-wrap gap-2 items-end">
            <Avatar text="Иван Иванов" size="xs" />
            <Avatar text="Анна Смирнова" size="sm" />
            <Avatar text="Петр Петров" />
            <Avatar text="Елена Иванова" size="lg" />
            <Avatar text="Сергей Сидоров" size="xl" />
          </div>
          
          <div class="flex flex-wrap gap-2">
            <Avatar text="Квадрат" shape="square" />
            <Avatar text="Округлен" shape="rounded" />
            <Avatar text="Круг" shape="circle" />
          </div>
          
          <div class="flex flex-wrap gap-2">
            <Avatar src="https://i.pravatar.cc/150?img=1" />
            <Avatar src="https://i.pravatar.cc/150?img=2" />
            <Avatar src="https://i.pravatar.cc/150?img=3" />
            <Avatar src="error-url" text="Запасной" />
          </div>
        </div>
      </Card>
      
      <!-- Формы -->
      <Card title="Элементы форм">
        <div class="space-y-4">
          <Input 
            v-model="formData.name" 
            label="Имя" 
            placeholder="Введите ваше имя" 
          />
          
          <Input 
            v-model="formData.email" 
            label="Email" 
            type="email" 
            placeholder="user@example.com" 
            required 
            :error="errors.email"
            error-message="Введите корректный email"
          />
          
          <Select 
            v-model="formData.role" 
            label="Роль" 
            :options="[
              { value: 'user', label: 'Пользователь' },
              { value: 'admin', label: 'Администратор' },
              { value: 'moderator', label: 'Модератор' }
            ]"
          />
          
          <div class="flex justify-end">
            <Button @click="resetForm">Отмена</Button>
            <Button variant="primary" class="ml-2" @click="submitForm">Отправить</Button>
          </div>
        </div>
      </Card>
      
      <!-- Уведомления -->
      <Card title="Уведомления">
        <div class="space-y-4">
          <Alert variant="info" title="Информация">
            Это информационное сообщение.
          </Alert>
          
          <Alert variant="success" title="Успех">
            Операция выполнена успешно.
          </Alert>
          
          <Alert variant="warning" title="Предупреждение" dismissible>
            Это сообщение можно закрыть.
          </Alert>
          
          <Alert variant="danger" title="Ошибка">
            Произошла ошибка при выполнении операции.
          </Alert>
        </div>
      </Card>
      
      <!-- Состояние загрузки -->
      <Card title="Состояние загрузки">
        <div class="space-y-4">
          <div>
            <Skeleton width="60%" height="24px" class="mb-2" />
            <Skeleton width="100%" height="16px" class="mb-1" />
            <Skeleton width="90%" height="16px" class="mb-1" />
            <Skeleton width="85%" height="16px" class="mb-3" />
            
            <div class="flex items-center gap-2">
              <Skeleton width="32px" height="32px" radius="full" />
              <div class="flex-1">
                <Skeleton width="40%" height="14px" class="mb-1" />
                <Skeleton width="30%" height="12px" />
              </div>
            </div>
          </div>
        </div>
      </Card>
      
      <!-- Модальное окно -->
      <Card title="Модальное окно">
        <div class="space-y-4">
          <Button variant="primary" @click="showModal = true">Открыть модальное окно</Button>
          
          <Modal :is-open="showModal" title="Пример модального окна" @close="showModal = false">
            <p class="text-text-light dark:text-text-dark">
              Это пример модального окна с кнопками в футере.
            </p>
            
            <template #footer>
              <Button variant="outline" @click="showModal = false">Отмена</Button>
              <Button variant="primary" @click="confirmModal">Подтвердить</Button>
            </template>
          </Modal>
        </div>
      </Card>
      
      <!-- Боковая панель -->
      <Card title="Боковая панель">
        <div class="space-y-4">
          <div class="flex flex-wrap gap-2">
            <Button variant="secondary" @click="openDrawer('left')">Слева</Button>
            <Button variant="secondary" @click="openDrawer('right')">Справа</Button>
            <Button variant="secondary" @click="openDrawer('top')">Сверху</Button>
            <Button variant="secondary" @click="openDrawer('bottom')">Снизу</Button>
          </div>
          
          <Drawer 
            :is-open="drawerOpen" 
            :position="drawerPosition" 
            title="Боковая панель" 
            @update:is-open="drawerOpen = $event"
          >
            <div class="p-4">
              <p class="text-text-light dark:text-text-dark mb-4">
                Это пример боковой панели. Она может открываться с разных сторон.
              </p>
              
              <Button variant="primary" @click="drawerOpen = false">Закрыть</Button>
            </div>
          </Drawer>
        </div>
      </Card>
      
      <!-- Вкладки -->
      <Card title="Вкладки">
        <div class="space-y-4">
          <Tabs 
            :tabs="[
              { id: 'tab1', title: 'Первая вкладка' },
              { id: 'tab2', title: 'Вторая вкладка' },
              { id: 'tab3', title: 'Третья вкладка' }
            ]"
            default-tab="tab1"
            @change="activeTab = $event"
          >
            <template #tab1>
              <p class="py-2 text-text-light dark:text-text-dark">
                Содержимое первой вкладки. Активная вкладка: <Badge>{{ activeTab }}</Badge>
              </p>
            </template>
            
            <template #tab2>
              <p class="py-2 text-text-light dark:text-text-dark">
                Содержимое второй вкладки. Активная вкладка: <Badge>{{ activeTab }}</Badge>
              </p>
            </template>
            
            <template #tab3>
              <p class="py-2 text-text-light dark:text-text-dark">
                Содержимое третьей вкладки. Активная вкладка: <Badge>{{ activeTab }}</Badge>
              </p>
            </template>
          </Tabs>
        </div>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { 
  Card, 
  Button, 
  Badge, 
  Avatar, 
  Input, 
  Select, 
  Alert, 
  Skeleton, 
  Modal, 
  Drawer, 
  Tabs 
} from '@/components/ui';

// Состояние формы
const formData = reactive({
  name: '',
  email: '',
  role: 'user'
});

// Ошибки формы
const errors = reactive({
  email: false
});

// Сброс формы
const resetForm = () => {
  formData.name = '';
  formData.email = '';
  formData.role = 'user';
  errors.email = false;
};

// Отправка формы
const submitForm = () => {
  errors.email = !formData.email.includes('@');
  
  if (!errors.email) {
    alert('Форма успешно отправлена!');
    resetForm();
  }
};

// Модальное окно
const showModal = ref(false);

const confirmModal = () => {
  showModal.value = false;
  alert('Действие подтверждено!');
};

// Боковая панель
const drawerOpen = ref(false);
const drawerPosition = ref('right');

const openDrawer = (position: string) => {
  drawerPosition.value = position;
  drawerOpen.value = true;
};

// Вкладки
const activeTab = ref('tab1');
</script> 