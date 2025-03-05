# Конфигурация сетевого взаимодействия

Документ содержит описание проблем, с которыми мы столкнулись при настройке взаимодействия между фронтендом и бэкендом, и их решения.

## Проблемы и решения

### 1. Проблема потери порта при редиректах

**Проблема:**  
При попытке отправить запрос на URL без слеша на конце (например, `/api/v1/login/access-token`), Nginx выполнял редирект на URL со слешем на конце (`/api/v1/login/access-token/`), но при этом терялся порт из URL. Запрос, отправленный на `http://localhost:3000/api/v1/login/access-token`, перенаправлялся на `http://localhost/api/v1/login/access-token/`, и сервер, работающий на порту 3000, становился недоступен.

**Решение:**  
1. В конфигурации Nginx добавлены директивы:
   ```nginx
   absolute_redirect off;
   port_in_redirect on;
   server_name_in_redirect on;
   merge_slashes off;
   ```

2. Созданы отдельные блоки `location` для обработки запросов авторизации как со слешем, так и без слеша на конце:
   ```nginx
   # Специальная обработка для запросов авторизации БЕЗ слеша на конце
   location = /api/v1/login/access-token {
       # ... конфигурация ...
       proxy_pass http://backend:8000/api/v1/login/access-token;
   }
   
   # Специальная обработка для запросов авторизации СО слешем на конце
   location = /api/v1/login/access-token/ {
       # ... конфигурация ...
       proxy_pass http://backend:8000/api/v1/login/access-token/;
   }
   ```

3. Для других API URL также добавлена обработка запросов без слеша на конце:
   ```nginx
   # Обработка других URL без слеша в конце - без редиректа
   location ~ ^/api/v1/(players|funds|cases|users)$ {
       rewrite ^(/api/v1/(?:players|funds|cases|users))$ $1/ break;
       proxy_pass http://backend:8000;
       # ... остальные настройки ...
   }
   ```

### 2. Проблема с автоматическими редиректами в axios

**Проблема:**  
Библиотека axios автоматически следовала за редиректами, что приводило к потере порта в URL.

**Решение:**  
В клиентском коде (auth.ts) отключено автоматическое следование за редиректами:
```javascript
const response = await axios.post<LoginResponse>(
  url,
  formData,
  {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    // Отключаем автоматическое следование за редиректами
    maxRedirects: 0
  }
);
```

Дополнительно добавлена логика обработки ошибок 307 (Temporary Redirect), которая автоматически отправляет запрос на URL со слешем в случае получения редиректа.

### 3. Ограничение Nginx: "proxy_pass cannot have URI part in location given by regular expression"

**Проблема:**  
Nginx не позволяет использовать URI-часть в директиве `proxy_pass` внутри блока `location`, определенного регулярным выражением.

**Решение:**  
Замена регулярных выражений на точные пути или использование директивы `rewrite` перед `proxy_pass`:
```nginx
# Было (ошибка):
location ~ ^/api/v1/login/access-token/?$ {
    proxy_pass http://backend:8000/api/v1/login/access-token/;
}

# Стало (работает):
location = /api/v1/login/access-token {
    proxy_pass http://backend:8000/api/v1/login/access-token;
}
```

или с использованием rewrite:
```nginx
location ~ ^/api/v1/(players|funds|cases|users)$ {
    rewrite ^(/api/v1/(?:players|funds|cases|users))$ $1/ break;
    proxy_pass http://backend:8000;
}
```

## Бэкап конфигураций

### Конфигурация Nginx (frontend/nginx.conf)

