// Экспортируем все компоненты UI библиотеки FondsRelations
// 
// ВАЖНО: При использовании компонентов с withDefaults(defineProps<Props>(), {})
// могут возникать ошибки линтера "Expected 1 arguments, but got 0".
// Для решения проблемы см. README.md в этой директории.

// Контейнеры
export { default as Card } from './Card.vue';
export { default as Modal } from './Modal.vue';
export { default as Drawer } from './Drawer.vue';

// Элементы ввода
export { default as Button } from './Button.vue';
export { default as Input } from './Input.vue';
export { default as Select } from './Select.vue';

// Навигация и структура
export { default as Tabs } from './Tabs.vue';
export { default as Badge } from './Badge.vue';
export { default as Avatar } from './Avatar.vue';

// Обратная связь
export { default as Alert } from './Alert.vue';
export { default as Tooltip } from './Tooltip.vue';
export { default as Skeleton } from './Skeleton.vue';

// Типы
export type { Tab } from './Tabs.vue'; 