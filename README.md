# DeepSeek Voice Assistant

<div align="center">

*Голосовой ассистент для Telegram на основе DeepSeek AI*

[![Python Version](https://img.shields.io/badge/python-3.14%2B-blue)](https://www.python.org/)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue)](https://core.telegram.org/bots)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

## Что это за проект?

DeepSeek Voice Assistant - это Telegram бот, который:
- Принимает голосовые сообщения от пользователей
- Преобразует речь в текст с помощью Whisper AI
- Обрабатывает запросы через DeepSeek API
- Отвечает текстовыми сообщениями

## Технологии которые используются

### Основные технологии:
- Python 3.14 - основной язык программирования (протестировано на Python 3.14)
- python_telegram_bot - библиотека для работы с Telegram API
- OpenAI Whisper - бесплатная модель для распознавания речи
- DeepSeek API - искусственный интеллект для обработки запросов
- FFmpeg - инструмент для обработки аудиофайлов

### Вспомогательные библиотеки:
- python-dotenv - для управления настройками
- requests - для отправки HTTP запросов
- logging - для ведения логов работы бота

## Установка и настройка

### Предварительные требования

   ```bash
python - 3.14 version
git - 2.51.1 version
ffmpeg - 8.0 version

# Копируем проект на ваш компьютер
git clone https://github.com/NailGusmanov/deepseek_voice_assistant.git
cd deepseek_voice_assistant

# Создаем изолированное окружение для Python
python -m venv venv

# Активируем окружение
# Для Windows:
venv\Scripts\activate

# Устанавливаем все нужные библиотеки
pip install -r requirements.txt

# Копируем шаблон настроек
cp .env.example .env

# Редактируем файл .env текстовым редактором
# Добавляйте ваши реальные API ключи

Получение API ключей

1. Telegram Bot Token

1. Найти в Telegram @BotFather
2. Отправить команду /newbot
3. Выбрать имя и username для бота
4. Скопировать выданный токен

2. DeepSeek API Key

1. Зарегистрироваться на platform.deepseek.com
2. Перейти в раздел API Keys
3. Создать новый API ключ
4. Скопировать ключ

# Убедитесь что виртуальное окружение активировано
venv\Scripts\activate    # для Windows

# Запускаем бота
python_deepseek_bot.py

# Структура проекта
deepseek_voice_assistant/
├── deepseek_bot.py          # Основной код бота
├── requirements.txt         # Список зависимостей
├── .env.example            # Шаблон настроек
├── .gitignore              # Игнорируемые файлы
└── README.md               # Эта инструкция

# Как работает бот
Пользователь → Голосовое сообщение → Telegram → Наш сервер →

Распознавание речи → Текст запроса → DeepSeek API → Текстовый ответ

# Частые проблемы
1. "ModuleNotFoundError"
  
   # Решение: переустановить зависимости
   pip install -r requirements.txt

2. Проблемы с API ключами
   · Проверить что файл .env создан
   · Убедиться что ключи вписаны без кавычек
   · Проверить что файл находится в той же папке что и бот

Если у вас возникли вопросы:

1. Проверьте этот README еще раз 😂
