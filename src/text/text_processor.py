import os
from openai import OpenAI
from utils.common import read_file, write_file
from logging_config import get_module_logger
from config.settings import OPENAI_API_KEY, OPENAI_MODEL, DOCUMENT_INPUT_DIR, DOCUMENT_OUTPUT_DIR

# Get logger for this module
logger = get_module_logger(__name__)

# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def translate_text(text, source_lang, target_lang):
    """
    Translates text from source language to target language using OpenAI's API.
    
    :param text: The text to translate
    :param source_lang: The source language
    :param target_lang: The target language
    :return: Translated text or None if translation fails
    """
    logger.info(f"Starting text translation from {source_lang} to {target_lang}")
    try:
        response = openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": f"You are a translator. Translate the following text from {source_lang} to {target_lang}."},
                {"role": "user", "content": text}
            ]
        )
        translated_text = response.choices[0].message.content.strip()
        logger.info("Text translation completed successfully")
        return translated_text
    except Exception as e:
        logger.exception(f"An error occurred during translation: {str(e)}")
        return None

def analyze_sentiment(text):
    """
    Analyzes the sentiment of the given text using OpenAI's API.
    
    :param text: The text to analyze
    :return: Sentiment analysis result or None if analysis fails
    """
    logger.info("Starting sentiment analysis")
    try:
        response = openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a sentiment analyzer. Analyze the sentiment of the following text and respond with 'Positive', 'Negative', or 'Neutral'."},
                {"role": "user", "content": text}
            ]
        )
        sentiment = response.choices[0].message.content.strip()
        logger.info(f"Sentiment analysis completed. Result: {sentiment}")
        return sentiment
    except Exception as e:
        logger.exception(f"An error occurred during sentiment analysis: {str(e)}")
        return None

def summarize_text(text, max_words=100):
    """
    Summarizes the given text using OpenAI's API.
    
    :param text: The text to summarize
    :param max_words: The maximum number of words for the summary
    :return: Summarized text or None if summarization fails
    """
    logger.info(f"Starting text summarization. Max words: {max_words}")
    try:
        response = openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": f"You are a text summarizer. Summarize the following text in no more than {max_words} words."},
                {"role": "user", "content": text}
            ]
        )
        summary = response.choices[0].message.content.strip()
        logger.info("Text summarization completed successfully")
        return summary
    except Exception as e:
        logger.exception(f"An error occurred during text summarization: {str(e)}")
        return None

def translate_file(input_file, output_file, source_lang, target_lang):
    """
    Translates the content of a file from source language to target language.
    
    :param input_file: Path to the input file
    :param output_file: Path to save the translated file
    :param source_lang: Source language
    :param target_lang: Target language
    :return: Path to the translated file
    """
    logger.info(f"Starting file translation. Input: {input_file}, Output: {output_file}")
    logger.info(f"Source language: {source_lang}, Target language: {target_lang}")
    try:
        content = read_file(input_file)
        logger.info("Input file read successfully")
        translated_content = translate_text(content, source_lang, target_lang)
        if translated_content:
            write_file(translated_content, output_file)
            logger.info(f"Translated content written to: {output_file}")
            return output_file
        else:
            logger.error("Translation failed, no content to write")
            return None
    except Exception as e:
        logger.exception(f"An error occurred during file translation: {str(e)}")
        return None

def process_text(text, operation, **kwargs):
    """
    Processes text based on the specified operation.
    
    :param text: The text to process
    :param operation: The operation to perform ('translate', 'analyze_sentiment', or 'summarize')
    :param kwargs: Additional keyword arguments for specific operations
    :return: Processed text or None if processing fails
    """
    logger.info(f"Processing text with operation: {operation}")
    if operation == 'translate':
        return translate_text(text, kwargs['source_lang'], kwargs['target_lang'])
    elif operation == 'analyze_sentiment':
        return analyze_sentiment(text)
    elif operation == 'summarize':
        return summarize_text(text, kwargs.get('max_words', 100))
    else:
        logger.error(f"Unsupported operation: {operation}")
        return None

def process_file(input_file, output_file, operation, **kwargs):
    """
    Processes a file based on the specified operation.
    
    :param input_file: Path to the input file
    :param output_file: Path to save the processed file
    :param operation: The operation to perform ('translate', 'analyze_sentiment', or 'summarize')
    :param kwargs: Additional keyword arguments for specific operations
    :return: Path to the processed file or None if processing fails
    """
    logger.info(f"Processing file. Input: {input_file}, Output: {output_file}, Operation: {operation}")
    try:
        content = read_file(input_file)
        logger.info("Input file read successfully")
        processed_content = process_text(content, operation, **kwargs)
        if processed_content:
            write_file(processed_content, output_file)
            logger.info(f"Processed content written to: {output_file}")
            return output_file
        else:
            logger.error("Processing failed, no content to write")
            return None
    except Exception as e:
        logger.exception(f"An error occurred during file processing: {str(e)}")
        return None

def batch_translate_files(input_dir=DOCUMENT_INPUT_DIR, output_dir=DOCUMENT_OUTPUT_DIR, source_lang='en', target_lang='es'):
    """
    Translates all text files in the input directory and saves the translated files in the output directory.
    
    :param input_dir: Directory containing files to translate (default: DOCUMENT_INPUT_DIR)
    :param output_dir: Directory to save translated files (default: DOCUMENT_OUTPUT_DIR)
    :param source_lang: Source language (default: 'en')
    :param target_lang: Target language (default: 'es')
    """
    logger.info(f"Starting batch translation. Input dir: {input_dir}, Output dir: {output_dir}")
    logger.info(f"Source language: {source_lang}, Target language: {target_lang}")
    
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):  # Assuming we're only translating .txt files
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, f"translated_{filename}")
            
            logger.info(f"Translating file: {filename}")
            result = translate_file(input_file, output_file, source_lang, target_lang)
            
            if result:
                logger.info(f"Successfully translated: {filename}")
            else:
                logger.error(f"Failed to translate: {filename}")
    
    logger.info("Batch translation completed")
