import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
from datetime import datetime
from src.utils.common import (
    generate_unique_filename, get_language_choice, get_filename,
    load_env_variables, read_file, write_file, split_content,
    check_text_size, check_audio_duration
)

class TestCommon(unittest.TestCase):

    def test_generate_unique_filename(self):
        with patch('utils.common.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
            result = generate_unique_filename("test", ".txt")
            self.assertEqual(result, "test_20230101_120000.txt")

    @patch('builtins.input', side_effect=['1'])
    def test_get_language_choice(self, mock_input):
        languages = {'1': ('English', 'en-US')}
        result = get_language_choice("Select language:", languages)
        self.assertEqual(result, ('English', 'en-US'))

    @patch('builtins.input', side_effect=['custom_name'])
    def test_get_filename(self, mock_input):
        result = get_filename("default", ".txt")
        self.assertEqual(result, "custom_name.txt")

    @patch('utils.common.load_dotenv')
    @patch.dict(os.environ, {
        'OPENAI_API_KEY': 'test_key',
        'GOOGLE_APPLICATION_CREDENTIALS': 'test_creds'
    })
    def test_load_env_variables(self, mock_load_dotenv):
        load_env_variables()
        mock_load_dotenv.assert_called_once()

    @patch('builtins.open', new_callable=mock_open, read_data="test content")
    def test_read_text_file(self, mock_file):
        content = read_file("test.txt")
        self.assertEqual(content, "test content")
        mock_file.assert_called_once_with("test.txt", 'r', encoding='utf-8')

    @patch('utils.common.PdfReader')
    def test_read_pdf_file(self, mock_pdf_reader):
        mock_pdf = MagicMock()
        mock_pdf.pages = [MagicMock(extract_text=lambda: "page1"), MagicMock(extract_text=lambda: "page2")]
        mock_pdf_reader.return_value = mock_pdf
        content = read_file("test.pdf")
        self.assertEqual(content, "page1page2")

    @patch('utils.common.Document')
    def test_read_docx_file(self, mock_document):
        mock_doc = MagicMock()
        mock_doc.paragraphs = [MagicMock(text="para1"), MagicMock(text="para2")]
        mock_document.return_value = mock_doc
        content = read_file("test.docx")
        self.assertEqual(content, "para1\npara2")

    @patch('builtins.open', new_callable=mock_open)
    def test_write_file(self, mock_file):
        write_file("test content", "test.txt")
        mock_file.assert_called_once_with("test.txt", 'w', encoding='utf-8')
        mock_file().write.assert_called_once_with("test content")

    def test_split_content(self):
        content = "This is a test. It has multiple sentences. Let's see how it splits."
        result = split_content(content, max_chars=20)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], "This is a test.")

    def test_check_text_size(self):
        small_text = "Small text"
        large_text = "Large text" * 1000
        self.assertFalse(check_text_size(small_text))
        self.assertTrue(check_text_size(large_text))

    @patch('utils.common.wave.open')
    def test_check_audio_duration_wav(self, mock_wave_open):
        mock_wave = MagicMock()
        mock_wave.getnframes.return_value = 48000
        mock_wave.getframerate.return_value = 16000
        mock_wave_open.return_value.__enter__.return_value = mock_wave

        result = check_audio_duration("test.wav")
        self.assertFalse(result)  # 3 seconds, not large

        mock_wave.getnframes.return_value = 1600000
        result = check_audio_duration("test.wav")
        self.assertTrue(result)  # 100 seconds, large

    @patch('utils.common.AudioSegment.from_file')
    def test_check_audio_duration_mp3(self, mock_audio_segment):
        mock_audio = MagicMock()
        mock_audio.__len__.return_value = 30000  # 30 seconds
        mock_audio_segment.return_value = mock_audio

        result = check_audio_duration("test.mp3")
        self.assertFalse(result)

        mock_audio.__len__.return_value = 120000  # 120 seconds
        result = check_audio_duration("test.mp3")
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()