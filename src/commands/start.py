from utils import TeleBot, types, sqlite3
DESCRIPTION = "Запуск бота"

def execute(client: TeleBot, message: types.Message, con: sqlite3.Connection):
    client.reply_to(message, "Пошёл нахуй")