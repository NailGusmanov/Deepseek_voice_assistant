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
   python --version
