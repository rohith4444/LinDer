import os
import io
import wave
import pyaudio
import pygame
from datetime import datetime
from google.cloud import speech, texttospeech
from pydub import AudioSegment

from text.text_processor import process_text
from utils.common import read_file, write_file, generate_unique_filename
from logging_config import get_module_logger

# Get logger for this module
logger = get_module_logger(__name__)

# Initialize Google Cloud clients
speech_client = speech.SpeechClient()
tts_client = texttospeech.TextToSpeechClient()

# Global variable for data directory
DATA_DIR = None

def set_data_dir(path):
    """
    Set the global DATA_DIR variable.

    This function should be called before using any functions that rely on DATA_DIR.

    :param path: The path to the data directory
    """
    global DATA_DIR
    DATA_DIR = path
    logger.info(f"Data directory set to: {DATA_DIR}")

def record_audio(duration=5, sample_rate=16000):
    """
    Records audio from the microphone and saves it to a file in the data folder.
    
    :param duration: The duration of the recording in seconds (default: 5)
    :param sample_rate: The sample rate of the audio (default: 16000)
    :return: The path of the saved audio file or None if an error occurred
    :raises ValueError: If DATA_DIR is not set
    """
    if DATA_DIR is None:
        logger.error("DATA_DIR is not set. Call set_data_dir() first.")
        raise ValueError("DATA_DIR is not set. Call set_data_dir() first.")
    
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1

    filename = generate_unique_filename("recorded_audio", ".wav")
    full_path = os.path.join(DATA_DIR, filename)

    logger.info(f"Starting audio recording. Duration: {duration}s, Sample rate: {sample_rate}Hz")
    try:
        p = pyaudio.PyAudio()
        os.makedirs(DATA_DIR, exist_ok=True)
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
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code=language_code,
        )

        response = speech_client.recognize(config=config, audio=audio)

        for result in response.results:
            transcribed_text = result.alternatives[0].transcript
            logger.info("Audio transcription completed successfully")
            return transcribed_text

        logger.warning("No transcription results returned")
        return ""

    except Exception as e:
        logger.exception(f"Error during audio transcription: {e}")
        return ""

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

def save_audio(audio_content, base_filename="output"):
    """
    Saves the audio content to a file in the data folder with a unique filename.
    
    :param audio_content: The audio content to save
    :param base_filename: The base name for the file (default: "output")
    :return: The full path of the saved file or None if an error occurred
    """
    logger.info(f"Saving audio content. Base filename: {base_filename}")
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        filename = generate_unique_filename(base_filename, ".mp3")
        full_path = os.path.join(DATA_DIR, filename)
        
        write_file(audio_content, full_path)
        logger.info(f'Audio content written to file: "{full_path}"')
        return full_path
    except Exception as e:
        logger.exception(f"An error occurred while saving the audio: {str(e)}")
        return None

def generate_audio_book(input_file, output_file, source_lang, target_lang, voice_gender):
    """
    Generates an audio book from a text file, with optional translation.
    
    :param input_file: Path to the input text file
    :param output_file: Path to save the output audio file
    :param source_lang: Source language code
    :param target_lang: Target language code
    :param voice_gender: Gender of the voice for text-to-speech
    :return: Path to the generated audio file
    """
    logger.info(f"Starting audio book generation. Input: {input_file}, Output: {output_file}")
    logger.info(f"Source language: {source_lang}, Target language: {target_lang}, Voice gender: {voice_gender}")
    try:
        content = read_file(input_file)
        logger.info("Input file read successfully")
    except Exception as e:
        logger.exception(f"Error reading input file: {str(e)}")
        raise ValueError(f"Error reading input file: {str(e)}")

    if source_lang != target_lang:
        logger.info("Translating content")
        content = process_text(content, 'translate', source_lang=source_lang, target_lang=target_lang)
        logger.info("Content translation completed")

    client = texttospeech.TextToSpeechClient()
    language_code = target_lang.split('-')[0]
    voice = texttospeech.VoiceSelectionParams(language_code=language_code, ssml_gender=voice_gender)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    chunks = split_content(content)
    logger.info(f"Content split into {len(chunks)} chunks")
    audio_segments = []

    for i, chunk in enumerate(chunks):
        logger.info(f"Processing chunk {i+1}/{len(chunks)}")
        synthesis_input = texttospeech.SynthesisInput(text=chunk)
        try:
            response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
            logger.info(f"Chunk {i+1} synthesized successfully")
        except Exception as e:
            logger.exception(f"Error in synthesize_speech for chunk {i+1}: {str(e)}")
            raise

        temp_file = f"temp_audio_{i}.mp3"
        write_file(response.audio_content, temp_file)

        audio_segment = AudioSegment.from_mp3(temp_file)
        audio_segments.append(audio_segment)
        os.remove(temp_file)
        logger.info(f"Processed and removed temporary file for chunk {i+1}")

    final_audio = sum(audio_segments)
    final_audio.export(output_file, format="mp3")
    logger.info(f"Audio book generated and saved as: {output_file}")

    return output_file

