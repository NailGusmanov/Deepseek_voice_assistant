import os
import logging
import requests
import subprocess
import tempfile
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class DeepSeekVoiceAssistant:
    def __init__(self):
        # Загрузка конфигурации
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        self.model = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')
        
        # Проверка обязательных переменных
        if not self.token or not self.deepseek_api_key:
            logger.error("Не найдены TELEGRAM_BOT_TOKEN или DEEPSEEK_API_KEY")
            raise ValueError("Проверьте настройки в .env файле")
        
        # Инициализация Telegram бота
        self.application = Application.builder().token(self.token).build()
        
        # Настройка обработчиков
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Настройка обработчиков сообщений"""
        # Обработчик текстовых сообщений
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text_message)
        )
        
        # Обработчик голосовых сообщений (пока заглушка)
        self.application.add_handler(
            MessageHandler(filters.VOICE, self.handle_voice_message)
        )
    
    async def handle_text_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка текстовых сообщений"""
        user_message = update.message.text
        user_id = update.message.from_user.id
        
        logger.info(f"Текст от пользователя {user_id}: {user_message}")
        
        try:
            # Получаем ответ от DeepSeek
            response = await self._get_deepseek_response(user_message)
            
            # Отправляем ответ пользователю
            await update.message.reply_text(response)
            
        except Exception as e:
            logger.error(f"Ошибка обработки сообщения: {e}")
            await update.message.reply_text("❌ Произошла ошибка при обработке запроса")
    
    async def import subprocess

async def  handle_voice_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка голосовых сообщений с использованием FFmpeg"""
    try:
        # Уведомляем пользователя о начале обработки
        await update.message.reply_text("🎤 Обрабатываю голосовое сообщение...")
        
        # Скачиваем голосовое сообщение
        voice_file = await update.message.voice.get_file()
        
        # Создаем временные файлы
        with tempfile.NamedTemporaryFile(suffix='.oga', delete=False) as oga_file:
            oga_path = oga_file.name
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as wav_file:
            wav_path = wav_file.name
        
        # Скачиваем файл
        await voice_file.download_to_drive(oga_path)
        
        # Конвертируем в WAV через FFmpeg (используем полный путь)
        ffmpeg_path = r"C:\Users\user\Desktop\ffmpeg\bin\ffmpeg.exe"
        command = [
            ffmpeg_path, 
            '-i', oga_path, 
            '-acodec', 'pcm_s16le', 
            '-ac', '1', 
            '-ar', '16000', 
            wav_path,
            '-y'
        ]
        
        # Запускаем FFmpeg
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            raise Exception(f"FFmpeg error: {result.stderr}")
        
        # Проверяем что файл создан
        if not os.path.exists(wav_path):
            raise Exception("Конвертированный файл не создан")
        
        # Пока временный ответ (Whisper добавим позже)
        text = "[РАСПОЗНАННЫЙ ТЕКСТ] Голосовое сообщение успешно обработано! Распознавание текста скоро будет добавлено."
        
        # Получаем ответ от DeepSeek
        response = await self._get_deepseek_response(text)
        await update.message.reply_text(f"🎤 Распознано: {text}\n\n Ответ: {response}")
        
    except Exception as e:
        logger.error(f"Ошибка обработки голосового сообщения: {e}")
        await update.message.reply_text("❌ Ошибка обработки голосового сообщения")
    
    finally:
        # Удаляем временные файлы
        for file_path in [oga_path, wav_path]:
            if os.path.exists(file_path):
                try:
                    os.unlink(file_path)
                except:
                    pass
        
        # Здесь будет распознавание через Whisper
        # text = whisper_model.transcribe(wav_path)["text"]
        
        # Временный ответ
        await update.message.reply_text("🎤 Голосовое сообщение получено! Распознавание скоро будет добавлено.")
        
    except Exception as e:
        logger.error(f"Ошибка обработки голосового сообщения: {e}")
        await update.message.reply_text("❌ Ошибка обработки голосового сообщения")
    
    finally:
        # Удаляем временные файлы
        for file_path in [oga_path, wav_path]:
            if os.path.exists(file_path):
                os.unlink(file_path)
    
   async def _get_deepseek_response(self, message: str) -> str:
    """Запрос к DeepSeek API с отладкой"""
    url = url = "https://api.deepseek.com/v1/models"
    
    headers = {
        "Authorization": f"Bearer {self.deepseek_api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": self.model,
        "messages": [
            {"role": "user", "content": message}
        ],
        "stream": False
    }
    
    try:
        print(f"🔍 Отправка запроса к DeepSeek API...")
        print(f"🔑 Ключ: {self.deepseek_api_key[:10]}...")  # Покажем только начало ключа
        print(f"📝 Сообщение: {message}")
        
        response = requests.post(url, json=data, headers=headers, timeout=30)
        print(f"📡 Статус ответа: {response.status_code}")
        
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ Ответ получен успешно!")
        return result['choices'][0]['message']['content']
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка DeepSeek API: {e}")
        print(f"❌ Ошибка запроса: {e}")
        return "⚠️ Не удалось получить ответ от AI. Попробуйте позже."
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        print(f"❌ Неожиданная ошибка: {e}")
        return "⚠️ Произошла непредвиденная ошибка."
