import os
import logging
from dotenv import load_dotenv

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
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        
        if not self.token or not self.deepseek_api_key:
            logger.error("Не найдены TELEGRAM_BOT_TOKEN или DEEPSEEK_API_KEY в .env файле")
            raise ValueError("Проверьте настройки окружения")
    
    def start(self):
        """Запуск бота"""
        logger.info("DeepSeek Voice Assistant запускается...")
        print("DeepSeek Voice Assistant активирован!")
        print("Готов к приему голосовых сообщений!")
        # Заглушка - реальную логику добавить позже
        self._keep_alive()
    
    def _keep_alive(self):
        """Заглушка чтобы бот не закрывался"""
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Бот остановлен пользователем")

def main():
    try:
        assistant = DeepSeekVoiceAssistant()
        assistant.start()
    except Exception as e:
        logger.error(f"Ошибка запуска: {e}")
        print("❌ Проверьте настройки в .env файле")

if name == "__main__":
    main()