def split_content(content, max_chars=5000):
    """
    Splits content into chunks of maximum characters.
    
    :param content: The content to split
    :param max_chars: Maximum characters per chunk (default: 5000)
    :return: List of content chunks
    """
    logger.info(f"Splitting content into chunks of max {max_chars} characters")
    chunks = [content[i:i+max_chars] for i in range(0, len(content), max_chars)]
    logger.info(f"Content split into {len(chunks)} chunks")
    return chunks

def transcribe_audio_file(audio_file_path, language_code):
    """
    Transcribes an audio file to text using Google Cloud Speech-to-Text API.
    
    :param audio_file_path: The path to the audio file
    :param language_code: The language code of the audio
    :return: The transcribed text
    """
    logger.info(f"Starting audio file transcription. File: {audio_file_path}, Language: {language_code}")
    client = speech.SpeechClient()
    
    _, file_extension = os.path.splitext(audio_file_path)
    
    content = read_file(audio_file_path)
    logger.info("Audio file read successfully")

    audio = speech.RecognitionAudio(content=content)
    
    if file_extension.lower() == '.mp3':
        encoding = speech.RecognitionConfig.AudioEncoding.MP3
    elif file_extension.lower() in ['.wav', '.wave']:
        encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16
    else:
        logger.error(f"Unsupported audio format: {file_extension}")
        raise ValueError(f"Unsupported audio format: {file_extension}")

    config = speech.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=16000,
        language_code=language_code,
    )

    logger.info("Sending request to Google Cloud Speech-to-Text API")
    response = client.recognize(config=config, audio=audio)

    transcription = " ".join(result.alternatives[0].transcript for result in response.results)
    logger.info("Audio file transcription completed")
    return transcription.strip()

def translate_audio_file(input_file, output_file, source_lang, target_lang, voice_gender):
    """
    Translates an audio file from the source language to the target language.
    
    :param input_file: Path to the input audio file
    :param output_file: Path to save the output audio file
    :param source_lang: Source language code
    :param target_lang: Target language code
    :param voice_gender: Gender of the voice for text-to-speech
    :return: Path to the generated audio file
    """
    logger.info(f"Starting audio file translation. Input: {input_file}, Output: {output_file}")
    logger.info(f"Source language: {source_lang}, Target language: {target_lang}, Voice gender: {voice_gender}")

    try:
        transcribed_text = transcribe_audio_file(input_file, source_lang)
        logger.info("Audio transcription completed")

        translated_text = process_text(transcribed_text, 'translate', source_lang=source_lang, target_lang=target_lang)
        logger.info("Text translation completed")

        audio_content = text_to_speech(translated_text, target_lang, voice_gender)
        logger.info("Text-to-speech conversion completed")
        
        write_file(audio_content, output_file)
        logger.info(f"Translated audio file saved as: {output_file}")
        
        return output_file
    except Exception as e:
        logger.exception(f"An error occurred during audio file translation: {str(e)}")
        raise