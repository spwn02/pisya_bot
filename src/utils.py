from telebot import TeleBot, types, formatting
from types import ModuleType
import sqlite3, os, dotenv, importlib.util
dotenv.load_dotenv()

API_KEY: str = os.getenv("API_KEY") # type: ignore
ADMIN: int = 1294619981
YEHOR: int = 1298772455

UserData = tuple[int, int, int, str, str, str]
UserScoreData = tuple[int, int, int, str, str]

def import_module(filename: str, filepath: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(filename, filepath)
    module: ModuleType = importlib.util.module_from_spec(spec) # type: ignore
    spec.loader.exec_module(module) # type: ignore
    return module

def user_info(message: types.Message) -> tuple[types.User, int, str|None, str]:
    user: types.User|None = message.from_user
    return user, user.id, user.username, user.first_name # type: ignore

def is_dm(client: TeleBot, message: types.Message) -> bool:
    return message.chat.id == message.from_user.id # type: ignore
