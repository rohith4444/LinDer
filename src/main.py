import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import (
    LANGUAGES, VOICES, AUDIO_OUTPUT_DIR, DOCUMENT_INPUT_DIR, DOCUMENT_OUTPUT_DIR,
    AUDIO_BOOK_INPUT_DIR, AUDIO_BOOK_OUTPUT_DIR, AUDIO_TO_TEXT_INPUT_DIR,
    AUDIO_TO_TEXT_OUTPUT_DIR, AUDIO_TRANSLATION_INPUT_DIR, AUDIO_TRANSLATION_OUTPUT_DIR,
    DEFAULT_AUDIO_DURATION
)
from speech.speech_processor import (
    record_audio, process_audio, process_audio_file, play_audio, save_audio,
    save_large_audio
)
from text.text_processor import process_text, process_file
from utils.common import get_language_choice, get_filename, load_env_variables, write_file, read_file
from logging_config import get_module_logger

logger = get_module_logger(__name__)

def main():
    """
    Main function to run the Speech and Text Processing Application.
    """
    logger.info("Starting Speech and Text Processing Application")
    load_env_variables()

    while True:
        logger.info("Displaying main menu")
        print("\nWelcome to the Speech and Text Processing Application!")
        print("1. Speech to Text (Same Language)")
        print("2. Speech to Text with Translation")
        print("3. Text to Speech (Same Language)")
        print("4. Text to Speech with Translation")
        print("5. Text Translation")
        print("6. Speech to Speech Translation")
        print("7. Document Translation")
        print("8. Generate Audio Book")
        print("9. Audio File to Text File (with Translation)")
        print("10. Audio File to Audio File Translation")
        print("11. Sentiment Analysis")
        print("12. Text Summarization")
        print("13. Exit")

        choice = input("Enter your choice (1-13): ")
        logger.info(f"User selected option: {choice}")

        if choice == '1':
            handle_speech_to_text(LANGUAGES, translate=False)
        elif choice == '2':
            handle_speech_to_text(LANGUAGES, translate=True)
        elif choice == '3':
            handle_text_to_speech(LANGUAGES, VOICES, translate=False)
        elif choice == '4':
            handle_text_to_speech(LANGUAGES, VOICES, translate=True)
        elif choice == '5':
            handle_text_translation(LANGUAGES)
        elif choice == '6':
            handle_speech_to_speech(LANGUAGES, VOICES)
        elif choice == '7':
            handle_document_translation(LANGUAGES)
        elif choice == '8':
            handle_audio_book_generation(LANGUAGES, VOICES)
        elif choice == '9':
            handle_audio_to_text_translation(LANGUAGES)
        elif choice == '10':
            handle_audio_to_audio_translation(LANGUAGES, VOICES)
        elif choice == '11':
            handle_sentiment_analysis()
        elif choice == '12':
            handle_text_summarization()
        elif choice == '13':
            logger.info("User chose to exit the application")
            print("Thank you for using the Speech and Text Processing Application. Goodbye!")
            break
        else:
            logger.warning(f"Invalid choice entered: {choice}")
            print("Invalid choice. Please try again.")

def handle_speech_to_text(languages, translate=False):
    """
    Handle speech-to-text conversion with optional translation.
    """
    logger.info(f"Starting speech-to-text process. Translation: {translate}")
    try:
        source_lang, source_code = get_language_choice("Select the language you'll speak in:", languages)
        duration = int(input(f"Enter recording duration in seconds (default: {DEFAULT_AUDIO_DURATION}): ") or DEFAULT_AUDIO_DURATION)
        
        audio_file = record_audio(duration)
        if not audio_file:
            logger.error("Failed to record audio")
            print("Failed to record audio. Please try again.")
            return

        text = process_audio(audio_file, 'transcribe', language_code=source_code)

        if not text:
            logger.error("Speech transcription failed")
            print("Speech transcription failed. Please try again.")
            return

        logger.info("Speech transcription completed successfully")
        print(f"Transcribed text: {text}")

        if translate:
            target_lang, _ = get_language_choice("Select the target language for translation:", languages)
            translated_text = process_text(text, 'translate', source_lang=source_lang, target_lang=target_lang)
            if not translated_text:
                logger.error("Text translation failed")
                print("Text translation failed. Please try again.")
                return

            logger.info("Text translation completed successfully")
            print(f"Translated text ({target_lang}): {translated_text}")

    except ValueError as ve:
        logger.error(f"Invalid input: {str(ve)}")
        print(f"Invalid input: {str(ve)}. Please try again.")
    except Exception as e:
        logger.exception(f"An unexpected error occurred during speech-to-text process: {str(e)}")
        print(f"An unexpected error occurred: {str(e)}. Please try again or contact support.")

