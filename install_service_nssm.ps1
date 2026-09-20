# Установка бота как Windows Service с использованием NSSM
# Шаг 1: Скачай NSSM с https://nssm.cc/download
# Шаг 2: Распакуй в папку проекта
# Шаг 3: Запусти этот скрипт как администратор

$botPath = "c:\Users\bilol\OneDrive\Desktop\telegramm_bot"
$nssmPath = "$botPath\nssm\win64\nssm.exe"
$serviceName = "TelegramBot"
$pythonPath = "C:\Users\bilol\AppData\Local\Programs\Python\Python311\python.exe"

# Проверяем, существует ли NSSM
if (-not (Test-Path $nssmPath)) {
    Write-Host "❌ NSSM не найден!"
    Write-Host "Скачай NSSM отсюда: https://nssm.cc/download"
    Write-Host "Распакуй в папку: $botPath\nssm"
    exit
}

# Проверяем, существует ли служба
$service = Get-Service -Name $serviceName -ErrorAction SilentlyContinue

if ($service) {
    Write-Host "⚠️ Служба уже существует. Удаляю старую версию..."
    & $nssmPath stop $serviceName
    & $nssmPath remove $serviceName confirm
}

Write-Host "📦 Создаю Windows Service..."

# Создаем службу с NSSM
& $nssmPath install $serviceName $pythonPath "$botPath\bot.py"

# Настраиваем работу директории
& $nssmPath set $serviceName AppDirectory "$botPath"

# Настраиваем автоматический перезапуск при ошибке
& $nssmPath set $serviceName AppExit Default Restart

# Устанавливаем тип автозапуска
& $nssmPath set $serviceName Start SERVICE_AUTO_START

Write-Host "✅ Служба создана успешно!"
Write-Host "🚀 Запускаю бота..."

& $nssmPath start $serviceName

Write-Host "✅ Бот работает 24/7!"
Write-Host ""
Write-Host "Полезные команды:"
Write-Host "Остановить:    $nssmPath stop $serviceName"
Write-Host "Перезагрузить: $nssmPath restart $serviceName"
Write-Host "Удалить:       $nssmPath remove $serviceName confirm"
