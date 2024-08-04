import os
from speech.speech_processor import record_audio, transcribe_audio, text_to_speech, play_audio, save_audio
from text.text_processor import translate_text, analyze_sentiment, summarize_text
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
        print("1. Speech to Text")
        print("2. Text to Speech")
        print("3. Translate Text")
        print("4. Analyze Sentiment")
        print("5. Summarize Text")
        print("6. Speech to Speech Translation")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':  # Speech to Text
            source_lang, source_code = get_language_choice("Select the language you'll speak in:", languages)
            duration = int(input("Enter recording duration in seconds: "))
            audio_file = record_audio(duration)
            text = transcribe_audio(audio_file, source_code)
            print(f"Transcribed text: {text}")

        elif choice == '2':  # Text to Speech
            text = input("Enter the text to convert to speech: ")
            target_lang, target_code = get_language_choice("Select the output language:", languages)
            voice_name, voice_gender = get_language_choice("Select the voice gender:", voices)
            audio_content = text_to_speech(text, target_code, voice_gender)
            if audio_content:
                play_audio(audio_content)
                save_option = input("Do you want to save the audio? (y/n): ").lower()
                if save_option == 'y':
                    filename = get_filename("output", ".mp3")
                    save_audio(audio_content, filename)

        elif choice == '3':  # Translate Text
            text = input("Enter the text to translate: ")
            source_lang, _ = get_language_choice("Select the source language:", languages)
            target_lang, _ = get_language_choice("Select the target language:", languages)
            translated_text = translate_text(text, source_lang, target_lang)
            print(f"Translated text: {translated_text}")

        elif choice == '4':  # Analyze Sentiment
            text = input("Enter the text to analyze sentiment: ")
            sentiment = analyze_sentiment(text)
            print(f"Sentiment: {sentiment}")

        elif choice == '5':  # Summarize Text
            text = input("Enter the text to summarize: ")
            max_words = int(input("Enter the maximum number of words for the summary: "))
            summary = summarize_text(text, max_words)
            print(f"Summary: {summary}")

        elif choice == '6':  # Speech to Speech Translation
            source_lang, source_code = get_language_choice("Select the language you'll speak in:", languages)
            target_lang, target_code = get_language_choice("Select the target language:", languages)
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
                    filename = get_filename("translated_output", ".mp3")
                    save_audio(audio_content, filename)

        elif choice == '7':  # Exit
            print("Thank you for using the Speech and Text Processing Application. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()