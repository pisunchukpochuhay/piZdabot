import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.exceptions import TelegramAPIError, TelegramConflictError, TelegramUnauthorizedError
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from colorama import Fore, Style, init

# Инициализация colorama
init(autoreset=True)

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Сообщение и кнопки
start_message = (
    "🍒 Платформа для Встречи❤️‍🔥 😈❤️‍🔥 Только у нас проверенные бабочки🍒🍌🧚‍♀️\n\n"
    "Наши девочки заставят Вас сиять!💋\n"
    "Стоит только попробовать!💋\n\n"
    "https://telegra.ph/Sweetnighte-01-13\n"
)

button1 = InlineKeyboardButton(text="Провести прекрасный вечер💋", url="https://telegra.ph/Sweetnighte-01-13")
button2 = InlineKeyboardButton(text="Заказать встречу", url="https://telegra.ph/Sweetnighte-01-13")
keyboard = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2]])

# Обработка команды /start
async def start(message: types.Message):
    await message.reply(start_message, reply_markup=keyboard)

# Запуск одного бота
async def run_bot(api_key: str, index: int):
    bot = Bot(token=api_key)
    dp = Dispatcher()
    dp.message.register(start, Command(commands=['start']))

    try:
        # Удаляем вебхук перед запуском long polling
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info(f"{Fore.GREEN}Bot {index + 1} with token {api_key} started.{Style.RESET_ALL}")

        # Запускаем long polling
        await dp.start_polling(bot, timeout=30, interval=2, allowed_updates=["message", "callback_query"])
    except TelegramUnauthorizedError:
        logger.error(f"{Fore.RED}Unauthorized error for bot {index + 1}. Check the API key.{Style.RESET_ALL}")
    except TelegramConflictError:
        logger.error(f"{Fore.RED}Conflict error for bot {index + 1}. Another instance is running.{Style.RESET_ALL}")
    except TelegramAPIError as e:
        logger.error(f"{Fore.RED}API error for bot {index + 1}: {e}{Style.RESET_ALL}")
    except Exception as e:
        logger.error(f"{Fore.RED}Unexpected error for bot {index + 1}: {e}{Style.RESET_ALL}")

# Запуск всех ботов
async def main():
    try:
        with open('api_keys.txt', 'r') as file:
            api_keys = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        logger.error("File api_keys.txt not found.")
        return
    except Exception as e:
        logger.error(f"Error reading api_keys.txt: {e}")
        return

    tasks = [run_bot(api_key, index) for index, api_key in enumerate(api_keys)]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
