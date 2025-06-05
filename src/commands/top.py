from utils import TeleBot, types, sqlite3, UserData, formatting, is_dm
DESCRIPTION = "Топ писичек"

def execute(client: TeleBot, message: types.Message, con: sqlite3.Connection):
    text: str = f"""
💎 Топ писичек:

{format_leaderboards(con, 'a' if is_dm(client, message) else message.chat.id, "dicks") or "Нет данных"}
"""
    client.send_message(message.chat.id, text, "html")

def generate_leaderboards(con: sqlite3.Connection, groupid: int|str, db: str) -> list[UserData]:
    leaderboards: list[UserData] = (con.cursor().execute(
        f"""SELECT * FROM {db} {"WHERE groupid=?" if groupid != 'a' else ""} ORDER BY {"length" if db == "dicks" else "score"} DESC""",
        (groupid,) if groupid != 'a' else ()).fetchall()
    )
    con.commit()
    return leaderboards

def format_leaderboards(con: sqlite3.Connection, groupid: int|str, db: str, format: bool = True) -> str:
    leaderboards: list[UserData] = generate_leaderboards(con, groupid, db)
    return "\n".join(
        f"{leaderboards.index(user)+1}|{formatting.hbold(user[5] if db == "dicks" else user[4]) if format else user[5] if db == "dicks" else user[4]} — {formatting.hbold(str(user[2])) if format else user[2]} {"см" if db == "dicks" else ("очко" if user[2] == 1 else ("очка" if user[2] < 5 else "очков"))}." for user in leaderboards
    )

def calculate_position(con: sqlite3.Connection, groupid: int, db: str, user: types.User) -> int:
    leaderboards: list[UserData] = generate_leaderboards(con, groupid, db)
    for item in leaderboards:
        if item[4] == user.username or item[5] == user.first_name:
            return leaderboards.index(item)+1
    return 1