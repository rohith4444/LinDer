import os
from google.cloud import speech, texttospeech
import configparser

# Load external configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Application settings

# Language options
LANGUAGES = {
    "1": ("English", "en-US"),
    "2": ("Spanish", "es-ES"),
    "3": ("French", "fr-FR"),
    "4": ("German", "de-DE"),
    "5": ("Italian", "it-IT")
}

# Voice options
VOICES = {
    "1": ("Male", texttospeech.SsmlVoiceGender.MALE),
    "2": ("Female", texttospeech.SsmlVoiceGender.FEMALE),
    "3": ("Neutral", texttospeech.SsmlVoiceGender.NEUTRAL)
}

# API settings
OPENAI_MODEL = config.get('API', 'OPENAI_MODEL', fallback='gpt-3.5-turbo')
OPENAI_API_KEY = config.get('API', 'OPENAI_API_KEY', fallback=os.getenv('OPENAI_API_KEY'))

# Google Cloud settings
GOOGLE_APPLICATION_CREDENTIALS = config.get('Google', 'GOOGLE_APPLICATION_CREDENTIALS', 
                                            fallback=os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))

# Audio settings
DEFAULT_AUDIO_DURATION = config.getint('Audio', 'DEFAULT_AUDIO_DURATION', fallback=5)  # seconds
AUDIO_SAMPLE_RATE = config.getint('Audio', 'AUDIO_SAMPLE_RATE', fallback=16000)

# File paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
AUDIO_OUTPUT_DIR = os.path.join(DATA_DIR, config.get('Paths', 'AUDIO_OUTPUT_DIR', fallback='audio_output'))
DOCUMENT_INPUT_DIR = os.path.join(DATA_DIR, config.get('Paths', 'DOCUMENT_INPUT_DIR', fallback='document_translation/input'))
DOCUMENT_OUTPUT_DIR = os.path.join(DATA_DIR, config.get('Paths', 'DOCUMENT_OUTPUT_DIR', fallback='document_translation/output'))
AUDIO_BOOK_INPUT_DIR = os.path.join(DATA_DIR, config.get('Paths', 'AUDIO_BOOK_INPUT_DIR', fallback='audio_book/input'))
AUDIO_BOOK_OUTPUT_DIR = os.path.join(DATA_DIR, config.get('Paths', 'AUDIO_BOOK_OUTPUT_DIR', fallback='audio_book/output'))
AUDIO_TO_TEXT_INPUT_DIR = os.path.join(DATA_DIR, config.get('Paths', 'AUDIO_TO_TEXT_INPUT_DIR', fallback='audio_to_text/input'))
AUDIO_TO_TEXT_OUTPUT_DIR = os.path.join(DATA_DIR, config.get('Paths', 'AUDIO_TO_TEXT_OUTPUT_DIR', fallback='audio_to_text/output'))
AUDIO_TRANSLATION_INPUT_DIR = os.path.join(DATA_DIR, config.get('Paths', 'AUDIO_TRANSLATION_INPUT_DIR', fallback='audio_translation/input'))
AUDIO_TRANSLATION_OUTPUT_DIR = os.path.join(DATA_DIR, config.get('Paths', 'AUDIO_TRANSLATION_OUTPUT_DIR', fallback='audio_translation/output'))

# Logging settings
LOG_LEVEL = config.get('Logging', 'LOG_LEVEL', fallback='INFO')
LOG_FORMAT = config.get('Logging', 'LOG_FORMAT', fallback='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOG_DIR = os.path.join(BASE_DIR, config.get('Logging', 'LOG_DIR', fallback='logs'))
MAX_LOG_SIZE = config.getint('Logging', 'MAX_LOG_SIZE', fallback=5 * 1024 * 1024)  # 5 MB
BACKUP_COUNT = config.getint('Logging', 'BACKUP_COUNT', fallback=5)