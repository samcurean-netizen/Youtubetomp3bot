"""Transcription module using faster-whisper for local speech-to-text."""
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import asyncio

logger = logging.getLogger(__name__)


class TranscriptionError(Exception):
    """Base exception for transcription errors."""
    pass


class UnsupportedFormatError(TranscriptionError):
    """Raised when audio format is not supported."""
    pass


class TranscriptionTimeoutError(TranscriptionError):
    """Raised when transcription request times out."""
    pass


class ModelLoadError(TranscriptionError):
    """Raised when model fails to load."""
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


SUPPORTED_FORMATS = {'.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.wav', '.webm', '.ogg', '.oga'}

_model = None
_model_lock = asyncio.Lock()


async def _get_model():
    """
    Get or initialize the faster-whisper model (singleton pattern).
    
    Returns:
        WhisperModel instance
        
    Raises:
        ModelLoadError: If model fails to load
    """
    global _model
    
    async with _model_lock:
        if _model is None:
            try:
                from faster_whisper import WhisperModel
                
                logger.info("Loading faster-whisper model (base)...")
                loop = asyncio.get_event_loop()
                _model = await loop.run_in_executor(
                    None,
                    lambda: WhisperModel(
                        "base",
                        device="cpu",
                        compute_type="int8"
                    )
                )
                logger.info("Faster-whisper model loaded successfully")
            except ImportError:
                raise ModelLoadError(
                    "faster-whisper package not installed. Install with: pip install faster-whisper"
                )
            except Exception as e:
                logger.error(f"Failed to load faster-whisper model: {e}", exc_info=True)
                raise ModelLoadError(f"Failed to load faster-whisper model: {str(e)}")
        
        return _model


async def transcribe_audio(
    audio_file_path: str,
    language: Optional[str] = None,
    timeout: int = 300
) -> TranscriptionResult:
    """
    Transcribe audio file using local faster-whisper model.
    
    Args:
        audio_file_path: Path to audio file on disk
        language: Optional ISO-639-1 language code (e.g., 'en', 'es', 'fr')
        timeout: Timeout in seconds for transcription (default: 300)
        
    Returns:
        TranscriptionResult containing transcribed text and metadata
        
    Raises:
        FileNotFoundError: If audio file doesn't exist
        UnsupportedFormatError: If audio format is not supported
        TranscriptionTimeoutError: If transcription times out
        ModelLoadError: If model fails to load
        TranscriptionError: For other transcription errors
    """
    audio_path = Path(audio_file_path)
    
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
    
    if audio_path.suffix.lower() not in SUPPORTED_FORMATS:
        raise UnsupportedFormatError(
            f"Unsupported audio format: {audio_path.suffix}. "
            f"Supported formats: {', '.join(SUPPORTED_FORMATS)}"
        )
    
    try:
        model = await _get_model()
        
        logger.info(f"Transcribing audio file: {audio_path.name}")
        
        loop = asyncio.get_event_loop()
        
        transcribe_kwargs = {
            'beam_size': 5,
            'best_of': 5,
            'temperature': 0.0,
        }
        
        if language:
            transcribe_kwargs['language'] = language
        
        segments_generator, info = await asyncio.wait_for(
            loop.run_in_executor(
                None,
                lambda: model.transcribe(str(audio_path), **transcribe_kwargs)
            ),
            timeout=timeout
        )
        
        segments = list(segments_generator)
        
        text = " ".join(segment.text.strip() for segment in segments)
        
        metadata = {
            'language': info.language,
            'language_probability': info.language_probability,
            'duration': info.duration,
            'file_name': audio_path.name,
            'file_size': audio_path.stat().st_size,
            'segments_count': len(segments),
        }
        
        logger.info(f"Transcription completed for: {audio_path.name} (language: {info.language})")
        
        return TranscriptionResult(
            text=text,
            metadata=metadata
        )
        
    except asyncio.TimeoutError:
        raise TranscriptionTimeoutError(
            f"Transcription timed out after {timeout} seconds"
        )
    
    except (ModelLoadError, FileNotFoundError, UnsupportedFormatError):
        raise
    
    except Exception as e:
        logger.error(f"Unexpected error during transcription: {e}", exc_info=True)
        raise TranscriptionError(
            f"Unexpected error during transcription: {str(e)}"
        )


async def transcribe_audio_safe(
    audio_file_path: str,
    language: Optional[str] = None,
    timeout: int = 300
) -> Optional[TranscriptionResult]:
    """
    Safely transcribe audio file with error handling.
    
    This is a convenience wrapper that catches all exceptions and returns None
    on failure, while logging errors.
    
    Args:
        audio_file_path: Path to audio file on disk
        language: Optional ISO-639-1 language code
        timeout: Timeout in seconds for transcription
        
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
