import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from docx import Document

def get_language_choice(prompt, languages):
    """
    Presents a list of language choices to the user and returns the selected language.
    
    :param prompt: The prompt to display to the user
    :param languages: A dictionary of language choices
    :return: The selected language
    """
    print(prompt)
    for key, language in languages.items():
        print(f"{key}. {language[0]}")
    
    while True:
        choice = input("Enter your choice: ")
        if choice in languages:
            return languages[choice]
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
    return filename

def load_env_variables():
    """
    Loads environment variables from a .env file.
    """
    load_dotenv()

    # Check if required environment variables are set
    required_vars = ["OPENAI_API_KEY", "GOOGLE_APPLICATION_CREDENTIALS"]
    for var in required_vars:
        if not os.getenv(var):
            raise EnvironmentError(f"Missing required environment variable: {var}")

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def read_pdf_file(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def read_docx_file(file_path):
    doc = Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

def read_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == '.txt':
        return read_text_file(file_path)
    elif file_extension.lower() == '.pdf':
        return read_pdf_file(file_path)
    elif file_extension.lower() == '.docx':
        return read_docx_file(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")