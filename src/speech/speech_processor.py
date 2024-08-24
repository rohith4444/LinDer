import os
import io
import wave
import pyaudio
import pygame
from datetime import datetime
from google.cloud import speech, texttospeech
from pydub import AudioSegment

from text.text_processor import process_text, translate_large_text
from utils.common import read_file, write_file, generate_unique_filename, split_content, check_audio_duration, check_text_size
from logging_config import get_module_logger
from config.settings import (
    AUDIO_SAMPLE_RATE, DEFAULT_AUDIO_DURATION, AUDIO_OUTPUT_DIR,
    GOOGLE_APPLICATION_CREDENTIALS
)

# Get logger for this module
logger = get_module_logger(__name__)

# Initialize Google Cloud clients
speech_client = speech.SpeechClient()
tts_client = texttospeech.TextToSpeechClient()

# Set Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_APPLICATION_CREDENTIALS

def process_audio(audio_content, operation, **kwargs):
    """
    Processes audio content based on the specified operation.
    
    :param audio_content: The audio content to process (bytes or file path)
    :param operation: The operation to perform ('transcribe', 'translate', or 'text_to_speech')
    :param kwargs: Additional keyword arguments for specific operations
    :return: Processed audio content or text, depending on the operation
    """
    logger.info(f"Processing audio with operation: {operation}")
    try:
        # Check if audio_content is a file path or bytes
        if isinstance(audio_content, str):
            is_large = check_audio_duration(audio_content)
        else:
            is_large = len(audio_content) > 10 * 1024 * 1024  # Consider audio large if it's more than 10MB

        if operation == 'transcribe':
            if is_large:
                return transcribe_large_audio(audio_content, kwargs['language_code'])
            else:
                return transcribe_audio(audio_content, kwargs['language_code'])
        elif operation == 'translate':
            if is_large:
                transcribed_text = transcribe_large_audio(audio_content, kwargs['source_lang'])
            else:
                transcribed_text = transcribe_audio(audio_content, kwargs['source_lang'])
            return process_text(transcribed_text, 'translate', source_lang=kwargs['source_lang'], target_lang=kwargs['target_lang'])
        elif operation == 'text_to_speech':
            text = kwargs['text']
            if check_text_size(text):
                return text_to_speech_large(text, kwargs['language_code'], kwargs['voice_gender'])
            else:
                return text_to_speech(text, kwargs['language_code'], kwargs['voice_gender'])
        else:
            logger.error(f"Unsupported operation: {operation}")
            return None
    except Exception as e:
        logger.exception(f"An error occurred during audio processing: {str(e)}")
        return None
    
def process_audio_file(input_file, output_file, operation, **kwargs):
    """
    Processes an audio file based on the specified operation.
    
    :param input_file: Path to the input audio file
    :param output_file: Path to save the processed audio file
    :param operation: The operation to perform ('transcribe', 'translate', or 'text_to_speech')
    :param kwargs: Additional keyword arguments for specific operations
    :return: Path to the processed file or None if processing fails
    """
    logger.info(f"Processing audio file. Input: {input_file}, Output: {output_file}, Operation: {operation}")
    try:
        
        if operation in ['transcribe', 'translate']:
            processed_content = process_audio(input_file, operation, **kwargs)
            if processed_content:
                write_file(processed_content, output_file)
                logger.info(f"Processed content saved to: {output_file}")
                return output_file
            else:
                logger.error("Processing failed, no content to write")
                return None
        elif operation == 'text_to_speech':
            audio_content = process_audio(kwargs['text'], operation, **kwargs)
            if audio_content:
                save_audio(audio_content, os.path.splitext(output_file)[0], use_unique_name=False)
                logger.info(f"Processed content saved to: {output_file}")
                return output_file
            else:
                logger.error("Processing failed, no content to write")
                return None
        else:
            logger.error(f"Unsupported operation: {operation}")
            return None
    except Exception as e:
        logger.exception(f"An error occurred during audio file processing: {str(e)}")
        return None

