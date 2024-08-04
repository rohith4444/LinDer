import os
from speech.speech_processor import record_audio, transcribe_audio, text_to_speech, play_audio, save_audio
from text.text_processor import translate_text
from utils.common import get_language_choice, get_filename, load_env_variables
from google.cloud import texttospeech

def main():
    # Load environment variables
    load_env_variables()

    # Define language options
    languages = {
        "1": ("English", "en-US"),
        "2": ("Spanish", "es-ES"),
        "3": ("French", "fr-FR"),
        "4": ("German", "de-DE"),
        "5": ("Italian", "it-IT")
    }

    # Define voice options
    voices = {
        "1": ("Male", texttospeech.SsmlVoiceGender.MALE),
        "2": ("Female", texttospeech.SsmlVoiceGender.FEMALE),
        "3": ("Neutral", texttospeech.SsmlVoiceGender.NEUTRAL)
    }

    while True:
        print("\nWelcome to the Speech and Text Processing Application!")
        print("1. Speech to Text (Same Language)")
        print("2. Speech to Text with Translation")
        print("3. Text to Speech (Same Language)")
        print("4. Text to Speech with Translation")
        print("5. Text to Text Language Translation")
        print("6. Speech to Speech Language Translation")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            handle_speech_to_text(languages, translate=False)
        elif choice == '2':
            handle_speech_to_text(languages, translate=True)
        elif choice == '3':
            handle_text_to_speech(languages, voices, translate=False)
        elif choice == '4':
            handle_text_to_speech(languages, voices, translate=True)
        elif choice == '5':
            handle_text_translation(languages)
        elif choice == '6':
            handle_speech_to_speech(languages, voices)
        elif choice == '7':
            print("Thank you for using the Speech and Text Processing Application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def handle_speech_to_text(languages, translate=False):
    source_lang, source_code = get_language_choice("Select the language you'll speak in:", languages)
    duration = int(input("Enter recording duration in seconds: "))
    audio_file = record_audio(duration)
    text = transcribe_audio(audio_file, source_code)
    print(f"Transcribed text: {text}")

    if translate:
        target_lang, _ = get_language_choice("Select the target language for translation:", languages)
        translated_text = translate_text(text, source_lang, target_lang)
        print(f"Translated text ({target_lang}): {translated_text}")

def handle_text_to_speech(languages, voices, translate=False):
    if translate:
        source_lang, _ = get_language_choice("Select the source language:", languages)
        text = input("Enter the text to translate and convert to speech: ")
        target_lang, target_code = get_language_choice("Select the target language for translation and speech:", languages)
        translated_text = translate_text(text, source_lang, target_lang)
        print(f"Translated text: {translated_text}")
    else:
        target_lang, target_code = get_language_choice("Select the language for text-to-speech:", languages)
        text = input("Enter the text to convert to speech: ")
        translated_text = text

    voice_name, voice_gender = get_language_choice("Select the voice gender:", voices)
    audio_content = text_to_speech(translated_text, target_code, voice_gender)
    if audio_content:
        play_audio(audio_content)
        save_option = input("Do you want to save the audio? (y/n): ").lower()
        if save_option == 'y':
            base_filename = input("Enter a filename (without extension, default: output): ").strip() or "output"
            saved_path = save_audio(audio_content, base_filename)
            if saved_path:
                print(f"Audio saved as: {saved_path}")

def handle_text_translation(languages):
    source_lang, _ = get_language_choice("Select the source language:", languages)
    target_lang, _ = get_language_choice("Select the target language:", languages)
    text = input("Enter the text to translate: ")
    translated_text = translate_text(text, source_lang, target_lang)
    print(f"Translated text: {translated_text}")

def handle_speech_to_speech(languages, voices):
    source_lang, source_code = get_language_choice("Select the language you'll speak in:", languages)
    target_lang, target_code = get_language_choice("Select the target language for translation:", languages)
    
    duration = int(input("Enter recording duration in seconds: "))
    audio_file = record_audio(duration)
    text = transcribe_audio(audio_file, source_code)
    print(f"Transcribed text: {text}")

    translated_text = translate_text(text, source_lang, target_lang)
    print(f"Translated text: {translated_text}")

    voice_name, voice_gender = get_language_choice("Select the voice gender for the output speech:", voices)
    audio_content = text_to_speech(translated_text, target_code, voice_gender)
    if audio_content:
        play_audio(audio_content)
        save_option = input("Do you want to save the translated audio? (y/n): ").lower()
        if save_option == 'y':
            base_filename = input("Enter a filename (without extension, default: translated_speech): ").strip() or "translated_speech"
            saved_path = save_audio(audio_content, base_filename)
            if saved_path:
                print(f"Translated audio saved as: {saved_path}")

if __name__ == "__main__":
    main()