```nginx
server {
    listen 80;
    server_name _;
    
    # Отключаем абсолютные редиректы (сохраняем порт)
    absolute_redirect off;
    
    # Включаем порт в редиректах
    port_in_redirect on;
    
    # Используем имя сервера в редиректах
    server_name_in_redirect on;
    
    # Отключаем слияние слешей для нормализации URL
    merge_slashes off;
    
    # Корневая директория для статических файлов
    root /usr/share/nginx/html;
    index index.html;

    # Включение отладочных логов
    error_log /var/log/nginx/error.log debug;
    
    # Конфигурация для SPA (Single Page Application)
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Обработка API запросов
    
    # Специальная обработка для запросов авторизации БЕЗ слеша на конце
    location = /api/v1/login/access-token {
        # Разрешаем только POST и OPTIONS запросы
        limit_except POST OPTIONS {
            deny all;
        }
        
        # Обработка CORS для preflight запросов
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' '*';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
            add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization';
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Content-Type' 'text/plain; charset=utf-8';
            add_header 'Content-Length' 0;
            return 204;
        }
        
        # Прямое проксирование на бэкенд без редиректа
        proxy_pass http://backend:8000/api/v1/login/access-token;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $http_host;
        proxy_set_header X-Forwarded-Port $server_port;
        proxy_redirect off;
        proxy_buffering off;
    }
    
    # Специальная обработка для запросов авторизации СО слешем на конце
    location = /api/v1/login/access-token/ {
        # Разрешаем только POST и OPTIONS запросы
        limit_except POST OPTIONS {
            deny all;
        }
        
        # Обработка CORS для preflight запросов
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' '*';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
            add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization';
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Content-Type' 'text/plain; charset=utf-8';
            add_header 'Content-Length' 0;
            return 204;
        }
        
        # Прямое проксирование на бэкенд со слешем
        proxy_pass http://backend:8000/api/v1/login/access-token/;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $http_host;
        proxy_set_header X-Forwarded-Port $server_port;
        proxy_redirect off;
        proxy_buffering off;
    }

    # Обработка других URL без слеша в конце - без редиректа
    location ~ ^/api/v1/(players|funds|cases|users)$ {
        # Изменяем URL для проксирования, добавляя слеш
        rewrite ^(/api/v1/(?:players|funds|cases|users))$ $1/ break;
        proxy_pass http://backend:8000;
        proxy_set_header Host $host:$server_port;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host:$server_port;
        proxy_set_header X-Forwarded-Port $server_port;
        proxy_set_header Origin $http_origin;
        proxy_redirect off;
        proxy_buffering off;
    }

    # Общая обработка API запросов
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $http_host;
        proxy_set_header X-Forwarded-Port $server_port;
        proxy_redirect off;
        proxy_buffering off;
    }

    # Настройка кэширования для статических файлов
    location ~* \.(js|css|png|jpg|jpeg|gif|ico)$ {
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    # Отключаем логирование запросов к файлам favicon и robots.txt
    location = /favicon.ico { access_log off; log_not_found off; }
    location = /robots.txt  { access_log off; log_not_found off; }
    
    # Обработка ошибок
    error_page 404 /index.html;
    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}
```

### Код авторизации (frontend/src/api/auth.ts)

```typescript
import axios from 'axios';
import apiClient from './config';

// Используем относительный путь для API запросов
const API_URL = '/api/v1';

interface LoginCredentials {
  username: string;
  password: string;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
}

/**
 * Выполняет запрос на аутентификацию пользователя
 * @param credentials Учетные данные пользователя
 * @returns Ответ с токеном доступа
 */
export const login = async (credentials: LoginCredentials): Promise<LoginResponse> => {
  const formData = new URLSearchParams();
  formData.append('username', credentials.username);
  formData.append('password', credentials.password);

  // Добавим более подробное логирование
  console.log('Window location:', window.location);
  console.log('Window location origin:', window.location.origin);
  console.log('API_URL:', API_URL);
  
  // Намеренно убираем слеш в конце URL, так как мы настроили nginx на обработку URL без слеша
  const url = `${API_URL}/login/access-token`;
  console.log('URL для авторизации (без слеша):', url);
  
  try {
    console.log(`Отправка запроса авторизации на ${url}`);
    
    // Используем относительный URL и отключаем редиректы
    const response = await axios.post<LoginResponse>(
      url,
      formData,
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        // Отключаем автоматическое следование за редиректами
        maxRedirects: 0
      }
    );
    console.log('Успешный ответ от сервера:', response);
    return response.data;
  } catch (error) {
    console.error('Ошибка при авторизации:', error);
    
    // Проверяем, если ошибка связана с редиректом (код 307)
    const axiosError = error as any;
    if (axiosError.response && axiosError.response.status === 307) {
      console.log('Получен редирект 307, пробуем отправить запрос на URL со слешем');
      // Пробуем отправить запрос на URL со слешем
      try {
        const urlWithSlash = `${API_URL}/login/access-token/`;
        console.log(`Повторная отправка запроса на ${urlWithSlash}`);
        const response = await axios.post<LoginResponse>(
          urlWithSlash,
          formData,
          {
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded'
            },
            maxRedirects: 0
          }
        );
        console.log('Успешный ответ от сервера после повторной попытки:', response);
        return response.data;
      } catch (retryError) {
        console.error('Ошибка при повторной попытке:', retryError);
        throw retryError;
      }
    }
    
    throw error;
  }
};

/**
 * Получает информацию о текущем пользователе
 * @returns Информация о пользователе
 */
export const getCurrentUser = async () => {
  const response = await apiClient.get(`/users/me`);
  return response.data;
};
```

## Рекомендации для разработчиков

1. **Всегда внимательно проверяйте редиректы.** Если вы видите, что URL изменился после отправки запроса, это может быть причиной проблем, особенно если изменились протокол, хост или порт.

2. **Используйте инструменты разработчика браузера.** Вкладка Network/Сеть в Developer Tools позволяет отслеживать все запросы и ответы, включая редиректы и заголовки.

3. **Добавляйте логирование в клиентский код.** Логирование помогает определить, какие именно URL используются для запросов и что происходит при обработке ответов.

4. **Будьте осторожны с конфигурацией Nginx.** Обратите внимание на ограничения Nginx, особенно связанные с использованием URI-части в директиве `proxy_pass` внутри блока `location`, определенного регулярным выражением.

5. **Контролируйте поведение клиентских библиотек.** Axios и другие HTTP-клиенты могут автоматически следовать за редиректами, что может привести к непредвиденным результатам. 