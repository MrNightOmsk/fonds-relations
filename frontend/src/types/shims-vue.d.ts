/* Объявления типов для Vue файлов */
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

/* Объявления для vite/client */
declare module 'vite/client' {
  interface ImportMetaEnv {
    VITE_API_URL: string
    // добавьте здесь любые другие переменные окружения
  }
}

/* Имитация node типов, которые могут понадобиться */
declare namespace NodeJS {
  interface Process {
    env: ProcessEnv
  }
  interface ProcessEnv {
    NODE_ENV: string
    // добавьте здесь любые другие переменные окружения
  }
} 