def record_audio(duration=DEFAULT_AUDIO_DURATION, sample_rate=AUDIO_SAMPLE_RATE):
    """
    Records audio from the microphone and saves it to a file in the data folder.
    
    :param duration: The duration of the recording in seconds (default: DEFAULT_AUDIO_DURATION)
    :param sample_rate: The sample rate of the audio (default: AUDIO_SAMPLE_RATE)
    :return: The path of the saved audio file or None if an error occurred
    """
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1

    filename = generate_unique_filename("recorded_audio", ".wav")
    full_path = os.path.join(AUDIO_OUTPUT_DIR, filename)

    logger.info(f"Starting audio recording. Duration: {duration}s, Sample rate: {sample_rate}Hz")
    try:
        p = pyaudio.PyAudio()
        os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)
        logger.info(f"Recording for {duration} seconds...")

        stream = p.open(format=FORMAT, channels=CHANNELS, rate=sample_rate, input=True, frames_per_buffer=CHUNK)
        frames = []

        for _ in range(0, int(sample_rate / CHUNK * duration)):
            try:
                data = stream.read(CHUNK)
                frames.append(data)
            except IOError as e:
                logger.warning(f"Dropped frame due to I/O error: {e}")

        logger.info("Recording finished.")
        stream.stop_stream()
        stream.close()
        p.terminate()

        with wave.open(full_path, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))
        logger.info(f"Audio saved as: {full_path}")
        return full_path

    except Exception as e:
        logger.exception(f"An error occurred during audio recording: {e}")
        return None

def transcribe_audio(audio_file, language_code):
    """
    Transcribes audio to text using Google Cloud Speech-to-Text API.
    
    :param audio_file: The path to the audio file
    :param language_code: The language code of the audio
    :return: The transcribed text
    """
    logger.info(f"Starting audio transcription. File: {audio_file}, Language: {language_code}")
    try:
        with io.open(audio_file, "rb") as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MP3,
            sample_rate_hertz=AUDIO_SAMPLE_RATE,
            language_code=language_code,
        )

        response = speech_client.recognize(config=config, audio=audio)

        transcribed_text = ""
        for result in response.results:
            transcribed_text += result.alternatives[0].transcript + " "

        if transcribed_text:
            logger.info("Audio transcription completed successfully")
            return transcribed_text.strip()
        else:
            logger.warning("No transcription results returned")
            return ""

    except Exception as e:
        logger.exception(f"Error during audio transcription: {str(e)}")
        return ""

def transcribe_large_audio(audio_file, language_code):
    """
    Transcribes a large audio file to text using Google Cloud Speech-to-Text API with long-running recognition.
    
    :param audio_file: The path to the audio file
    :param language_code: The language code of the audio
    :return: The transcribed text
    """
    logger.info(f"Starting large audio transcription. File: {audio_file}, Language: {language_code}")
    client = speech.SpeechClient()
    
    with io.open(audio_file, "rb") as audio_file:
        content = audio_file.read()
    
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=AUDIO_SAMPLE_RATE,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    logger.info("Waiting for operation to complete...")
    response = operation.result(timeout=None)  # Set timeout to None for very large files

    transcription = ""
    for result in response.results:
        transcription += result.alternatives[0].transcript + " "

    logger.info("Large audio transcription completed successfully")
    return transcription.strip()

def text_to_speech(text, language_code, voice_gender):
    """
    Converts text to speech using Google Cloud Text-to-Speech API.
    
    :param text: The text to convert to speech
    :param language_code: The language code for the text
    :param voice_gender: The gender of the voice to use
    :return: Audio content or None if conversion fails
    """
    logger.info(f"Starting text-to-speech conversion. Language: {language_code}, Voice gender: {voice_gender}")
    try:
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(language_code=language_code, ssml_gender=voice_gender)
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

        response = tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        logger.info("Text-to-speech conversion completed successfully")
        return response.audio_content
    except Exception as e:
        logger.exception(f"An error occurred during text-to-speech conversion: {str(e)}")
        return None

