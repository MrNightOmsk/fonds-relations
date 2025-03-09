# План реализации дашборда для менеджеров

## 1. Анализ текущего состояния

**Текущая ситуация:**
- Имеется базовый дашборд с общей информацией
- Навигация в админ-панели позволяет переходить между разными секциями
- Существуют компоненты для управления игроками и кейсами
- Elasticsearch упоминается в проекте, но не интегрирован

**Требования:**
- Менеджеры должны иметь доступ на чтение ко всем кейсам и игрокам
- Разрешено управление только кейсами/игроками своего фонда
- Универсальная строка поиска с Elasticsearch
- Возможность создания новых кейсов
- Интуитивная навигация для просмотра деталей кейсов и игроков

## 2. План технической реализации

### Этап 1: Создание унифицированного интерфейса поиска

1. **Создание компонента универсального поиска**:
   ```vue
   <!-- Компонент UnifiedSearch.vue -->
   <template>
     <div class="search-container">
       <div class="relative w-full">
         <input 
           type="text" 
           v-model="searchQuery" 
           @input="search" 
           placeholder="Поиск игроков, кейсов..." 
           class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
         />
         <button v-if="searchQuery" @click="clearSearch" class="absolute right-3 top-2.5 text-gray-400 hover:text-gray-600">
           <span>✕</span>
         </button>
       </div>
       
       <div v-if="results.length > 0" class="results-container mt-2 shadow-lg rounded-lg border overflow-hidden">
         <div v-if="players.length > 0" class="section">
           <h3 class="bg-gray-100 px-3 py-1 font-medium text-sm">Игроки</h3>
           <div v-for="player in players" :key="player.id" 
                @click="selectResult('player', player)" 
                class="result-item p-2 hover:bg-blue-50 cursor-pointer">
             <div class="font-medium">{{ player.full_name }}</div>
             <div class="text-xs text-gray-500" v-if="player.details">{{ player.details }}</div>
           </div>
         </div>
         
         <div v-if="cases.length > 0" class="section">
           <h3 class="bg-gray-100 px-3 py-1 font-medium text-sm">Кейсы</h3>
           <div v-for="case_item in cases" :key="case_item.id" 
                @click="selectResult('case', case_item)" 
                class="result-item p-2 hover:bg-blue-50 cursor-pointer">
             <div class="font-medium">{{ case_item.title }}</div>
             <div class="text-xs text-gray-500">{{ getCaseDetails(case_item) }}</div>
           </div>
         </div>
       </div>
     </div>
   </template>
   ```

2. **Реализация API для поиска на бэкенде**:
   - Создание эндпоинта для универсального поиска
   - Интеграция с Elasticsearch
   - Поддержка поиска по игрокам и кейсам одновременно

### Этап 2: Улучшение дашборда менеджера

1. **Редизайн страницы дашборда**:
   ```vue
   <template>
     <div class="dashboard">
       <!-- Секция поиска -->
       <div class="search-section mb-6">
         <h2 class="text-lg font-medium mb-2">Поиск</h2>
         <UnifiedSearch @select="handleSearchResultSelect" />
       </div>
       
       <!-- Секция быстрых действий -->
       <div class="quick-actions mb-6">
         <h2 class="text-lg font-medium mb-2">Быстрые действия</h2>
         <div class="grid grid-cols-2 gap-3">
           <button @click="showCreateCaseModal = true" class="action-btn bg-blue-600 text-white">
             <span class="icon">+</span>
             <span>Создать кейс</span>
           </button>
           <button @click="navigateTo('/my-cases')" class="action-btn bg-green-600 text-white">
             <span class="icon">📁</span>
             <span>Мои кейсы</span>
           </button>
           <button @click="navigateTo('/players-list')" class="action-btn bg-purple-600 text-white">
             <span class="icon">👤</span>
             <span>Игроки</span>
           </button>
           <button @click="navigateTo('/recent-activity')" class="action-btn bg-orange-600 text-white">
             <span class="icon">🔔</span>
             <span>Активность</span>
           </button>
         </div>
       </div>
       
       <!-- Секция последних кейсов -->
       <div class="recent-cases mb-6">
         <div class="flex justify-between items-center mb-2">
           <h2 class="text-lg font-medium">Последние кейсы</h2>
           <button @click="navigateTo('/all-cases')" class="text-blue-600 text-sm">Все кейсы</button>
         </div>
         <div class="bg-white rounded-lg shadow overflow-hidden">
           <RecentCases :limit="5" />
         </div>
       </div>
       
       <!-- Модальное окно создания кейса -->
       <CreateCaseModal v-if="showCreateCaseModal" @close="showCreateCaseModal = false" />
     </div>
   </template>
   ```

