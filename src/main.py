from utils import TeleBot, types, sqlite3, API_KEY, ADMIN, import_module
import glob

client: TeleBot = TeleBot(API_KEY)
con: sqlite3.Connection = sqlite3.connect("./dicks.db", check_same_thread=False)

commands: dict[str, dict[str, str|bool]] = {}

def set_commands() -> None:
    command_files: list[str] = glob.glob("./src/commands/*.py")
    client_commands: list[types.BotCommand] = []

    for command in command_files:
        command_name: str = command.split("\\")[-1][:-3]

        module = import_module(command_name, command)

        description: str = getattr(module, "DESCRIPTION", "Описание отсутствует")
        admin: bool = getattr(module, "ADMIN", False)

        client_commands.append(types.BotCommand(command_name, description))
        commands[command_name] = {"description": description, "admin": admin, "path": command}

    client.set_my_commands(client_commands)

@client.message_handler(func=lambda x: True)
def on_message(message: types.Message):
    if not message.text.startswith('/'): return # type: ignore
    command_name: str = message.text.split('/')[1].split('@')[0] # type: ignore
    if command_name in commands:
        command = commands[command_name]
        if command["admin"] and message.from_user.id != ADMIN: # type: ignore
            return client.reply_to(message, "У тебя нет прав, скотина 🖕")

        execute = getattr(import_module(command_name, command["path"]), "execute", None) # type: ignore
        if not execute: return client.reply_to(message, "Я это ещё не сделал, прости пожалуйста 🥹")
        execute(client, message, con)

if __name__ == "__main__":
    set_commands()

    cur: sqlite3.Cursor = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS dicks(uid INTEGER, groupid TEXT, length INTEGER, last_try TEXT, username TEXT, first_name TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS score(uid INTEGER, groupid TEXT, score INTEGER, username TEXT, first_name TEXT)""")
    con.commit()

    print(f"✅ | {client.user.first_name} launched up!")
    client.polling(True)