def text_to_speech_large(text, language_code, voice_gender, chunk_size=3500):
    """
    Converts large text to speech using Google Cloud Text-to-Speech API by splitting it into chunks.
    
    :param text: The text to convert to speech
    :param language_code: The language code for the text
    :param voice_gender: The gender of the voice to use
    :param chunk_size: The maximum size of each chunk
    :return: List of audio contents or None if conversion fails
    """
    logger.info(f"Starting large text-to-speech conversion. Language: {language_code}, Voice gender: {voice_gender}")
    chunks = split_content(text, chunk_size)
    audio_contents = []

    for i, chunk in enumerate(chunks):
        logger.info(f"Converting chunk {i+1}/{len(chunks)} to speech")
        if check_text_size(chunk):
            logger.warning(f"Chunk {i+1} is still too large, splitting further")
            sub_chunks = split_content(chunk, chunk_size // 2)
            for j, sub_chunk in enumerate(sub_chunks):
                audio_content = text_to_speech(sub_chunk, language_code, voice_gender)
                if audio_content:
                    audio_contents.append(audio_content)
                else:
                    logger.error(f"Failed to convert sub-chunk {j+1} of chunk {i+1} to speech")
        else:
            audio_content = text_to_speech(chunk, language_code, voice_gender)
            if audio_content:
                audio_contents.append(audio_content)
            else:
                logger.error(f"Failed to convert chunk {i+1} to speech")

    if len(audio_contents) == sum(len(split_content(chunk, chunk_size // 2)) if check_text_size(chunk) else 1 for chunk in chunks):
        logger.info("Large text-to-speech conversion completed successfully")
        return audio_contents
    else:
        logger.error("Large text-to-speech conversion failed")
        return None

def play_audio(audio_input):
    """
    Plays the audio content using pygame.
    
    :param audio_input: Either a file path (str) or audio content (bytes)
    """
    logger.info("Starting audio playback")
    try:
        pygame.mixer.init()
        
        if isinstance(audio_input, str):
            if not os.path.exists(audio_input):
                logger.error(f"Audio file not found: {audio_input}")
                raise FileNotFoundError(f"Audio file not found: {audio_input}")
            pygame.mixer.music.load(audio_input)
            logger.info(f"Loaded audio file: {audio_input}")
        elif isinstance(audio_input, bytes):
            audio_bytes = io.BytesIO(audio_input)
            pygame.mixer.music.load(audio_bytes)
            logger.info("Loaded audio content from bytes")
        else:
            logger.error("Invalid audio input type")
            raise ValueError("Invalid audio input type. Expected str (file path) or bytes (audio content).")
        
        pygame.mixer.music.play()
        logger.info("Audio playback started")
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        logger.info("Audio playback completed")
    except Exception as e:
        logger.exception(f"An error occurred during audio playback: {str(e)}")
    finally:
        pygame.mixer.quit()
        logger.info("Audio playback resources released")

def save_audio(audio_content, base_filename="output", use_unique_name=True):
    """
    Saves the audio content to a file in the data folder.
    
    :param audio_content: The audio content to save
    :param base_filename: The base name for the file (default: "output")
    :param use_unique_name: Whether to generate a unique filename (default: True)
    :return: The full path of the saved file or None if an error occurred
    """
    logger.info(f"Saving audio content. Base filename: {base_filename}")
    try:
        os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)
        if use_unique_name:
            filename = generate_unique_filename(base_filename, ".mp3")
        else:
            filename = f"{base_filename}.mp3"
        full_path = os.path.join(AUDIO_OUTPUT_DIR, filename)
        
        with open(full_path, 'wb') as file:
            file.write(audio_content)
        logger.info(f'Audio content written to file: "{full_path}"')
        return full_path
    except Exception as e:
        logger.exception(f"An error occurred while saving the audio: {str(e)}")
        return None

def save_large_audio(audio_contents, base_filename="output", use_unique_name=True):
    """
    Saves large audio content (multiple chunks) to a file in the data folder.
    
    :param audio_contents: List of audio contents to save
    :param base_filename: The base name for the file (default: "output")
    :param use_unique_name: Whether to generate a unique filename (default: True)
    :return: The full path of the saved file or None if an error occurred
    """
    logger.info(f"Saving large audio content. Base filename: {base_filename}")
    try:
        os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)
        if use_unique_name:
            filename = generate_unique_filename(base_filename, ".mp3")
        else:
            filename = f"{base_filename}.mp3"
        full_path = os.path.join(AUDIO_OUTPUT_DIR, filename)
        
        combined = AudioSegment.empty()
        for audio_content in audio_contents:
            segment = AudioSegment.from_mp3(io.BytesIO(audio_content))
            combined += segment

        combined.export(full_path, format="mp3")
        logger.info(f'Large audio content written to file: "{full_path}"')
        return full_path
    except Exception as e:
        logger.exception(f"An error occurred while saving the large audio: {str(e)}")
        return None