def handle_text_to_speech(languages, voices, translate=False):
    """
    Handle text-to-speech conversion with optional translation.
    """
    logger.info(f"Starting text-to-speech process. Translation: {translate}")
    if translate:
        source_lang, _ = get_language_choice("Select the source language:", languages)
        text = input("Enter the text to translate and convert to speech: ")
        target_lang, target_code = get_language_choice("Select the target language for translation and speech:", languages)
        translated_text = process_text(text, 'translate', source_lang=source_lang, target_lang=target_lang)
        logger.info("Text translation completed")
        print(f"Translated text: {translated_text}")
    else:
        target_lang, target_code = get_language_choice("Select the language for text-to-speech:", languages)
        translated_text = input("Enter the text to convert to speech: ")

    voice_name, voice_gender = get_language_choice("Select the voice gender:", voices)
    audio_content = process_audio(translated_text, 'text_to_speech', text=translated_text, language_code=target_code, voice_gender=voice_gender)
    if audio_content:
        logger.info("Text-to-speech conversion completed")
        play_audio(audio_content)
        save_option = input("Do you want to save the audio? (y/n): ").lower()
        if save_option == 'y':
            base_filename = input("Enter a filename (without extension, default: output): ").strip() or "output"
            saved_path = save_audio(audio_content, base_filename)
            if saved_path:
                logger.info(f"Audio saved to: {saved_path}")
                print(f"Audio saved as: {saved_path}")

def handle_text_translation(languages):
    """
    Handle text-to-text translation.
    """
    logger.info("Starting text-to-text translation process")
    source_lang, _ = get_language_choice("Select the source language:", languages)
    target_lang, _ = get_language_choice("Select the target language:", languages)
    text = input("Enter the text to translate: ")
    translated_text = process_text(text, 'translate', source_lang=source_lang, target_lang=target_lang)
    logger.info("Text translation completed")
    print(f"Translated text: {translated_text}")

def handle_speech_to_speech(languages, voices):
    """
    Handle speech-to-speech translation.
    """
    logger.info("Starting speech-to-speech translation process")
    source_lang, source_code = get_language_choice("Select the language you'll speak in:", languages)
    target_lang, target_code = get_language_choice("Select the target language for translation:", languages)
    
    duration = int(input(f"Enter recording duration in seconds (default: {DEFAULT_AUDIO_DURATION}): ") or DEFAULT_AUDIO_DURATION)
    logger.info(f"Recording audio for {duration} seconds")
    audio_file = record_audio(duration)
    
    logger.info("Transcribing and translating audio")
    translated_text = process_audio(audio_file, 'translate', source_lang=source_code, target_lang=target_code)
    logger.info("Audio transcription and translation completed")
    print(f"Translated text: {translated_text}")

    voice_name, voice_gender = get_language_choice("Select the voice gender for the output speech:", voices)
    logger.info(f"Converting translated text to speech with {voice_name} voice")
    audio_content = process_audio(translated_text, 'text_to_speech', text=translated_text, language_code=target_code, voice_gender=voice_gender)
    if audio_content:
        logger.info("Playing translated audio")
        play_audio(audio_content)
        save_option = input("Do you want to save the translated audio? (y/n): ").lower()
        if save_option == 'y':
            base_filename = input("Enter a filename (without extension, default: translated_speech): ").strip() or "translated_speech"
            saved_path = save_audio(audio_content, base_filename)
            if saved_path:
                logger.info(f"Translated audio saved as: {saved_path}")
                print(f"Translated audio saved as: {saved_path}")
        else:
            logger.info("User chose not to save the translated audio")
    else:
        logger.error("Failed to convert translated text to speech")

