import os
import logging
import requests
import subprocess
import tempfile
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Глобальные переменные
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

if not TOKEN or not DEEPSEEK_API_KEY:
    raise ValueError("Проверьте TELEGRAM_BOT_TOKEN и DEEPSEEK_API_KEY в .env файле")

# Создаем приложение
application = Application.builder().token(TOKEN).build()

# Функции для ответов
def get_fallback_response(message: str) -> str:
    """Умные ответы когда AI недоступен"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['привет', 'здравств', 'hello', 'hi']):
        return "Привет! 👋 Я голосовой ассистент. AI сервис временно недоступен!"
    elif any(word in message_lower for word in ['как дела', 'как ты']):
        return "Всё отлично! 🚀 Работаю над интеграцией AI."
    elif '?' in message:
        return "🤔 Интересный вопрос! Пока AI сервис настраивается."
    else:
        return "Сообщение получено! 📝 Я голосовой ассистент."

async def get_deepseek_response(message: str) -> str:
    """Запрос к DeepSeek API"""
    try:
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
        data = {"model": "deepseek-chat", "messages": [{"role": "user", "content": message}]}
        
        response = requests.post(url, json=data, headers=headers, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return get_fallback_response(message)
            
    except Exception as e:
        logger.error(f"Ошибка AI API: {e}")
        return get_fallback_response(message)

async def handle_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ВСЕХ входящих сообщений для отладки"""
    print(f"🔥 ВХОДЯЩЕЕ СООБЩЕНИЕ:")
    print(f"🔥 User: {update.effective_user.id}")
    
    # Правильный способ определения типа сообщения
    if update.message.text:
        print(f"🔥 Тип: text")
        print(f"🔥 Текст: {update.message.text}")
    elif update.message.voice:
        print(f"🔥 Тип: voice")
        print(f"🔥 Голосовое: {update.message.voice.duration} сек")
    elif update.message.audio:
        print(f"🔥 Тип: audio") 
        print(f"🔥 Аудио: {update.message.audio.duration} сек")
    elif update.message.document:
        print(f"🔥 Тип: document")
    elif update.message.photo:
        print(f"🔥 Тип: photo")
    elif update.message.video:
        print(f"🔥 Тип: video")
    else:
        print(f"🔥 Тип: unknown")
    
    print("---")

# Обработчики команд
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"🎯 Команда /start от {update.effective_user.id}")
    await update.message.reply_text(
        "🤖 **DeepSeek Voice Assistant**\n\n"
        "Привет! Я твой голосовой ассистент.\n\n"
        "Отправь мне текстовое сообщение! 🚀",
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"🎯 Команда /help от {update.effective_user.id}")
    await update.message.reply_text(
        "ℹ️ **Помощь**\n\n"
        "• /start - начать работу\n"
        "• /help - эта справка\n"
        "• Текст - AI ответ\n"
        "• Голос - скоро будет!",
        parse_mode='Markdown'
    )

# Обработчик текстовых сообщений
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.effective_user.id
    print(f"📝 Текст от {user_id}: {user_message}")
    
    try:
        response = await get_deepseek_response(user_message)
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await update.message.reply_text("❌ Ошибка обработки")

# Обработчик голосовых сообщений
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка голосовых сообщений с отладкой"""
    user_id = update.effective_user.id
    print(f"🔥 ГОЛОС: Получено голосовое сообщение от {user_id}")
    
    try:
        print("🔥 ГОЛОС: Начинаю обработку...")
        
        # Проверяем что это действительно голосовое сообщение
        if not update.message.voice:
            print("❌ ГОЛОС: Это не голосовое сообщение!")
            await update.message.reply_text("❌ Это не голосовое сообщение")
            return
            
        print(f"🔥 ГОЛОС: Длительность: {update.message.voice.duration} сек")
        print(f"🔥 ГОЛОС: Размер файла: {update.message.voice.file_size} байт")
        
        # Отправляем подтверждение
        await update.message.reply_text("🎤 Получил голосовое сообщение! Обрабатываю...")
        
        # Тестовый ответ
        response = await get_deepseek_response("Пользователь отправил голосовое сообщение. Ответь что ты его получил и скоро сможешь распознавать речь.")
        await update.message.reply_text(f"🤖 {response}")
        
        print("✅ ГОЛОС: Обработка завершена успешно!")
        
    except Exception as e:
        print(f"❌ ГОЛОС: Ошибка: {e}")
        logger.error(f"Ошибка обработки голосового сообщения: {e}")
        await update.message.reply_text("❌ Ошибка обработки голосового сообщения")

# Настройка обработчиков
print("🔧 Настраиваю обработчики...")
application.add_handler(MessageHandler(filters.ALL, handle_all_messages))  # ← ПЕРВЫЙ!
application.add_handler(CommandHandler("start", start_command))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
application.add_handler(MessageHandler(filters.VOICE, handle_voice))
print("✅ Все обработчики настроены!")

# Запуск бота
if __name__ == "__main__":
    print("🚀 DeepSeek Voice Assistant запускается...")
    print("🤖 Бот активирован!")
    
    # ПРОСТОЙ ТЕСТ: Проверим базовое подключение
    print("🔍 Простой тест подключения...")
    try:
        # Просто проверим что бот может сделать запрос
        import requests
        test_url = f"https://api.telegram.org/bot{TOKEN}/getMe"
        response = requests.get(test_url, timeout=10)
        print(f"✅ Telegram API доступен. Статус: {response.status_code}")
        
        if response.status_code == 200:
            bot_info = response.json()
            print(f"✅ Бот: {bot_info['result']['first_name']} (@{bot_info['result']['username']})")
        else:
            print(f"❌ Ошибка API: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка теста: {e}")
    
    print("🔍 Проверяем очередь сообщений...")
    try:
        # Простой синхронный запрос для проверки очереди
        import requests
        updates_url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        response = requests.get(updates_url, timeout=10)
        
        if response.status_code == 200:
            updates_data = response.json()
            updates_count = len(updates_data['result'])
            print(f"📡 Сообщений в очереди: {updates_count}")
            
            if updates_count > 0:
                print("💡 В очереди есть сообщения! Отправь '/start' чтобы очистить.")
                for update in updates_data['result']:
                    print(f"   - Update {update['update_id']}")
            else:
                print("📭 Очередь сообщений пуста")
        else:
            print(f"❌ Ошибка получения updates: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Ошибка проверки очереди: {e}")
    
    print("🚀 Запускаю основной цикл...")
    application.run_polling()
