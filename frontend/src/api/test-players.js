/**
 * Тестовый скрипт для проверки обработки никнеймов на фронтенде
 * Запускается в консоли браузера
 */

(function() {
  // Функция для вывода результатов в консоль
  const logResult = (title, result, isError = false) => {
    console.group(`%c ${title}`, `color: ${isError ? 'red' : 'blue'}; font-weight: bold;`);
    console.log(result);
    console.groupEnd();
  };

  // Проверка наличия никнеймов в модели игрока
  const checkPlayerModel = async (playerId) => {
    try {
      const player = await window.$nuxt.$store.dispatch('player/fetchPlayer', playerId);
      
      logResult('Данные игрока из хранилища:', player);
      
      if (player && player.nicknames) {
        logResult(`Никнеймы (${player.nicknames.length} шт.):`, player.nicknames);
      } else {
        logResult('Никнеймы отсутствуют в данных игрока', null, true);
      }
      
      return player;
    } catch (error) {
      logResult('Ошибка при загрузке данных игрока', error, true);
      return null;
    }
  };

  // Проверка прямого API запроса
  const checkDirectApiCall = async (playerId) => {
    try {
      const api = window.$nuxt.$api || window.$nuxt.context.$api;
      if (!api) {
        logResult('API клиент не найден', null, true);
        return null;
      }
      
      const baseUrl = '/api/v1/players';
      const response = await fetch(`${baseUrl}/${playerId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Accept': 'application/json'
        }
      });
      
      if (!response.ok) {
        throw new Error(`Ошибка API: ${response.status}`);
      }
      
      const data = await response.json();
      logResult('Данные игрока напрямую из API:', data);
      
      if (data && data.nicknames) {
        logResult(`Никнеймы из прямого запроса API (${data.nicknames.length} шт.):`, data.nicknames);
      } else {
        logResult('Никнеймы отсутствуют в прямом ответе API', null, true);
      }
      
      return data;
    } catch (error) {
      logResult('Ошибка при прямом запросе к API', error, true);
      return null;
    }
  };

  // Проверка компонента отображения
  const checkRenderingComponent = (playerId) => {
    try {
      // Пытаемся найти компонент детального просмотра игрока
      const playerDetailComponent = Array.from(
        document.querySelectorAll('*')
      ).find(el => el.__vue__ && el.__vue__.$options && el.__vue__.$options.name === 'PlayerDetail');
      
      if (!playerDetailComponent) {
        logResult('Компонент PlayerDetail не найден на странице', null, true);
        return;
      }
      
      const playerData = playerDetailComponent.__vue__.player;
      logResult('Данные игрока в компоненте:', playerData);
      
      if (playerData && playerData.nicknames) {
        logResult(`Никнеймы в компоненте (${playerData.nicknames.length} шт.):`, playerData.nicknames);
        
        // Проверка отображения первого никнейма
        const nicknameElement = document.querySelector('.player-detail .text-gray-600');
        if (nicknameElement) {
          logResult('Отображаемый никнейм:', nicknameElement.textContent);
        } else {
          logResult('Элемент с никнеймом не найден в DOM', null, true);
        }
      } else {
        logResult('Никнеймы отсутствуют в компоненте', null, true);
      }
    } catch (error) {
      logResult('Ошибка при проверке компонента', error, true);
    }
  };

  // Основная функция проверки
  const checkNicknames = async () => {
    console.clear();
    console.log('%c Проверка обработки никнеймов игроков ', 'background: #4b5563; color: white; padding: 5px;');
    
    // Пытаемся получить ID игрока из URL
    const pathParts = window.location.pathname.split('/');
    const playerIndex = pathParts.indexOf('players');
    
    if (playerIndex === -1 || playerIndex === pathParts.length - 1) {
      logResult('Ошибка: Нет ID игрока в URL', 'Перейдите на страницу игрока для проверки', true);
      return;
    }
    
    const playerId = pathParts[playerIndex + 1];
    logResult('ID игрока из URL:', playerId);
    
    // Запускаем все проверки
    const playerFromStore = await checkPlayerModel(playerId);
    const playerFromApi = await checkDirectApiCall(playerId);
    checkRenderingComponent(playerId);
    
    // Сравнение данных
    if (playerFromStore && playerFromApi) {
      const storeHasNicknames = playerFromStore.nicknames && playerFromStore.nicknames.length > 0;
      const apiHasNicknames = playerFromApi.nicknames && playerFromApi.nicknames.length > 0;
      
      if (storeHasNicknames !== apiHasNicknames) {
        logResult('Обнаружено расхождение!', `API: ${apiHasNicknames ? 'есть никнеймы' : 'нет никнеймов'}, Хранилище: ${storeHasNicknames ? 'есть никнеймы' : 'нет никнеймов'}`, true);
      } else {
        logResult('Данные в API и хранилище согласованы', `Никнеймы ${storeHasNicknames ? 'присутствуют' : 'отсутствуют'} в обоих источниках`);
      }
    }
    
    console.log('%c Проверка завершена ', 'background: #10b981; color: white; padding: 5px;');
  };

  // Выполняем проверку
  checkNicknames();
})(); 