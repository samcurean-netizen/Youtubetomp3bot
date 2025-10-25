"""Transcription API wrapper for speech-to-text services."""
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import asyncio

from config import get_openai_api_key

logger = logging.getLogger(__name__)


class TranscriptionError(Exception):
    """Base exception for transcription errors."""
    pass


class APIKeyMissingError(TranscriptionError):
    """Raised when API key is not configured."""
    pass


class UnsupportedFormatError(TranscriptionError):
    """Raised when audio format is not supported."""
    pass


class TranscriptionTimeoutError(TranscriptionError):
    """Raised when transcription request times out."""
    pass


class TranscriptionAPIError(TranscriptionError):
    """Raised when API returns an error."""
    pass


class TranscriptionResult:
    """Container for transcription results."""
    
    def __init__(self, text: str, metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize transcription result.
        
        Args:
            text: Transcribed text
            metadata: Additional metadata (language, duration, etc.)
        """
        self.text = text
        self.metadata = metadata or {}
    
    def __str__(self) -> str:
        return self.text
    
    def __repr__(self) -> str:
        return f"TranscriptionResult(text={self.text!r}, metadata={self.metadata!r})"


SUPPORTED_FORMATS = {'.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.wav', '.webm'}
MOCK_TRANSCRIPTION = "This is a mock transcription. OpenAI API key not configured."


async def transcribe_audio(
    audio_file_path: str,
    language: Optional[str] = None,
    timeout: int = 300,
    use_mock: Optional[bool] = None
) -> TranscriptionResult:
    """
    Transcribe audio file using OpenAI Whisper API.
    
    Args:
        audio_file_path: Path to audio file on disk
        language: Optional ISO-639-1 language code (e.g., 'en', 'es', 'fr')
        timeout: Timeout in seconds for API request (default: 300)
        use_mock: Force mock mode. If None, auto-detect based on API key presence
        
    Returns:
        TranscriptionResult containing transcribed text and metadata
        
    Raises:
        FileNotFoundError: If audio file doesn't exist
        UnsupportedFormatError: If audio format is not supported
        TranscriptionTimeoutError: If request times out
        TranscriptionAPIError: If API returns an error
        APIKeyMissingError: If API key is missing and mock mode is disabled
    """
    audio_path = Path(audio_file_path)
    
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
    
    if audio_path.suffix.lower() not in SUPPORTED_FORMATS:
        raise UnsupportedFormatError(
            f"Unsupported audio format: {audio_path.suffix}. "
            f"Supported formats: {', '.join(SUPPORTED_FORMATS)}"
        )
    
    api_key = get_openai_api_key()
    
    if use_mock is None:
        use_mock = api_key is None
    
    if use_mock:
        logger.info(f"Using mock transcription for: {audio_file_path}")
        return await _mock_transcribe(audio_path, language)
    
    if not api_key:
        raise APIKeyMissingError(
            "OpenAI API key not configured. Set OPENAI_API_KEY environment variable "
            "or enable mock mode for development."
        )
    
    return await _transcribe_with_openai(audio_path, api_key, language, timeout)


async def _mock_transcribe(
    audio_path: Path,
    language: Optional[str] = None
) -> TranscriptionResult:
    """
    Mock transcription for development when API key is not available.
    
    Args:
        audio_path: Path to audio file
        language: Optional language hint
        
    Returns:
        TranscriptionResult with mock data
    """
    await asyncio.sleep(0.5)
    
    metadata = {
        'mock': True,
        'file_name': audio_path.name,
        'file_size': audio_path.stat().st_size,
        'language': language or 'en',
    }
    
    return TranscriptionResult(
        text=MOCK_TRANSCRIPTION,
        metadata=metadata
    )


async def _transcribe_with_openai(
    audio_path: Path,
    api_key: str,
    language: Optional[str] = None,
    timeout: int = 300
) -> TranscriptionResult:
    """
    Transcribe audio using OpenAI Whisper API.
    
    Args:
        audio_path: Path to audio file
        api_key: OpenAI API key
        language: Optional language hint
        timeout: Request timeout in seconds
        
    Returns:
        TranscriptionResult with transcribed text and metadata
        
    Raises:
        TranscriptionTimeoutError: If request times out
        TranscriptionAPIError: If API returns an error
    """
    try:
        from openai import AsyncOpenAI
        from openai import APIError, APITimeoutError, RateLimitError
    except ImportError:
        raise TranscriptionAPIError(
            "OpenAI package not installed. Install with: pip install openai"
        )
    
    client = AsyncOpenAI(api_key=api_key)
    
    try:
        logger.info(f"Transcribing audio file: {audio_path.name}")
        
        with open(audio_path, 'rb') as audio_file:
            kwargs = {
                'model': 'whisper-1',
                'file': audio_file,
                'response_format': 'verbose_json',
                'timeout': timeout,
            }
            
            if language:
                kwargs['language'] = language
            
            response = await asyncio.wait_for(
                client.audio.transcriptions.create(**kwargs),
                timeout=timeout
            )
        
        metadata = {
            'language': getattr(response, 'language', language),
            'duration': getattr(response, 'duration', None),
            'file_name': audio_path.name,
            'file_size': audio_path.stat().st_size,
        }
        
        if hasattr(response, 'segments'):
            metadata['segments'] = response.segments
        
        logger.info(f"Transcription completed for: {audio_path.name}")
        
        return TranscriptionResult(
            text=response.text,
            metadata=metadata
        )
        
    except asyncio.TimeoutError:
        raise TranscriptionTimeoutError(
            f"Transcription request timed out after {timeout} seconds"
        )
    
    except APITimeoutError:
        raise TranscriptionTimeoutError(
            f"OpenAI API request timed out after {timeout} seconds"
        )
    
    except RateLimitError as e:
        raise TranscriptionAPIError(
            f"OpenAI API rate limit exceeded: {str(e)}"
        )
    
    except APIError as e:
        raise TranscriptionAPIError(
            f"OpenAI API error: {str(e)}"
        )
    
    except Exception as e:
        logger.error(f"Unexpected error during transcription: {e}", exc_info=True)
        raise TranscriptionAPIError(
            f"Unexpected error during transcription: {str(e)}"
        )


def is_api_configured() -> bool:
    """
    Check if OpenAI API is properly configured.
    
    Returns:
        True if API key is available, False otherwise
    """
    return get_openai_api_key() is not None


async def transcribe_audio_safe(
    audio_file_path: str,
    language: Optional[str] = None,
    timeout: int = 300
) -> Optional[TranscriptionResult]:
    """
    Safely transcribe audio file with automatic fallback to mock mode.
    
    This is a convenience wrapper that catches all exceptions and returns None
    on failure, while logging errors. Automatically uses mock mode if API key
    is not configured.
    
    Args:
        audio_file_path: Path to audio file on disk
        language: Optional ISO-639-1 language code
        timeout: Timeout in seconds for API request
        
    Returns:
        TranscriptionResult on success, None on failure
    """
    try:
        return await transcribe_audio(
            audio_file_path,
            language=language,
            timeout=timeout
        )
    except Exception as e:
        logger.error(f"Transcription failed for {audio_file_path}: {e}")
        return None
