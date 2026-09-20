import logging
import os
import random
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получаем токен
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN не установлен!")

# Создаем объекты
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Данные
user_stats = {}
user_mode = {}

# Данные для игр
JOKES = [
    "Почему программист вышел из ванны? Потому что C# острый! 🔪",
    "Как назвать программиста-рыбака? Stack Overflow! 🎣",
    "Сколько программистов вкрутить лампочку? Ни одного - железо! 💡",
]

MAGIC = ["Да! ✅", "Нет ❌", "Может быть 🤔", "Конечно! 💯", "Вряд ли 😔"]

QUIZ = [
    {"вопрос": "2+2=?", "ответ": "4"},
    {"вопрос": "Столица России?", "ответ": "москва"},
    {"вопрос": "Планет?", "ответ": "8"},
]

# МЕНЮ
def main_menu():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🎮 Игры"), KeyboardButton(text="🤖 ИИ")],
        [KeyboardButton(text="😂 Шутка"), KeyboardButton(text="📊 Очки")],
    ], resize_keyboard=True)

def games_menu():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🎲 Кубик"), KeyboardButton(text="🎰 Рулетка")],
        [KeyboardButton(text="🔮 Шар"), KeyboardButton(text="❓ Викторина")],
        [KeyboardButton(text="◀️ Назад")],
    ], resize_keyboard=True)

# /start
@dp.message(Command("start"))
async def start(message: Message):
    uid = message.from_user.id
    if uid not in user_stats:
        user_stats[uid] = {"очки": 0}
    
    await message.answer(
        f"🎉 Привет, {message.from_user.first_name}!\n"
        f"Выбери что-нибудь:",
        reply_markup=main_menu()
    )

# ГЛАВНОЕ МЕНЮ
@dp.message(F.text == "🎮 Игры")
async def games(message: Message):
    await message.answer("🎮 Выбери игру:", reply_markup=games_menu())

@dp.message(F.text == "◀️ Назад")
async def back(message: Message):
    uid = message.from_user.id
    user_mode.pop(uid, None)
    await message.answer("📌 Меню:", reply_markup=main_menu())

@dp.message(F.text == "🤖 ИИ")
async def ai(message: Message):
    uid = message.from_user.id
    user_mode[uid] = "ai"
    await message.answer(
        "🤖 Привет! Напиши вопрос:\n"
        "(Напиши 'Назад' чтобы выйти)",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Назад")]],
            resize_keyboard=True
        )
    )

@dp.message(F.text == "😂 Шутка")
async def joke(message: Message):
    await message.answer(f"😂 {random.choice(JOKES)}", reply_markup=main_menu())

@dp.message(F.text == "📊 Очки")
async def stats(message: Message):
    uid = message.from_user.id
    очки = user_stats.get(uid, {}).get("очки", 0)
    await message.answer(f"📊 Твои очки: {очки} 🎯", reply_markup=main_menu())

# ИГРЫ
@dp.message(F.text == "🎲 Кубик")
async def dice(message: Message):
    uid = message.from_user.id
    roll = random.randint(1, 6)
    user_stats[uid]["очки"] += roll
    await message.answer(
        f"🎲 Выпало: {roll}\nОчки: {user_stats[uid]['очки']} 🎯",
        reply_markup=games_menu()
    )

@dp.message(F.text == "🎰 Рулетка")
async def roulette(message: Message):
    uid = message.from_user.id
    num = random.randint(0, 36)
    user_stats[uid]["очки"] += num
    await message.answer(
        f"🎰 Число: {num}\nОчки: {user_stats[uid]['очки']} 🎯",
        reply_markup=games_menu()
    )

@dp.message(F.text == "🔮 Шар")
async def magic(message: Message):
    ans = random.choice(MAGIC)
    await message.answer(f"🔮 {ans}", reply_markup=games_menu())

@dp.message(F.text == "❓ Викторина")
async def quiz(message: Message):
    uid = message.from_user.id
    q = random.choice(QUIZ)
    user_stats[uid]["вопрос"] = q["ответ"]
    user_mode[uid] = "quiz"
    await message.answer(
        f"❓ {q['вопрос']}\n"
        f"(или 'Пропустить')",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Пропустить")]],
            resize_keyboard=True
        )
    )

