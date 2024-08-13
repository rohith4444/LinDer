import os
from speech.speech_processor import record_audio, transcribe_audio, text_to_speech, play_audio, save_audio, generate_audio_book, transcribe_audio_file, translate_audio_file, set_data_dir
from text.text_processor import translate_text, translate_file, process_text, process_file
from utils.common import get_language_choice, get_filename, load_env_variables, write_file, read_file
from google.cloud import texttospeech
from logging_config import get_module_logger

logger = get_module_logger(__name__)

def main():
    """
    Main function to run the Speech and Text Processing Application.
    """

    logger.info("Starting Speech and Text Processing Application")

    load_env_variables()

    languages = {
        "1": ("English", "en-US"),
        "2": ("Spanish", "es-ES"),
        "3": ("French", "fr-FR"),
        "4": ("German", "de-DE"),
        "5": ("Italian", "it-IT")
    }

    voices = {
        "1": ("Male", texttospeech.SsmlVoiceGender.MALE),
        "2": ("Female", texttospeech.SsmlVoiceGender.FEMALE),
        "3": ("Neutral", texttospeech.SsmlVoiceGender.NEUTRAL)
    }

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
            handle_document_translation(languages)
        elif choice == '8':
            handle_audio_book_generation(languages, voices)
        elif choice == '9':
            handle_audio_to_text_translation(languages)
        elif choice == '10':
            handle_audio_to_audio_translation(languages, voices)
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

# Define constants for input and output directories
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
IO_FILES_DIR = os.path.join(DATA_DIR, 'io files')
set_data_dir(IO_FILES_DIR)
DOCUMENT_INPUT_DIR = os.path.join(DATA_DIR, 'document_translation', 'input')
DOCUMENT_OUTPUT_DIR = os.path.join(DATA_DIR, 'document_translation', 'output')
AUDIO_BOOK_INPUT_DIR = os.path.join(DATA_DIR, 'audio_book', 'input')
AUDIO_BOOK_OUTPUT_DIR = os.path.join(DATA_DIR, 'audio_book', 'output')
AUDIO_TO_TEXT_INPUT_DIR = os.path.join(DATA_DIR, 'audio_to_text', 'input')
AUDIO_TO_TEXT_OUTPUT_DIR = os.path.join(DATA_DIR, 'audio_to_text', 'output')
AUDIO_TRANSLATION_INPUT_DIR = os.path.join(DATA_DIR, 'audio_translation', 'input')
AUDIO_TRANSLATION_OUTPUT_DIR = os.path.join(DATA_DIR, 'audio_translation', 'output')

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
    output_filename = input("Enter the output filename (including extension): ")

    input_file = os.path.join(AUDIO_BOOK_INPUT_DIR, input_filename)
    output_file = os.path.join(AUDIO_BOOK_OUTPUT_DIR, output_filename)

    logger.info(f"Generating audio book from {input_file}")
    logger.info(f"Source language: {source_lang}, Target language: {target_lang}, Voice gender: {voice_name}")
    print(f"Generating audio book from {input_file}...")
    print(f"Source language: {source_lang}")
    print(f"Target language: {target_lang}")
    print(f"Voice gender: {voice_name}")

    try:
        generated_file = generate_audio_book(input_file, output_file, source_code, target_code, voice_gender)
        logger.info(f"Audio book generated successfully: {generated_file}")
        print(f"Audio book generated successfully!")
        print(f"Saved as: {generated_file}")
        
        play_option = input("Would you like to play the generated audio? (y/n): ").lower()
        if play_option == 'y':
            logger.info("Playing generated audio book")
            play_audio(generated_file)
    except Exception as e:
        logger.exception(f"An error occurred during audio book generation: {str(e)}")
        print(f"An error occurred during audio book generation: {str(e)}")

def handle_audio_to_text_translation(languages):
    """
    Handle the translation of an audio file to a text file.
    """
    logger.info("Starting audio to text translation process")
    source_lang, source_code = get_language_choice("Select the source language of the audio:", languages)
    target_lang, _ = get_language_choice("Select the target language for translation:", languages)
    
    input_filename = input("Enter the input audio filename (including extension): ")
    output_filename = input("Enter the output text filename (including extension): ")

    input_file = os.path.join(AUDIO_TO_TEXT_INPUT_DIR, input_filename)
    output_file = os.path.join(AUDIO_TO_TEXT_OUTPUT_DIR, output_filename)

    try:
        transcribed_text = transcribe_audio_file(input_file, source_code)
        logger.info("Audio transcription completed")
        print(f"Transcribed text: {transcribed_text}")

        translated_text = process_text(transcribed_text, 'translate', source_lang=source_lang, target_lang=target_lang)
        logger.info("Text translation completed")
        print(f"Translated text: {translated_text}")

        write_file(translated_text, output_file)
        logger.info(f"Translated text saved to: {output_file}")
        print(f"Translated text saved as: {output_file}")
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
        translated_audio_file = translate_audio_file(input_file, output_file, source_code, target_code, voice_gender)
        logger.info(f"Audio translation completed: {translated_audio_file}")
        print(f"Translated audio saved as: {translated_audio_file}")
        
        play_option = input("Would you like to play the translated audio? (y/n): ").lower()
        if play_option == 'y':
            logger.info("Playing translated audio")
            play_audio(translated_audio_file)
    except Exception as e:
        logger.exception(f"An error occurred during audio translation: {str(e)}")
        print(f"An error occurred during audio translation: {str(e)}")

def handle_speech_to_text(languages, translate=False):
    """
    Handle speech-to-text conversion with optional translation.
    """
    logger.info(f"Starting speech-to-text process. Translation: {translate}")
    source_lang, source_code = get_language_choice("Select the language you'll speak in:", languages)
    duration = int(input("Enter recording duration in seconds: "))
    audio_file = record_audio(duration)
    text = transcribe_audio(audio_file, source_code)
    logger.info("Speech transcription completed")
    print(f"Transcribed text: {text}")

    if translate:
        target_lang, _ = get_language_choice("Select the target language for translation:", languages)
        translated_text = process_text(text, 'translate', source_lang=source_lang, target_lang=target_lang)
        logger.info("Text translation completed")
        print(f"Translated text ({target_lang}): {translated_text}")

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
        text = input("Enter the text to convert to speech: ")
        translated_text = text

    voice_name, voice_gender = get_language_choice("Select the voice gender:", voices)
    audio_content = text_to_speech(translated_text, target_code, voice_gender)
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
    
    duration = int(input("Enter recording duration in seconds: "))
    logger.info(f"Recording audio for {duration} seconds")
    audio_file = record_audio(duration)
    
    logger.info("Transcribing audio")
    text = transcribe_audio(audio_file, source_code)
    logger.info("Audio transcription completed")
    print(f"Transcribed text: {text}")

    logger.info("Translating transcribed text")
    translated_text = process_text(text, 'translate', source_lang=source_lang, target_lang=target_lang)
    logger.info("Text translation completed")
    print(f"Translated text: {translated_text}")

    voice_name, voice_gender = get_language_choice("Select the voice gender for the output speech:", voices)
    logger.info(f"Converting translated text to speech with {voice_name} voice")
    audio_content = text_to_speech(translated_text, target_code, voice_gender)
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