def handle_document_translation(languages):
    """
    Handle the translation of document files.
    """
    logger.info("Starting document translation process")
    source_lang, _ = get_language_choice("Select the source language:", languages)
    target_lang, _ = get_language_choice("Select the target language:", languages)
    
    input_filename = input("Enter the input filename (including extension): ")
    output_filename = input("Enter the output filename (including extension): ")

    input_file = os.path.join(DOCUMENT_INPUT_DIR, input_filename)
    output_file = os.path.join(DOCUMENT_OUTPUT_DIR, output_filename)

    try:
        translated_file = process_file(input_file, output_file, 'translate', source_lang=source_lang, target_lang=target_lang)
        if translated_file:
            logger.info(f"Document translated successfully: {os.path.basename(translated_file)}")
            print(f"Translated file saved as: {os.path.basename(translated_file)}")
        else:
            logger.error("Document translation failed")
            print("Translation failed.")
    except Exception as e:
        logger.exception(f"An error occurred during file translation: {str(e)}")
        print(f"An error occurred during file translation: {str(e)}")

def handle_audio_book_generation(languages, voices):
    """
    Handle the generation of an audio book from a text file.
    """
    logger.info("Starting audio book generation process")
    source_lang, source_code = get_language_choice("Select the source language:", languages)
    target_lang, target_code = get_language_choice("Select the target language:", languages)
    voice_name, voice_gender = get_language_choice("Select the voice gender:", voices)

    input_filename = input("Enter the input filename (including extension): ")
    output_filename = input("Enter the output filename (without extension): ")

    input_file = os.path.join(AUDIO_BOOK_INPUT_DIR, input_filename)
    output_file = os.path.join(AUDIO_BOOK_OUTPUT_DIR, output_filename)

    logger.info(f"Generating audio book from {input_file}")
    logger.info(f"Source language: {source_lang}, Target language: {target_lang}, Voice gender: {voice_name}")
    print(f"Generating audio book from {input_file}...")
    print(f"Source language: {source_lang}")
    print(f"Target language: {target_lang}")
    print(f"Voice gender: {voice_name}")

    try:
        # Read the input file
        content = read_file(input_file)
        logger.info("Input file read successfully")

        # Translate if necessary
        if source_lang != target_lang:
            logger.info("Translating content")
            content = process_text(content, 'translate', source_lang=source_lang, target_lang=target_lang)
            logger.info("Content translation completed")

        # Convert text to speech
        audio_content = process_audio(content, 'text_to_speech', text=content, language_code=target_code, voice_gender=voice_gender)
        
        if audio_content:
            # Save the audio book
            if isinstance(audio_content, list):
                generated_file = save_large_audio(audio_content, output_file, use_unique_name=False)
            else:
                generated_file = save_audio(audio_content, output_file, use_unique_name=False)
            
            if generated_file:
                logger.info(f"Audio book generated successfully: {generated_file}")
                print(f"Audio book generated successfully!")
                print(f"Saved as: {generated_file}")
                
                play_option = input("Would you like to play the generated audio? (y/n): ").lower()
                if play_option == 'y':
                    logger.info("Playing generated audio book")
                    play_audio(generated_file)
            else:
                logger.error("Failed to save audio book")
                print("Failed to save audio book.")
        else:
            logger.error("Failed to generate audio content")
            print("Failed to generate audio book.")
    except Exception as e:
        logger.exception(f"An error occurred during audio book generation: {str(e)}")
        print(f"An error occurred during audio book generation: {str(e)}")

