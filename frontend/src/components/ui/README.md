# UI Компоненты

Библиотека компонентов пользовательского интерфейса для проекта "Fonds Relations".

## Содержание

- [Установка и использование](#установка-и-использование)
- [Решение проблем](#решение-проблем)
- [Компоненты](#компоненты)

## Установка и использование

Компоненты доступны через импорт из директории `@/components/ui`:

```vue
<script setup lang="ts">
import { Card, Button, Modal } from '@/components/ui';
</script>
```

## Решение проблем

### Ошибки TypeScript

В некоторых компонентах могут возникать ошибки TypeScript, связанные с типами props. Наиболее распространенные ошибки:

1. **Expected 1 arguments, but got 0**

   Эта ошибка возникает при использовании `withDefaults(defineProps<Props>(), {})`. TypeScript не может правильно вывести типы.

   **Решение:**
   
   Заменить на прямое использование `defineProps` с типизацией:

   ```typescript
   // Вместо этого:
   interface Props {
     size?: string;
   }
   
   const props = withDefaults(defineProps<Props>(), {
     size: 'md'
   });
   
   // Используйте это:
   const props = defineProps({
     size: {
       type: String, 
       default: 'md'
     }
   });
   ```

2. **Type 'string' is not comparable to type...**

   Эта ошибка возникает при сравнении значений props в switch/case или условиях.

   **Решение:**
   
   Использовать computed свойства для работы с props:

   ```typescript
   // Вместо прямого доступа к props в условиях:
   const result = props.variant === 'primary' ? 'foo' : 'bar';
   
   // Используйте промежуточное значение:
   const variant = props.variant as string;
   const result = variant === 'primary' ? 'foo' : 'bar';
   
   // Или еще лучше - используйте computed:
   const result = computed(() => {
     const variant = props.variant as string;
     return variant === 'primary' ? 'foo' : 'bar';
   });
   ```

3. **Cannot be used as an index type**

   Ошибка при использовании props в качестве индекса объекта.

   **Решение:**
   
   ```typescript
   // Вместо этого:
   const classes = {
     primary: 'bg-primary',
     secondary: 'bg-secondary'
   }[props.variant];
   
   // Используйте:
   const variant = props.variant as string;
   const classes = {
     primary: 'bg-primary',
     secondary: 'bg-secondary'
   }[variant];
   ```

## Компоненты

### Контейнеры
- **Card** - карточка с тенью и закругленными углами
- **Modal** - модальное окно
- **Drawer** - выдвижная панель

### Элементы ввода
- **Button** - кнопка
- **Input** - поле ввода
- **Select** - выпадающий список

### Навигация и структура
- **Tabs** - вкладки
- **Badge** - значок/метка
- **Avatar** - аватар пользователя

### Обратная связь
- **Alert** - уведомление
- **Tooltip** - всплывающая подсказка
- **Skeleton** - заполнитель при загрузке

## Примеры использования

### Card

```vue
<Card title="Заголовок карточки" padding="md" hover clickable>
  Содержимое карточки
</Card>
```

### Button

```vue
<Button variant="primary" size="md" :loading="isLoading" @click="handleClick">
  Нажать
</Button>
```

### Modal

```vue
<Modal :is-open="showModal" title="Заголовок" @close="closeModal">
  <p>Содержимое модального окна</p>
  
  <template #footer>
    <Button variant="outline" @click="closeModal">Отмена</Button>
    <Button variant="primary" @click="saveAndClose">Сохранить</Button>
  </template>
</Modal>
``` 