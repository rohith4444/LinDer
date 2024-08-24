import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
from datetime import datetime
from src.utils.common import (
    generate_unique_filename, get_language_choice, get_filename,
    load_env_variables, read_file, write_file, split_content,
    check_text_size, check_audio_duration
)

# This section imports necessary modules and functions for testing.

class TestCommon(unittest.TestCase):
    # This class defines a test case for the common utility functions.

    def test_generate_unique_filename(self):
        # Tests the generate_unique_filename function
        with patch('utils.common.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
            result = generate_unique_filename("test", ".txt")
            self.assertEqual(result, "test_20230101_120000.txt")
        # Mocks the datetime and checks if the generated filename is correct

    @patch('builtins.input', side_effect=['1'])
    def test_get_language_choice(self, mock_input):
        # Tests the get_language_choice function
        languages = {'1': ('English', 'en-US')}
        result = get_language_choice("Select language:", languages)
        self.assertEqual(result, ('English', 'en-US'))
        # Mocks user input and checks if the correct language is returned

    @patch('builtins.input', side_effect=['custom_name'])
    def test_get_filename(self, mock_input):
        # Tests the get_filename function
        result = get_filename("default", ".txt")
        self.assertEqual(result, "custom_name.txt")
        # Mocks user input and checks if the correct filename is returned

    @patch('utils.common.load_dotenv')
    @patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test_key',
        'GOOGLE_APPLICATION_CREDENTIALS': 'test_creds'
    })
    def test_load_env_variables(self, mock_load_dotenv):
        # Tests the load_env_variables function
        load_env_variables()
        mock_load_dotenv.assert_called_once()
        # Mocks environment variables and checks if load_dotenv is called

    @patch('builtins.open', new_callable=mock_open, read_data="test content")
    def test_read_text_file(self, mock_file):
        # Tests reading a text file
        content = read_file("test.txt")
        self.assertEqual(content, "test content")
        mock_file.assert_called_once_with("test.txt", 'r', encoding='utf-8')
        # Mocks file opening and checks if content is read correctly

    @patch('utils.common.PdfReader')
    def test_read_pdf_file(self, mock_pdf_reader):
        # Tests reading a PDF file
        mock_pdf = MagicMock()
        mock_pdf.pages = [MagicMock(extract_text=lambda: "page1"), MagicMock(extract_text=lambda: "page2")]
        mock_pdf_reader.return_value = mock_pdf
        content = read_file("test.pdf")
        self.assertEqual(content, "page1page2")
        # Mocks PDF reading and checks if content is extracted correctly

    @patch('utils.common.Document')
    def test_read_docx_file(self, mock_document):
        # Tests reading a DOCX file
        mock_doc = MagicMock()
        mock_doc.paragraphs = [MagicMock(text="para1"), MagicMock(text="para2")]
        mock_document.return_value = mock_doc
        content = read_file("test.docx")
        self.assertEqual(content, "para1\npara2")
        # Mocks DOCX reading and checks if content is extracted correctly

    @patch('builtins.open', new_callable=mock_open)
    def test_write_file(self, mock_file):
        # Tests writing to a file
        write_file("test content", "test.txt")
        mock_file.assert_called_once_with("test.txt", 'w', encoding='utf-8')
        mock_file().write.assert_called_once_with("test content")
        # Mocks file opening and checks if content is written correctly

    def test_split_content(self):
        # Tests the split_content function
        content = "This is a test. It has multiple sentences. Let's see how it splits."
        result = split_content(content, max_chars=20)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "This is a test.")
        # Checks if content is split correctly based on character limit

    def test_check_text_size(self):
        # Tests the check_text_size function
        small_text = "Small text"
        large_text = "Large text" * 1000
        self.assertFalse(check_text_size(small_text))
        self.assertTrue(check_text_size(large_text))
        # Checks if text size is correctly identified as small or large

    @patch('utils.common.wave.open')
    def test_check_audio_duration_wav(self, mock_wave_open):
        # Tests checking WAV audio duration
        mock_wave = MagicMock()
        mock_wave.getnframes.return_value = 48000
        mock_wave.getframerate.return_value = 16000
        mock_wave_open.return_value.__enter__.return_value = mock_wave

        result = check_audio_duration("test.wav")
        self.assertFalse(result)  # 3 seconds, not large

        mock_wave.getnframes.return_value = 1600000
        result = check_audio_duration("test.wav")
        self.assertTrue(result)  # 100 seconds, large
        # Mocks WAV file opening and checks if duration is correctly identified

    @patch('utils.common.AudioSegment.from_file')
    def test_check_audio_duration_mp3(self, mock_audio_segment):
        # Tests checking MP3 audio duration
        mock_audio = MagicMock()
        mock_audio.__len__.return_value = 30000  # 30 seconds
        mock_audio_segment.return_value = mock_audio

        result = check_audio_duration("test.mp3")
        self.assertFalse(result)

        mock_audio.__len__.return_value = 120000  # 120 seconds
        result = check_audio_duration("test.mp3")
        self.assertTrue(result)
        # Mocks MP3 file reading and checks if duration is correctly identified

if __name__ == '__main__':
    unittest.main()
    # Allows the test file to be run as a script