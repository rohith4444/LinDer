import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader, PdfWriter
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from datetime import datetime
from logging_config import get_module_logger

# Get logger for this module
logger = get_module_logger(__name__)

def generate_unique_filename(base_name, extension):
    """
    Generates a unique filename using the current timestamp.
    
    :param base_name: The base name for the file
    :param extension: The file extension
    :return: A unique filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_filename = f"{base_name}_{timestamp}{extension}"
    logger.info(f"Generated unique filename: {unique_filename}")
    return unique_filename

def get_language_choice(prompt, languages):
    """
    Presents a list of language choices to the user and returns the selected language.
    
    :param prompt: The prompt to display to the user
    :param languages: A dictionary of language choices
    :return: The selected language
    """
    logger.info("Presenting language choices to user")
    print(prompt)
    for key, language in languages.items():
        print(f"{key}. {language[0]}")
    
    while True:
        choice = input("Enter your choice: ")
        if choice in languages:
            selected_language = languages[choice]
            logger.info(f"User selected language: {selected_language[0]}")
            return selected_language
        logger.warning(f"Invalid language choice: {choice}")
        print("Invalid choice. Please try again.")

def get_filename(default_name, extension):
    """
    Prompts the user for a filename and returns it with the given extension.
    
    :param default_name: The default filename to use if the user doesn't provide one
    :param extension: The file extension to use
    :return: The filename with extension
    """
    filename = input(f"Enter a filename (default: {default_name}{extension}): ").strip()
    if not filename:
        filename = default_name
    if not filename.endswith(extension):
        filename += extension
    logger.info(f"User provided filename: {filename}")
    return filename

def load_env_variables():
    """
    Loads environment variables from a .env file.
    """
    logger.info("Loading environment variables")
    load_dotenv()

    required_vars = ["OPENAI_API_KEY", "GOOGLE_APPLICATION_CREDENTIALS"]
    for var in required_vars:
        if not os.getenv(var):
            logger.error(f"Missing required environment variable: {var}")
            raise EnvironmentError(f"Missing required environment variable: {var}")
    logger.info("Environment variables loaded successfully")

def read_text_file(file_path):
    """
    Reads content from a text file.
    
    :param file_path: Path to the text file
    :return: Content of the text file
    """
    logger.info(f"Reading text file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        logger.info("Text file read successfully")
        return content
    except Exception as e:
        logger.exception(f"Error reading text file: {str(e)}")
        raise

def read_pdf_file(file_path):
    """
    Reads content from a PDF file.
    
    :param file_path: Path to the PDF file
    :return: Content of the PDF file
    """
    logger.info(f"Reading PDF file: {file_path}")
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        logger.info("PDF file read successfully")
        return text
    except Exception as e:
        logger.exception(f"Error reading PDF file: {str(e)}")
        raise

def read_docx_file(file_path):
    """
    Reads content from a DOCX file.
    
    :param file_path: Path to the DOCX file
    :return: Content of the DOCX file
    """
    logger.info(f"Reading DOCX file: {file_path}")
    try:
        doc = Document(file_path)
        content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        logger.info("DOCX file read successfully")
        return content
    except Exception as e:
        logger.exception(f"Error reading DOCX file: {str(e)}")
        raise

def read_file(file_path):
    """
    Reads content from a file based on its extension.
    
    :param file_path: Path to the file
    :return: Content of the file
    """
    logger.info(f"Reading file: {file_path}")
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == '.txt':
        return read_text_file(file_path)
    elif file_extension.lower() == '.pdf':
        return read_pdf_file(file_path)
    elif file_extension.lower() == '.docx':
        return read_docx_file(file_path)
    else:
        logger.error(f"Unsupported file format: {file_extension}")
        raise ValueError(f"Unsupported file format: {file_extension}")

def write_pdf(content, output_file):
    """
    Writes content to a PDF file.
    
    :param content: The content to write to the PDF
    :param output_file: The path to save the PDF file
    """
    logger.info(f"Writing content to PDF file: {output_file}")
    try:
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
        logger.info("Content written to PDF successfully")
    except Exception as e:
        logger.exception(f"Error writing to PDF file: {str(e)}")
        raise

def write_docx(content, output_file):
    """
    Writes content to a DOCX file.
    
    :param content: The content to write to the DOCX
    :param output_file: The path to save the DOCX file
    """
    logger.info(f"Writing content to DOCX file: {output_file}")
    try:
        doc = Document()
        doc.add_paragraph(content)
        doc.save(output_file)
        logger.info("Content written to DOCX successfully")
    except Exception as e:
        logger.exception(f"Error writing to DOCX file: {str(e)}")
        raise

def write_file(content, output_file):
    """
    Writes content to a file based on its extension.
    
    :param content: The content to write to the file
    :param output_file: The path to save the file
    """
    logger.info(f"Writing content to file: {output_file}")
    _, file_extension = os.path.splitext(output_file)
    try:
        if file_extension.lower() == '.txt':
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(content)
            logger.info("Content written to text file successfully")
        elif file_extension.lower() == '.pdf':
            write_pdf(content, output_file)
        elif file_extension.lower() == '.docx':
            write_docx(content, output_file)
        else:
            logger.error(f"Unsupported output file format: {file_extension}")
            raise ValueError(f"Unsupported output file format: {file_extension}")
    except Exception as e:
        logger.exception(f"Error writing to file: {str(e)}")
        raise