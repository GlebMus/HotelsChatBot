from loguru import logger
from decouple import config

TOKEN = config('BOT_TOKEN')
HEAD = config('HEAD')
logger.add('debug.log', format="{time} {level} {message}", level='DEBUG', rotation='10 MB',
           compression='zip')