# ИИ И ВИКТОРИНА
@dp.message(lambda msg: user_mode.get(msg.from_user.id) == "ai")
async def ai_answer(message: Message):
    uid = message.from_user.id
    user_text = message.text.lower().strip()
    
    if user_text == "назад":
        user_mode.pop(uid, None)
        await message.answer("📌 Меню:", reply_markup=main_menu())
        return
    
    # Большая база ответов ИИ
    ai_base = {
        # Приветствия
        "привет": "Привет! 👋 Как дела? Чем я могу помочь?",
        "привет бот": "Привет! 🤖 Рад видеть!",
        "здравствуй": "Здравствуй! 🙂 Что нужно?",
        "hello": "Hello! 👋 How are you?",
        
        # Самочувствие
        "как дела": "Отлично! 😊 А у тебя как? Что-то беспокоит?",
        "как жизнь": "Жизнь прекрасна! 😄 Как твои дела?",
        "что ты делаешь": "Я помогаю людям! 🤖 Отвечаю на вопросы и развлекаю!",
        
        # О боте
        "кто ты": "Я ИИ бот! 🤖 Я создан для помощи и развлечения!",
        "что ты": "Я интерактивный Telegram-бот с ИИ! 🤖",
        "расскажи о себе": "Я бот с ИИ! 🤖 Помогаю людям через Telegram!",
        "ты живой": "Я программа, но я живой в своем роде! 🤖",
        
        # Спасибо
        "спасибо": "Пожалуйста! 😌 Рад был помочь!",
        "благодарю": "Спасибо за благодарность! 😊",
        "спс": "Пожалуйста! 😊",
        
        # Прощание
        "пока": "До встречи! 👋 Приходи еще!",
        "до свидания": "До встречи! 👋",
        "пока бот": "Пока! 👋 Буду ждать!",
        "до скорого": "До скорого! 😊",
        
        # Ночь/Утро/День
        "спокойной ночи": "Спокойной ночи! 😴 Хорошо спи!",
        "доброе утро": "Доброе утро! ☀️ Как спалось?",
        "добрый день": "Добрый день! 🌤️ Как погода?",
        "добрый вечер": "Добрый вечер! 🌙 Как прошел день?",
        
        # Помощь
        "помощь": "Я помогу! 🆘 Расскажи, что нужно?",
        "помоги": "Помогу с удовольствием! 💪 В чем помочь?",
        "нужна помощь": "Я здесь! 🤝 Что тебе нужно?",
        
        # Вопросы о знаниях
        "сколько будет 2+2": "2+2 = 4! 🧮 Просто математика!",
        "2+2": "4! ✅",
        "столица россии": "Москва! 🏛️ Красивый город!",
        "москва": "Столица России! 🏛️",
        "сколько планет": "8 планет! 🌍 Земля одна из них!",
        
        # Развлечения
        "расскажи шутку": "😂 Почему программист вышел из ванны? Потому что слышал C# острый!",
        "смешная история": "😂 Stack Overflow - это как назвать программиста-рыбака!",
        "анекдот": "😂 Сколько программистов вкрутить лампочку? Ни одного - это железо!",
        "пошути": "😂 Java и Python встретились... Java говорит: я более строгий! Python: а я красивее!",
        
        # Вопросы о времени
        "сколько времени": "Пора играть! 🎮 Давай сыграем?",
        "который час": "Время больших дел! ⏰",
        "какое время": "Время развлекаться! 🎉",
        
        # Эмоции
        "я грустный": "Не грусти! 😊 Давай поиграем? Это поднимет настроение!",
        "я грущу": "Давай поиграем в кубик! 🎲 Может повезет?",
        "мне скучно": "Давай играть! 🎮 У меня есть кубик, рулетка и викторина!",
        "я одинок": "Ты не один! 🤝 Я здесь с тобой!",
        "люблю тебя": "Я тоже люблю помогать! 💙",
        
        # Желания и планы
        "давай играть": "Да! 🎮 Выбери: кубик, рулетка или викторина?",
        "хочу играть": "Отлично! 🎲 Какую игру выбираешь?",
        "давай сыграем": "Играем! 🎰 Ставка на везение!",
        
        # Вопросы почему
        "почему ты бот": "Потому что я создан программистом! 👨💻",
        "зачем ты": "Я создан чтобы помогать людям! 🤖",
        "какой смысл": "Смысл в том, чтобы развлекать и помогать! 😊",
        
        # Одобрение/Неодобрение
        "ты молодец": "Спасибо! 😊 Ты тоже молодец!",
        "ты отличный": "Благодаря тебе! 💙 Ты крутой!",
        "ты плохой": "Извини! 😔 Я стараюсь улучшаться!",
    }
    
    # Поиск ответа
    for key, answer in ai_base.items():
        if key in user_text:
            await message.answer(answer)
            return
    
    # Если нет точного совпадения - генерируем универсальный ответ
    if "?" in message.text:
        # Это вопрос
        await message.answer(
            f"🤔 Хороший вопрос: *{message.text}*\n\n"
            f"Я думаю... 💭\n"
            f"Это интересная тема! Попробуй еще раз переформулировать или напиши проще! 😊"
        )
    elif len(user_text) > 15:
        # Длинное сообщение
        await message.answer(
            f"✨ Интересное сообщение!\n\n"
            f"*{message.text[:50]}...*\n\n"
            f"Мне нравится! 😊 Расскажи больше?"
        )
    elif len(user_text) < 2:
        # Очень короткое
        await message.answer("Напиши что-нибудь посложнее! 😊")
    else:
        # Среднее сообщение
        await message.answer(
            f"🎯 Ты сказал: *{message.text}*\n\n"
            f"Интересно! 🤔 Расскажи подробнее!"
        )

@dp.message(lambda msg: user_mode.get(msg.from_user.id) == "quiz")
async def quiz_answer(message: Message):
    uid = message.from_user.id
    
    if message.text == "Пропустить":
        user_mode.pop(uid, None)
        await message.answer("Выбери игру:", reply_markup=games_menu())
        return
    
    correct = user_stats[uid].get("вопрос", "").lower()
    if message.text.lower() == correct:
        user_stats[uid]["очки"] += 10
        await message.answer(
            f"✅ Правильно! +10 очков\n"
            f"Всего: {user_stats[uid]['очки']} 🎯",
            reply_markup=games_menu()
        )
    else:
        await message.answer(
            f"❌ Неправильно! Ответ: {correct}\n"
            f"Очки: {user_stats[uid]['очки']}",
            reply_markup=games_menu()
        )
    
    user_mode.pop(uid, None)

# ГЛАВНАЯ ФУНКЦИЯ
async def main():
    logger.info("🤖 Бот запущен!")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