2. **Добавление компонентов статистики и последних активностей**:
   - Реализация компонента RecentCases для отображения последних кейсов
   - Добавление списка последних активностей пользователя
   - Информационная панель с ключевыми метриками

### Этап 3: Настройка прав доступа и изоляции данных

1. **Реализация модуля разграничения прав**:
   - Настройка middleware для проверки прав при доступе к API
   - Фильтрация данных по принадлежности к фонду пользователя

2. **Обновление API для поддержки разных ролей**:
   - Доработка существующих API для проверки разрешений
   - Для менеджеров: чтение всех данных, изменение только своего фонда

### Этап 4: Интеграция Elasticsearch

1. **Настройка индексирования данных**:
   - Создание индексов для игроков и кейсов
   - Настройка автоматической индексации при изменении данных

2. **Реализация поисковых запросов**:
   ```python
   @router.get("/search/unified", response_model=UnifiedSearchResult)
   async def unified_search(
       query: str,
       db: Session = Depends(deps.get_db),
       es: AsyncElasticsearch = Depends(deps.get_elasticsearch),
       current_user: models.User = Depends(deps.get_current_active_user),
   ) -> Any:
       """
       Унифицированный поиск по игрокам и кейсам
       """
       search_results = UnifiedSearchResult(players=[], cases=[])
       
       # Поиск в Elasticsearch
       try:
           # Поиск по игрокам
           players_query = {
               "multi_match": {
                   "query": query,
                   "fields": ["full_name^3", "first_name", "last_name", "nicknames.nickname"],
                   "fuzziness": "AUTO"
               }
           }
           players_result = await es.search(index="players", query=players_query, size=5)
           
           # Поиск по кейсам
           cases_query = {
               "multi_match": {
                   "query": query,
                   "fields": ["title^3", "description", "player.full_name"],
                   "fuzziness": "AUTO"
               }
           }
           cases_result = await es.search(index="cases", query=cases_query, size=5)
           
           # Обработка результатов
           # ... код обработки результатов ...
           
       except Exception as e:
           # Поиск в базе данных, если Elasticsearch недоступен
           logger.warning(f"Elasticsearch search failed, falling back to database search: {str(e)}")
           
           # ... код поиска в БД ...
           
       return search_results
   ```

## 3. Рекомендации по UI/UX

1. **Основные принципы навигации**:
   - Основная страница (дашборд) должна содержать все ключевые точки входа
   - Меню быстрого доступа в верхней части страницы с поиском
   - Боковая навигация для переключения между секциями

2. **Компоненты интерфейса**:
   - Единая строка поиска всегда видима в хедере
   - Результаты поиска показываются в выпадающем меню с категориями
   - Карточки для быстрого доступа к основным функциям
   - Модальные окна для создания новых сущностей

3. **Представление данных**:
   - Таблицы с возможностью сортировки и фильтрации
   - Карточки для компактного представления данных
   - Индикаторы статуса с цветовой кодировкой

## 4. Этапы внедрения

1. **Первый этап (MVP)**:
   - Базовая интеграция Elasticsearch
   - Универсальная строка поиска
   - Обновленный дашборд с быстрыми действиями
   - Разграничение прав доступа

2. **Второй этап (расширение)**:
   - Улучшенный поиск с фильтрами и подсказками
   - Расширенная статистика на дашборде
   - Оповещения и уведомления
   - Оптимизация производительности

3. **Третий этап (завершение)**:
   - Персонализация интерфейса для пользователей
   - Экспорт данных в различные форматы
   - Аналитические отчеты
   - Мобильная оптимизация

## Резюме

Предложенный план позволит создать эффективный интерфейс для менеджеров, сосредоточенный вокруг универсального поиска с использованием Elasticsearch. Ключевые моменты:

- Интуитивная навигация с фокусом на поиск
- Четкое разграничение прав доступа
- Простой доступ к просмотру и созданию кейсов и игроков
- Быстрый доступ к наиболее важной информации на дашборде

Предложенная структура обеспечит менеджерам удобный рабочий процесс, соответствующий всем указанным требованиям. 