from openai import OpenAI
import os
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from utils.common import read_file
from PyPDF2 import PdfReader, PdfWriter

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

def write_pdf(content, output_file):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    width, height = letter
    y = height - 50  # Start 50 points down from the top

    for line in content.split('\n'):
        if y < 50:  # If we're near the bottom of the page
            can.showPage()  # Start a new page
            y = height - 50  # Reset y to the top of the new page

        can.drawString(50, y, line)
        y -= 15  # Move down 15 points

    can.save()

    packet.seek(0)
    new_pdf = PdfReader(packet)
    writer = PdfWriter()
    writer.add_page(new_pdf.pages[0])

    with open(output_file, 'wb') as output_file_handle:
        writer.write(output_file_handle)

def translate_file(input_file, output_file, source_lang, target_lang):
    content = read_file(input_file)
    translated_content = translate_text(content, source_lang, target_lang)
    
    _, file_extension = os.path.splitext(output_file)
    if file_extension.lower() == '.txt':
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(translated_content)
    elif file_extension.lower() == '.pdf':
        write_pdf(translated_content, output_file)
    elif file_extension.lower() == '.docx':
        doc = Document()
        doc.add_paragraph(translated_content)
        doc.save(output_file)
    else:
        raise ValueError(f"Unsupported output file format: {file_extension}")

    return output_file