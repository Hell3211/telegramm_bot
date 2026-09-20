@echo off
REM Бот будет работать 24/7
REM Если упадет - перезапустится автоматически

cd /d "c:\Users\bilol\OneDrive\Desktop\telegramm_bot"

:loop
echo.
echo ======================================
echo  🤖 Запуск Telegram бота...
echo  Время: %date% %time%
echo ======================================
echo.

python bot.py

echo.
echo ❌ Бот упал! Перезапуск через 5 секунд...
echo.
timeout /t 5

goto loop
