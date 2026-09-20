@echo off
REM Скрипт для создания автозапуска бота в Windows Планировщике
REM Запусти этот файл как администратор!

setlocal enabledelayedexpansion

set BOT_PATH=c:\Users\bilol\OneDrive\Desktop\telegramm_bot
set BOT_RUNNER=%BOT_PATH%\run_bot_forever.bat
set TASK_NAME=TelegramBot24x7

echo.
echo ======================================
echo  🤖 Создание автозапуска бота
echo ======================================
echo.

REM Проверяем права администратора
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ОШИБКА: Запусти этот файл от администратора!
    echo.
    echo Как это сделать:
    echo 1. Правый клик на этот файл
    echo 2. "Запустить от имени администратора"
    echo.
    pause
    exit /b 1
)

echo ✅ Права администратора подтверждены!
echo.

REM Удаляем старую задачу если существует
echo Проверяю наличие старой задачи...
tasklist /FI "TASKNAME eq %TASK_NAME%" 2>NUL | find /I /N "%TASK_NAME%">NUL
if "%ERRORLEVEL%"=="0" (
    echo Удаляю старую задачу...
    schtasks /delete /tn %TASK_NAME% /f >nul 2>&1
)

echo.
echo 📋 Создаю новую задачу в Планировщике...
echo.

REM Создаем новую задачу
schtasks /create /tn %TASK_NAME% /tr "%BOT_RUNNER%" /sc onlogon /rl highest /f

if %errorlevel% equ 0 (
    echo.
    echo ✅ УСПЕШНО! Задача создана!
    echo.
    echo 📌 Информация:
    echo   Имя задачи: %TASK_NAME%
    echo   Запуск: При входе в систему
    echo   Уровень: Администратор
    echo   Батник: %BOT_RUNNER%
    echo.
    echo 🚀 Бот будет автоматически запускаться при включении ПК!
    echo.
    echo ⚠️  Примечание:
    echo   - Если нужна отладка, откройте батник вручную
    echo   - Лог работы не сохраняется (можешь добавить сам)
    echo.
) else (
    echo.
    echo ❌ ОШИБКА при создании задачи!
    echo Попробуй еще раз...
    echo.
)

pause
