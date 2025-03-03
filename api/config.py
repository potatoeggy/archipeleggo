from dotenv import load_dotenv

load_dotenv()

from .utils import getenv_or, getenv_or_raise

# general
CONFIG_PORT = int(getenv_or("PORT", "8000"))

# island: music
CONFIG_ISLAND_MUSIC_CACHE_PATH = getenv_or_raise("ISLAND_MUSIC_CACHE_PATH")
