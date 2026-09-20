# Скрипт для установки бота как Windows Service
# Запусти этот файл как администратор!

$botPath = "c:\Users\bilol\OneDrive\Desktop\telegramm_bot"
$serviceName = "TelegramBot"
$pythonPath = "C:\Users\bilol\AppData\Local\Programs\Python\Python311\python.exe"

# Проверяем, существует ли служба
$service = Get-Service -Name $serviceName -ErrorAction SilentlyContinue

if ($service) {
    Write-Host "Служба уже существует. Удаляю старую версию..."
    Stop-Service -Name $serviceName -Force
    Remove-Item "HKLM:\SYSTEM\CurrentControlSet\Services\$serviceName" -Force
}

# Создаем батник для запуска бота
$batContent = @"
@echo off
cd /d "$botPath"
python bot.py
"@

$batContent | Out-File -FilePath "$botPath\start_bot.bat" -Encoding ASCII

# Создаем новую службу
Write-Host "Создаю Windows Service..."
New-Service -Name $serviceName `
    -DisplayName "Telegram Bot Service" `
    -BinaryPathName "cmd.exe /c $botPath\start_bot.bat" `
    -StartupType Automatic | Out-Null

Write-Host "✅ Служба создана!"
Write-Host "Запускаю бота..."

Start-Service -Name $serviceName

Write-Host "✅ Бот запущен!"
Write-Host "Бот будет автоматически запускаться при включении ПК"
