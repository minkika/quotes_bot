# quotes_bot
Easy bot to collect your memories in telegram

### Summary
Bot does not require any admin permissions in chat. You can add it as a member and this is enough. 
* Reply to message you want to save with a special message (see Configuration), and bot will save it in database.
* Send a special message without reply to retrieve a random quote from a database
* Send a special message with number of quote to retrieve it (for example '!c 15')
* Send a special message with 'a' at the end to get all your quotes in one list ('!ca')
* Send a special message to delete a quote ('!cd 15')
* Bot does not save messages without text (audio, stickers, etc.)
* Bot does not save messages from itself
* If the quoted message was deleted, bot will send it's text representation
* MySQL database

### Configuration
Create file 'config.py' at the same level with 'bot.py' with the following settings:
* API_TOKEN = Bot token (from @BotFather)
* GROUP_ID = List of group id where bot has to work
* DB_HOST = Database host
* DB_PASSWORD = Database password
* DB_USER = Database user
* DB_SCHEMA = Database schema
* SAVE_CONFIRMATION_STICKER = Row string with sticker id to be sent when message is successfully saved 
* REACTION_STRING = String to turn to bot
* MAMA_ID = User id with permission to delete quotes from database
* BOT_USER_ID = Your bot id (to exclude massages from itself)
* DELETION_STRING = String to delete a quote

Do not forget to create a db table with 'db_creation.sql'