import logging
from re import compile, findall

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import API_TOKEN, GROUP_ID, DB_USER, DB_PASSWORD, BOT_USER_ID, DB_SCHEMA, SAVE_CONFIRMATION_STICKER, \
    REACTION_STRING, DB_HOST, MAMA_ID
from db_handle import Database, Quote

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Initialize database
db = Database(DB_HOST, DB_USER, DB_PASSWORD, DB_SCHEMA)


async def send_message(message, text):
    await bot.send_message(message.chat.id, text)


async def reply_message(message, text):
    await bot.send_message(message.chat.id, text, reply_to_message_id=message.reply_to_message.message_id)


async def send_sticker(message, sticker):
    await bot.send_sticker(message.chat.id, sticker)


async def forward_message(message, forward_id):
    await bot.forward_message(message.chat.id, message.chat.id, forward_id)


async def empty_message(quote, message):
    if message.reply_to_message:
        return True

    random_quote = quote.random()

    try:
        await forward_message(message, random_quote['message_id'])
    except:
        await send_message(message, convert_quote_to_text(random_quote))

    return False


async def reply_to_not_text(message):
    if message.reply_to_message.text:
        return True

    await reply_message(message, 'Только текст, только олдскул!')

    return False


async def reply_to_bot_message(message):
    if message.reply_to_message.from_user.id == BOT_USER_ID:
        await reply_message(message, 'Я стесняюсь')
        return False

    return True


async def reply_to_exist_message(quote, message):
    if quote.get_by_message_id(message.reply_to_message.message_id):
        await reply_message(message, 'Такое уже было')
        return False

    return True


# Save quote if reply, random quote otherwise
@dp.message_handler(
    lambda message: message.chat.id in GROUP_ID and compile(rf'^{REACTION_STRING}$').search(message.text))
async def main_quotes(message: types.ForceReply):
    quote = Quote(db)

    # !ц <empty>
    if not await empty_message(quote, message):
        return

    # !ц на не-текст
    if not await reply_to_not_text(message):
        return

    # !ц на сообщение бота
    if not await reply_to_bot_message(message):
        return

    # !ц на сообщение в базе
    if not await reply_to_exist_message(quote, message):
        return

    # message is totally cool, let's save it

    saved_id = quote.save(message.reply_to_message)

    await reply_message(message, f'Цитата номер {saved_id}')
    await send_sticker(message, SAVE_CONFIRMATION_STICKER)


# retrieve specific quote
@dp.message_handler(
    lambda message: message.chat.id in GROUP_ID and compile(rf'^{REACTION_STRING} \d+$').search(message.text))
async def return_quote(message: types.ForceReply):
    quote_id = findall('\d+', message.text)[0]
    quote = Quote(db).get_one(quote_id)

    if not quote:
        await send_message(message, "Не нашел :(")
        return

    try:
        await forward_message(message, quote['message_id'])
    except:
        await send_message(message, convert_quote_to_text(quote))


@dp.message_handler(
    lambda message: message.chat.id in GROUP_ID and compile(rf'^{REACTION_STRING}а$').search(message.text))
async def return_list(message: types.ForceReply):
    response = Quote(db).get_all()

    list = ''

    for quote in response:
        list += f"{quote['quote_id']} :: {quote['message_text']} \n"

    await send_message(message, list)


@dp.message_handler(
    lambda message: message.chat.id in GROUP_ID and message.from_user.id == MAMA_ID and compile(r'^удоли \d+$').search(
        message.text))
async def delete_quote(message: types.ForceReply):
    quote_id = findall('\d+', message.text)[0]

    if Quote(db).delete(quote_id):
        await send_message(message, 'Удолил!')


def convert_quote_to_text(quote):
    if not quote['from_username']:
        user = f"{quote['from_name']} {quote['from_lastname']}"
    else:
        user = f"@{quote['from_username']}"

    return f"{quote['message_date_time']} {user}: {quote['message_text']}"


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
