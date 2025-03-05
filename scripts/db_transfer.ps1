# PowerShell скрипт для переноса базы данных из локального Docker на боевой сервер
# Использование: .\db_transfer.ps1 -ServerIP <IP> -SSHUser <user>

param (
    [Parameter(Mandatory=$true)]
    [string]$ServerIP,
    
    [Parameter(Mandatory=$true)]
    [string]$SSHUser
)

Write-Host "=== Начинаю процесс переноса базы данных ===" -ForegroundColor Green
Write-Host "Сервер: $ServerIP"
Write-Host "Пользователь: $SSHUser"

# 1. Создаем дамп локальной базы данных
Write-Host "=== Создаю дамп локальной базы данных ===" -ForegroundColor Green
docker-compose ps
$DBContainer = (docker-compose ps | Select-String -Pattern "db").ToString().Split(" ")[0]

if (-not $DBContainer) {
    Write-Host "Ошибка: Контейнер с базой данных не найден!" -ForegroundColor Red
    exit 1
}

Write-Host "Найден контейнер базы данных: $DBContainer" -ForegroundColor Cyan
Write-Host "Создаю дамп базы данных..." -ForegroundColor Cyan
docker exec $DBContainer pg_dump -U postgres -d app -F c -f /tmp/db_backup.dump

# 2. Копируем дамп из контейнера на локальную машину
Write-Host "=== Копирую дамп на локальную машину ===" -ForegroundColor Green
docker cp ${DBContainer}:/tmp/db_backup.dump ./db_backup.dump

if (-not (Test-Path -Path "./db_backup.dump")) {
    Write-Host "Ошибка: Не удалось скопировать файл дампа из контейнера!" -ForegroundColor Red
    exit 1
}

$fileInfo = Get-Item -Path "./db_backup.dump"
Write-Host "Дамп базы данных создан: $($fileInfo.Length / 1KB) KB" -ForegroundColor Cyan

# 3. Копируем дамп на сервер
Write-Host "=== Копирую дамп на сервер ===" -ForegroundColor Green
Write-Host "Выполняется команда: scp ./db_backup.dump ${SSHUser}@${ServerIP}:/tmp/db_backup.dump"

# Проверяем, установлен ли OpenSSH
$sshCommand = Get-Command ssh -ErrorAction SilentlyContinue
if (-not $sshCommand) {
    Write-Host "ВНИМАНИЕ: Команда SSH не найдена. Убедитесь, что у вас установлен OpenSSH клиент." -ForegroundColor Yellow
    Write-Host "Вы можете включить его в 'Дополнительные компоненты Windows' -> 'Добавить компоненты' -> 'OpenSSH клиент'" -ForegroundColor Yellow
    Write-Host "Или используйте альтернативный SSH клиент, например, PuTTY" -ForegroundColor Yellow
    
    $useAlternative = Read-Host "Хотите ли вы продолжить, используя явную команду для вашего SSH клиента? (y/n)"
    if ($useAlternative -ne "y") {
        Write-Host "Операция отменена." -ForegroundColor Red
        exit 1
    }
    
    Write-Host "Руководство по ручной загрузке файла на сервер:" -ForegroundColor Yellow
    Write-Host "1. Используйте WinSCP, FileZilla или другой SFTP клиент для загрузки файла db_backup.dump"
    Write-Host "2. Загрузите файл по пути /tmp/db_backup.dump на сервере"
    Write-Host "3. Подключитесь к серверу через ваш SSH клиент"
    Write-Host "4. Проверьте запуск контейнеров: cd /var/www/fonds-relations && docker ps"
    exit 0
}

# Если OpenSSH доступен, используем его
try {
    scp ./db_backup.dump ${SSHUser}@${ServerIP}:/tmp/db_backup.dump
    Write-Host "=== Проверяю состояние CI/CD процесса на сервере ===" -ForegroundColor Green
    ssh ${SSHUser}@${ServerIP} "cd /var/www/fonds-relations && docker ps"
} catch {
    Write-Host "Ошибка при выполнении SSH/SCP команд: $_" -ForegroundColor Red
    Write-Host "Убедитесь, что у вас настроен доступ по SSH к серверу" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== Дамп базы данных успешно перенесен на сервер ===" -ForegroundColor Green
Write-Host "Путь к дампу на сервере: /tmp/db_backup.dump"
Write-Host ""
Write-Host "При следующем запуске CI/CD процесса база данных будет автоматически восстановлена из дампа." -ForegroundColor Cyan
Write-Host "Если вы хотите запустить процесс восстановления немедленно, выполните следующую команду:" -ForegroundColor Cyan
Write-Host "  ssh ${SSHUser}@${ServerIP} 'cd /var/www/fonds-relations && git pull'" -ForegroundColor Yellow 