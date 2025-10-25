"""Unit tests for transcription module."""
import asyncio
import tempfile
from pathlib import Path

from transcription import (
    transcribe_audio,
    transcribe_audio_safe,
    is_api_configured,
    TranscriptionResult,
    TranscriptionError,
    APIKeyMissingError,
    UnsupportedFormatError,
    TranscriptionTimeoutError,
    MOCK_TRANSCRIPTION,
)

try:
    import pytest
    HAS_PYTEST = True
except ImportError:
    HAS_PYTEST = False


def create_temp_audio_file(suffix: str = '.mp3') -> Path:
    """Create a temporary audio file for testing."""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp_file.write(b'fake audio content')
    temp_file.close()
    return Path(temp_file.name)


async def test_transcribe_with_mock():
    """Test transcription in mock mode."""
    audio_file = create_temp_audio_file()
    
    try:
        result = await transcribe_audio(str(audio_file), use_mock=True)
        
        assert isinstance(result, TranscriptionResult)
        assert result.text == MOCK_TRANSCRIPTION
        assert result.metadata['mock'] is True
        assert result.metadata['file_name'] == audio_file.name
        assert 'file_size' in result.metadata
        
    finally:
        audio_file.unlink()


async def test_transcribe_with_language_hint():
    """Test transcription with language hint in mock mode."""
    audio_file = create_temp_audio_file()
    
    try:
        result = await transcribe_audio(str(audio_file), language='es', use_mock=True)
        
        assert result.metadata['language'] == 'es'
        
    finally:
        audio_file.unlink()


async def test_transcribe_nonexistent_file():
    """Test transcription with nonexistent file."""
    try:
        await transcribe_audio('/nonexistent/file.mp3', use_mock=True)
        assert False, "Should have raised FileNotFoundError"
    except FileNotFoundError:
        pass


async def test_transcribe_unsupported_format():
    """Test transcription with unsupported format."""
    audio_file = create_temp_audio_file(suffix='.txt')
    
    try:
        try:
            await transcribe_audio(str(audio_file), use_mock=True)
            assert False, "Should have raised UnsupportedFormatError"
        except UnsupportedFormatError as e:
            assert 'Unsupported audio format' in str(e)
        
    finally:
        audio_file.unlink()


async def test_transcribe_safe():
    """Test safe transcription that doesn't raise exceptions."""
    audio_file = create_temp_audio_file()
    
    try:
        result = await transcribe_audio_safe(str(audio_file))
        
        assert result is not None
        assert isinstance(result, TranscriptionResult)
        
    finally:
        audio_file.unlink()


async def test_transcribe_safe_with_invalid_file():
    """Test safe transcription with invalid file returns None."""
    result = await transcribe_audio_safe('/nonexistent/file.mp3')
    assert result is None


async def test_transcription_result_str():
    """Test TranscriptionResult string representation."""
    result = TranscriptionResult("Hello world", {'language': 'en'})
    
    assert str(result) == "Hello world"
    assert 'Hello world' in repr(result)
    assert 'language' in repr(result)


def test_is_api_configured():
    """Test API configuration check."""
    configured = is_api_configured()
    assert isinstance(configured, bool)


async def test_supported_formats():
    """Test that all supported formats work in mock mode."""
    formats = ['.mp3', '.mp4', '.wav', '.m4a', '.webm']
    
    for fmt in formats:
        audio_file = create_temp_audio_file(suffix=fmt)
        
        try:
            result = await transcribe_audio(str(audio_file), use_mock=True)
            assert result is not None
        finally:
            audio_file.unlink()


if __name__ == '__main__':
    print("Running transcription tests...")
    
    asyncio.run(test_transcribe_with_mock())
    print("✓ test_transcribe_with_mock")
    
    asyncio.run(test_transcribe_with_language_hint())
    print("✓ test_transcribe_with_language_hint")
    
    asyncio.run(test_transcribe_safe())
    print("✓ test_transcribe_safe")
    
    asyncio.run(test_transcribe_safe_with_invalid_file())
    print("✓ test_transcribe_safe_with_invalid_file")
    
    test_is_api_configured()
    print("✓ test_is_api_configured")
    
    asyncio.run(test_supported_formats())
    print("✓ test_supported_formats")
    
    asyncio.run(test_transcription_result_str())
    print("✓ test_transcription_result_str")
    
    print("\nAll tests passed! ✓")
