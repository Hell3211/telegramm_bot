# Telegram Bot 🤖
# Интерактивный бот с играми и ИИ

## Требования

- Python 3.11+
- aiogram 3.4.1
- python-dotenv 1.0.0

## Установка локально

```bash
pip install -r requirements.txt
```

## Запуск

```bash
python bot.py
```

## Развертывание на облако (Render.com)

### Шаг 1: GitHub Repository

1. Создай GitHub аккаунт (если нет)
2. Создай новый репозиторий `telegramm_bot`
3. Загрузи все файлы из папки проекта

### Шаг 2: Render.com

1. Откройи https://render.com
2. Нажми "Sign up" и регистрируйся
3. Нажми "New +" → "Web Service"
4. Выбери свой GitHub репозиторий
5. Настройки:
   - **Name**: telegramm-bot
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`

### Шаг 3: Переменные окружения

В Render.com в разделе "Environment":
- Добавь: `BOT_TOKEN` = твой токен бота

### Шаг 4: Deploy

Нажми "Deploy" и жди ~2 минуты.

✅ Готово! Бот работает на облаке 24/7! ☁️

## Преимущества облака:

✅ Бот работает 24/7
✅ Не нужен включенный ПК
✅ Высокая надежность
✅ Бесплатно!

## Команды бота

- `/start` - главное меню
- `/help` - справка
- `🎮 Игры` - кубик, рулетка, викторина
- `🤖 ИИ` - умный помощник
- `😂 Шутка` - анекдот
- `📊 Очки` - твоя статистика

Приятной игры! 🎉
