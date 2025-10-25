"""Configuration helpers for loading environment variables."""
import os
from typing import Optional


def get_env_var(key: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    """
    Get environment variable with optional default and required check.
    
    Args:
        key: Environment variable name
        default: Default value if not found
        required: If True, raises ValueError when variable is not found
        
    Returns:
        Environment variable value or default
        
    Raises:
        ValueError: If required is True and variable is not found
    """
    value = os.environ.get(key, default)
    
    if required and value is None:
        raise ValueError(f"{key} not found in environment variables!")
    
    return value


def get_openai_api_key() -> Optional[str]:
    """Get OpenAI API key from environment variables."""
    return get_env_var('OPENAI_API_KEY')


def get_bot_token() -> str:
    """Get Telegram bot token from environment variables."""
    return get_env_var('BOT_TOKEN', required=True)
