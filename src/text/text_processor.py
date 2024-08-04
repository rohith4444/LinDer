from openai import OpenAI
import os

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