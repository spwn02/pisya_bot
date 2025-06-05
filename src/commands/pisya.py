from utils import TeleBot, types, sqlite3, user_info, is_dm, UserData, UserScoreData, formatting, YEHOR
from datetime import datetime
from commands.top import calculate_position, format_leaderboards
from commands.reset import reset
from random import choice

DESCRIPTION = "Вырастить писю"

def execute(client: TeleBot, message: types.Message, con: sqlite3.Connection) -> None:
    if is_dm(client, message):
        client.send_message(message.chat.id, "Долбоёб не в лс это юзай придурок ебанный дибил тупой. Ещё раз сюда напишешь пальцы <b>нахуй</b> отрублю!!!!", "html", reply_to_message_id = message.id)
        return

    user, uid, username, first_name = user_info(message)
    cur: sqlite3.Cursor = con.cursor()

    print(uid, message.chat.id)
    user_data: UserData|None = cur.execute("""SELECT * FROM dicks WHERE uid=? AND groupid=?""", (uid, message.chat.id,)).fetchone()
    con.commit()
    last_try: list[int] = [int(val) for val in user_data[3].split("/")] if user_data else [0,0]

    # Setting up variables
    today: datetime = datetime.now()
    today_format: str = f"{today.day}/{today.month}"
    score: int = calculate_position(con, message.chat.id, "dicks", user)

    # If user is in cooldown
    # if user_data and not ((today.day > last_try[0] and today.month == last_try[1]) or (today.month > last_try[1])): # type: ignore
    #     text: str = f"""
# @{username}, ты уже играл.
# Сейчас он равен <b>{user_data[1]}</b> см.
# Ты занимаешь <b>{score}</b> место в топе.
# Следующая попытка завтра!
    #     """
    #     return client.send_message(message.chat.id, text, "html") # type: ignore

    # If user is able to play
    if uid == YEHOR and not user_data:
        number: int = -2000
        new_length: int = -2000
    else:
        number: int = choice([val for val in range(-10, 20) if val != 0])
        new_length: int = user_data[2] + number if user_data else number # type: ignore
        if new_length < 0: new_length = 0

    if user_data:
        cur.execute("""UPDATE dicks SET groupid=?,length=?,last_try=?,username=?,first_name=? WHERE uid=?""", (message.chat.id, new_length, today_format, username, first_name, uid,))
    else:
        cur.execute("""INSERT INTO dicks VALUES (?,?,?,?,?,?)""", (uid, message.chat.id, new_length, today_format, username, first_name,))
    con.commit()

    if new_length > 100:
        return rebirth(client, message, con, new_length)

    score: int = calculate_position(con, message.chat.id, "dicks", user)

    text: str = f"""
{'@'+username if username else "<b>"+first_name+"</b>"}, твой писюн {"вырос" if number > 0 else "сократился"} на <b>{abs(number)}</b> см.
Теперь он равен <b>{new_length}</b> см.
Ты занимаешь <b>{score}</b> место в топе
Следующая попытка завтра!
    """

    client.send_message(message.chat.id, text, "html")

def rebirth(client: TeleBot, message: types.Message, con: sqlite3.Connection, length: int) -> None:
    cur: sqlite3.Cursor = con.cursor()
    user, uid, username, first_name = user_info(message)

    user_data: UserScoreData|None = cur.execute("""SELECT * FROM score WHERE uid=? AND groupid=?""", (uid, message.chat.id,)).fetchone()
    current_score: int = user_data[2]+1 if user_data else 1

    text: str = f"""
👑 Поздравляем {'@'+username if username else "<b>"+first_name+"</b>"}, твой писюн достиг отметки в <b>{length}</b> см!

Ты получаешь <b>1</b> очко. Теперь твой счёт побед: <b>{current_score}</b>

Весь предыдущий топ:
{formatting.hcite(format_leaderboards(con, message.chat.id, "dicks", False))}
    """

    if user_data:
        cur.execute("""UPDATE score SET score=?,username=?,first_name=? WHERE uid=? AND groupid=?""", (current_score, username, first_name, uid, message.chat.id))
    else:
        cur.execute("""INSERT INTO score VALUES (?,?,?,?,?)""", (uid, message.chat.id, current_score, username, first_name))

    client.send_message(message.chat.id, text, "html")

    reset(message, con)