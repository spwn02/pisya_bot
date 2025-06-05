from utils import TeleBot, types, sqlite3, is_dm
from commands.top import format_leaderboards
DESCRIPTION = "Топ победителей битвы пиписичек"

def execute(client: TeleBot, message: types.Message, con: sqlite3.Connection):
    text: str = f"""
👑 Топ победителей:

{format_leaderboards(con, 'a' if is_dm(client, message) else message.chat.id, "score") or "Нет данных"}
"""
    client.send_message(message.chat.id, text, "html")