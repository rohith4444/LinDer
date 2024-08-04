import os
import io
import wave
import pyaudio
import pygame
from datetime import datetime
from google.cloud import speech, texttospeech

# Initialize Google Cloud clients
speech_client = speech.SpeechClient()
tts_client = texttospeech.TextToSpeechClient()

# Define the path to the specdata folder
SPECDATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'specdata')

def generate_unique_filename(base_name, extension):
    """
    Generates a unique filename using the current timestamp.
    
    :param base_name: The base name for the file
    :param extension: The file extension
    :return: A unique filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}{extension}"

def record_audio(duration=5, sample_rate=16000):
    """
    Records audio from the microphone and saves it to a file in the specdata folder.
    
    :param duration: The duration of the recording in seconds (default: 5)
    :param sample_rate: The sample rate of the audio (default: 16000)
    :return: The path of the saved audio file or None if an error occurred
    """
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1

    # Generate a unique filename
    filename = generate_unique_filename("recorded_audio", ".wav")
    full_path = os.path.join(SPECDATA_DIR, filename)

    try:
        p = pyaudio.PyAudio()

        # Ensure the specdata directory exists
        os.makedirs(SPECDATA_DIR, exist_ok=True)

        print(f"Recording for {duration} seconds...")

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=CHUNK)

        frames = []

        for i in range(0, int(sample_rate / CHUNK * duration)):
            try:
                data = stream.read(CHUNK)
                frames.append(data)
            except IOError as e:
                print(f"Warning: Dropped frame due to I/O error: {e}")

        print("Recording finished.")

        stream.stop_stream()
        stream.close()
        p.terminate()

        # Save the recorded audio to a file in the specdata folder
        with wave.open(full_path, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))
        print(f"Audio saved as: {full_path}")
        return full_path

    except pyaudio.PyAudioError as e:
        print(f"Error initializing PyAudio: {e}")
        return None
    except OSError as e:
        print(f"Error accessing the audio device: {e}")
        return None
    except wave.Error as e:
        print(f"Error saving the audio file: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    finally:
        # Cleanup
        if stream:
            try:
                stream.stop_stream()
                stream.close()
            except Exception as e:
                print(f"Note: Could not close stream. It may already be closed. Details: {e}")
        if p:
            try:
                p.terminate()
            except Exception as e:
                print(f"Note: Error terminating PyAudio. Details: {e}")

def transcribe_audio(audio_file, language_code):
    """
    Transcribes audio to text using Google Cloud Speech-to-Text API.
    
    :param audio_file: The path to the audio file
    :param language_code: The language code of the audio
    :return: The transcribed text
    """
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
            return result.alternatives[0].transcript

        return ""  # Return empty string if no transcription is found

    except Exception as e:
        print(f"Error during audio transcription: {e}")
        return ""

def text_to_speech(text, language_code, voice_gender):
    """
    Converts text to speech using Google Cloud Text-to-Speech API.
    
    :param text: The text to convert to speech
    :param language_code: The language code for the text
    :param voice_gender: The gender of the voice to use
    :return: Audio content or None if conversion fails
    """
    try:
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            ssml_gender=voice_gender
        )
        
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = tts_client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        return response.audio_content
    except Exception as e:
        print(f"An error occurred during text-to-speech conversion: {str(e)}")
        return None

def play_audio(audio_content):
    """
    Plays the audio content using pygame.
    
    :param audio_content: The audio content to play
    """
    try:
        pygame.mixer.init()
        audio_bytes = io.BytesIO(audio_content)
        pygame.mixer.music.load(audio_bytes)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"An error occurred during audio playback: {str(e)}")

def save_audio(audio_content, base_filename="output"):
    """
    Saves the audio content to a file in the specdata folder with a unique filename.
    
    :param audio_content: The audio content to save
    :param base_filename: The base name for the file (default: "output")
    :return: The full path of the saved file or None if an error occurred
    """
    try:
        # Ensure the specdata directory exists
        os.makedirs(SPECDATA_DIR, exist_ok=True)
        
        # Generate a unique filename
        filename = generate_unique_filename(base_filename, ".mp3")
        full_path = os.path.join(SPECDATA_DIR, filename)
        
        with open(full_path, "wb") as out:
            out.write(audio_content)
        print(f'Audio content written to file "{full_path}"')
        return full_path
    except Exception as e:
        print(f"An error occurred while saving the audio: {str(e)}")
        return None