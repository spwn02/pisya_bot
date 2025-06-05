from utils import TeleBot, types, sqlite3, formatting, os, UserData
from commands.top import generate_leaderboards, format_leaderboards
DESCRIPTION: str = "Сбросить прогресс"
ADMIN: bool = True

def execute(client: TeleBot, message: types.Message, con: sqlite3.Connection):
    filename: str = f"./previous_top/{message.chat.id}.log"
    with open(filename, 'w', encoding = "utf-8") as file:
        file.write(str(generate_leaderboards(con, 'a', "dicks")))

    text: str = f"""
Предыдущий топ игроков:

{formatting.hcite(format_leaderboards(con, 'a', "dicks", False))}
"""

    file.close()

    client.send_document(message.chat.id, types.InputFile(filename), message.id, text, parse_mode="html")
    os.remove(filename)

    reset(message, con)

def reset(message: types.Message, con: sqlite3.Connection):
    con.cursor().execute("""DELETE FROM dicks WHERE groupid=?""", (message.chat.id,))
    con.commit()