from google.cloud import speech, texttospeech

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
voices = {
    "1": ("Male", texttospeech.SsmlVoiceGender.MALE),
    "2": ("Female", texttospeech.SsmlVoiceGender.FEMALE),
    "3": ("Neutral", texttospeech.SsmlVoiceGender.NEUTRAL)
}

# API settings
OPENAI_MODEL = "gpt-3.5-turbo"

# Audio settings
DEFAULT_AUDIO_DURATION = 5  # seconds
AUDIO_SAMPLE_RATE = 16000

# File paths
AUDIO_OUTPUT_DIR = "audio_output"