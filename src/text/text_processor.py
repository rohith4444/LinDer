import os
from openai import OpenAI
from utils.common import read_file, write_file

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def translate_text(text, source_lang, target_lang):
    """
    Translates text from source language to target language using OpenAI's API.
    
    :param text: The text to translate
    :param source_lang: The source language
    :param target_lang: The target language
    :return: Translated text or None if translation fails
    """
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a translator. Translate the following text from {source_lang} to {target_lang}."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"An error occurred during translation: {str(e)}")
        return None

def analyze_sentiment(text):
    """
    Analyzes the sentiment of the given text using OpenAI's API.
    
    :param text: The text to analyze
    :return: Sentiment analysis result or None if analysis fails
    """
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a sentiment analyzer. Analyze the sentiment of the following text and respond with 'Positive', 'Negative', or 'Neutral'."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"An error occurred during sentiment analysis: {str(e)}")
        return None

def summarize_text(text, max_words=100):
    """
    Summarizes the given text using OpenAI's API.
    
    :param text: The text to summarize
    :param max_words: The maximum number of words for the summary
    :return: Summarized text or None if summarization fails
    """
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a text summarizer. Summarize the following text in no more than {max_words} words."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"An error occurred during text summarization: {str(e)}")
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
    try:
        content = read_file(input_file)
        translated_content = translate_text(content, source_lang, target_lang)
        write_file(translated_content, output_file)
        return output_file
    except Exception as e:
        print(f"An error occurred during file translation: {str(e)}")
        return None

def process_text(text, operation, **kwargs):
    """
    Processes text based on the specified operation.
    
    :param text: The text to process
    :param operation: The operation to perform ('translate', 'analyze_sentiment', or 'summarize')
    :param kwargs: Additional keyword arguments for specific operations
    :return: Processed text or None if processing fails
    """
    if operation == 'translate':
        return translate_text(text, kwargs['source_lang'], kwargs['target_lang'])
    elif operation == 'analyze_sentiment':
        return analyze_sentiment(text)
    elif operation == 'summarize':
        return summarize_text(text, kwargs.get('max_words', 100))
    else:
        print(f"Unsupported operation: {operation}")
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
    try:
        content = read_file(input_file)
        processed_content = process_text(content, operation, **kwargs)
        if processed_content:
            write_file(processed_content, output_file)
            return output_file
        else:
            return None
    except Exception as e:
        print(f"An error occurred during file processing: {str(e)}")
        return None