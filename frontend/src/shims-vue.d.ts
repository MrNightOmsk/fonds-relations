/* eslint-disable */
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

// Определения для Vue
declare module 'vue' {
  export function ref<T>(value: T): { value: T }
  export function reactive<T extends object>(target: T): T
  export function computed<T>(getter: () => T): { readonly value: T }
  export function watch(source: any, callback: Function, options?: object): any
  export function onMounted(fn: () => void): void
  export function onUnmounted(fn: () => void): void
  export function defineProps<T>(props: T): T
  export function defineEmits<T extends string[]>(emits: T): { (event: T[number], ...args: any[]): void }
}

// Определения для Vue Router
declare module 'vue-router' {
  export interface Router {
    push(location: string | { path?: string, query?: Record<string, string>, params?: Record<string, string> }): Promise<void>
    replace(location: string | { path?: string, query?: Record<string, string>, params?: Record<string, string> }): Promise<void>
    go(n: number): void
    back(): void
    forward(): void
  }

  export function useRouter(): Router
  export function useRoute(): any
} 