def handle_audio_to_text_translation(languages):
    """
    Handle the translation of an audio file to a text file.
    """
    logger.info("Starting audio to text translation process")
    source_lang, source_code = get_language_choice("Select the source language of the audio:", languages)
    target_lang, target_code = get_language_choice("Select the target language for translation:", languages)
    
    logger.info(f"Source language: {source_lang}, Source code: {source_code}")
    logger.info(f"Target language: {target_lang}, Target code: {target_code}")
    
    input_filename = input("Enter the input audio filename (including extension): ")
    output_filename = input("Enter the output text filename (including extension): ")

    input_file = os.path.join(AUDIO_TO_TEXT_INPUT_DIR, input_filename)
    output_file = os.path.join(AUDIO_TO_TEXT_OUTPUT_DIR, output_filename)

    logger.info(f"Input file: {input_file}")
    logger.info(f"Output file: {output_file}")

    try:
        result = process_audio_file(input_file, output_file, 'translate', source_lang=source_code, target_lang=target_code)
        if result:
            logger.info(f"Audio transcription and translation completed. Output saved to: {output_file}")
            print(f"Translated text saved as: {output_file}")
        else:
            logger.error("Audio transcription and translation failed")
            print("Audio transcription and translation failed. Please try again.")
    except Exception as e:
        logger.exception(f"An error occurred during audio-to-text translation: {str(e)}")
        print(f"An error occurred during audio-to-text translation: {str(e)}")

def handle_audio_to_audio_translation(languages, voices):
    """
    Handle the translation of an audio file to another audio file in a different language.
    """
    logger.info("Starting audio to audio translation process")
    source_lang, source_code = get_language_choice("Select the source language of the audio:", languages)
    target_lang, target_code = get_language_choice("Select the target language for translation:", languages)
    voice_name, voice_gender = get_language_choice("Select the voice gender for the output audio:", voices)
    
    input_filename = input("Enter the input audio filename (including extension): ")
    output_filename = input("Enter the output audio filename (including extension): ")

    input_file = os.path.join(AUDIO_TRANSLATION_INPUT_DIR, input_filename)
    output_file = os.path.join(AUDIO_TRANSLATION_OUTPUT_DIR, output_filename)

    try:
        process_audio_file(input_file, output_file, 'translate', source_lang=source_code, target_lang=target_code, voice_gender=voice_gender)
        logger.info(f"Audio translation completed: {output_file}")
        print(f"Translated audio saved as: {output_file}")
        
        play_option = input("Would you like to play the translated audio? (y/n): ").lower()
        if play_option == 'y':
            logger.info("Playing translated audio")
            play_audio(output_file)
    except Exception as e:
        logger.exception(f"An error occurred during audio translation: {str(e)}")
        print(f"An error occurred during audio translation: {str(e)}")

def handle_sentiment_analysis():
    """
    Handle sentiment analysis of text.
    """
    logger.info("Starting sentiment analysis process")
    text = input("Enter the text for sentiment analysis: ")
    logger.info("Performing sentiment analysis")
    sentiment = process_text(text, 'analyze_sentiment')
    if sentiment:
        logger.info(f"Sentiment analysis completed. Result: {sentiment}")
        print(f"Sentiment: {sentiment}")
    else:
        logger.error("Sentiment analysis failed")
        print("Failed to analyze sentiment.")

def handle_text_summarization():
    """
    Handle text summarization.
    """
    logger.info("Starting text summarization process")
    text = input("Enter the text to summarize: ")
    max_words = int(input("Enter the maximum number of words for the summary: "))
    logger.info(f"Summarizing text with max words: {max_words}")
    summary = process_text(text, 'summarize', max_words=max_words)
    if summary:
        logger.info("Text summarization completed")
        print(f"Summary: {summary}")
    else:
        logger.error("Text summarization failed")
        print("Failed to summarize text.")

if __name__ == "__main__":
    logger.info("Starting the main application")
    main()
    logger.info("Application execution completed")