import logging
from re import compile, findall

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import pymysql

from config import API_TOKEN, GROUP_ID

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

from pymysql.cursors import DictCursor

date_base = pymysql.connect(
    host='localhost',
    user='user',
    password='password',
    db='iata',
    charset='utf8mb4',
    cursorclass=DictCursor
)


@dp.message_handler(lambda message: message.chat.id == GROUP_ID and compile(r'^!ц$').search(message.text))
async def echo(message: types.ForceReply):
    save(message.reply_to_message.message_id, message.reply_to_message.date,
         message.reply_to_message.from_user.username, message.reply_to_message.text)
    await bot.send_sticker(message.chat.id, r'CAACAgIAAxkBAAEBA3dfA1xTFga3-FmdbL1rqNVvqcbBSQACTwIAAvXt7AUyYpkJ0M9IyBoE')
    await bot.send_message(message.chat.id, last_quote - 1)


@dp.message_handler(lambda message: message.chat.id == GROUP_ID and compile(r'^!ц \d+$').search(message.text))
async def return_quote(message: types.ForceReply):
    quotation_number = int(findall('\d+', message.text)[0])
    try:
        await bot.forward_message(message.chat.id, message.chat.id, quotes[quotation_number][0])
    except:
        reply = quotes[quotation_number]
        await bot.send_message(message.chat.id, reply)


quotes = {}
last_quote = 0


def save(message_id, time, author, text):
    global last_quote
    quotes[last_quote] = [message_id, time, author, text]
    print(quotes[last_quote])
    last_quote += 1


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
