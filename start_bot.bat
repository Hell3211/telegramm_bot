@echo off
REM Простой способ запустить бота при включении ПК через планировщик задач
REM 
REM Инструкция:
REM 1. Сохрани этот файл как start_bot.bat
REM 2. Открой Task Scheduler (Планировщик задач)
REM 3. Создай новую задачу:
REM    - Триггер: При запуске системы
REM    - Действие: Запустить программу (этот батник)
REM    - Опция: Запустить с наивысшими привилегиями

cd /d "c:\Users\bilol\OneDrive\Desktop\telegramm_bot"

REM Устанавливаем зависимости если нужно
REM pip install -r requirements.txt

REM Запускаем бота
python bot.py

REM Если бот упал, перезапускаем каждые 10 секунд
:loop
timeout /t 10
python bot.py
goto loop
