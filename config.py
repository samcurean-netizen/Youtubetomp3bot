import os
from pathlib import Path

def get_env(key: str, default: str = None, required: bool = False) -> str:
    """Get environment variable with optional default and required validation."""
    value = os.environ.get(key, default)
    if required and not value:
        raise ValueError(f"{key} is required but not found in environment variables!")
    return value

BOT_TOKEN = get_env('BOT_TOKEN', required=True)
OPENAI_API_KEY = get_env('OPENAI_API_KEY', default='')
DATABASE_PATH = get_env('DATABASE_PATH', default='bot_data.db')
FLASK_HOST = get_env('FLASK_HOST', default='0.0.0.0')
FLASK_PORT = int(get_env('FLASK_PORT', default='8080'))
LOG_LEVEL = get_env('LOG_LEVEL', default='INFO')
DELETE_FILES_AFTER_SEND = get_env('DELETE_FILES_AFTER_SEND', default='true').lower() == 'true'
DOWNLOAD_DIR = get_env('DOWNLOAD_DIR', default='downloads')

Path(DOWNLOAD_DIR).mkdir(exist_ok=True)
