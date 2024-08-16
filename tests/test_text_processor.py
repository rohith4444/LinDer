import unittest
from unittest.mock import patch, MagicMock
from src.text.text_processor import translate_text_chunk, translate_large_text, translate_text, analyze_sentiment, summarize_text, process_text, process_file

class TestTextProcessor(unittest.TestCase):

    @patch('text.text_processor.translate_text')
    @patch('text.text_processor.analyze_sentiment')
    @patch('text.text_processor.summarize_text')
    def test_process_text(self, mock_summarize, mock_analyze, mock_translate):
        # Test translation
        process_text("Hello", 'translate', source_lang='en', target_lang='es')
        mock_translate.assert_called_once_with("Hello", 'en', 'es')

        # Test sentiment analysis
        process_text("Great day!", 'analyze_sentiment')
        mock_analyze.assert_called_once_with("Great day!")

        # Test summarization
        process_text("Long text...", 'summarize', max_words=10)
        mock_summarize.assert_called_once_with("Long text...", 10)

        # Test invalid operation
        result = process_text("Test", 'invalid_op')
        self.assertIsNone(result)

    @patch('text.text_processor.read_file')
    @patch('text.text_processor.process_text')
    @patch('text.text_processor.write_file')
    def test_process_file(self, mock_write, mock_process, mock_read):
        mock_read.return_value = "File content"
        mock_process.return_value = "Processed content"

        result = process_file("input.txt", "output.txt", 'translate', source_lang='en', target_lang='es')

        mock_read.assert_called_once_with("input.txt")
        mock_process.assert_called_once_with("File content", 'translate', source_lang='en', target_lang='es')
        mock_write.assert_called_once_with("Processed content", "output.txt")
        self.assertEqual(result, "output.txt")

        # Test processing failure
        mock_process.return_value = None
        result = process_file("input.txt", "output.txt", 'translate', source_lang='en', target_lang='es')
        self.assertIsNone(result)

    @patch('text.text_processor.openai_client.chat.completions.create')
    def test_translate_text_chunk(self, mock_create):
        # Setup mock
        mock_create.return_value.choices[0].message.content = "Translated text"

        result = translate_text_chunk("Test text", "en", "es")
        self.assertEqual(result, "Translated text")

        mock_create.assert_called_once()

    @patch('text.text_processor.translate_text_chunk')
    @patch('text.text_processor.split_content')
    def test_translate_large_text(self, mock_split, mock_translate_chunk):
        # Setup mocks
        mock_split.return_value = ["Chunk1", "Chunk2"]
        mock_translate_chunk.side_effect = ["Translated1", "Translated2"]

        result = translate_large_text("Large text", "en", "es")
        self.assertEqual(result, "Translated1 Translated2")

        mock_split.assert_called_once_with("Large text", 4000)
        self.assertEqual(mock_translate_chunk.call_count, 2)

    @patch('text.text_processor.check_text_size')
    @patch('text.text_processor.translate_large_text')
    @patch('text.text_processor.translate_text_chunk')
    def test_translate_text(self, mock_chunk, mock_large, mock_check_size):
        # Test small text
        mock_check_size.return_value = False
        mock_chunk.return_value = "Translated small"

        result = translate_text("Small text", "en", "es")
        self.assertEqual(result, "Translated small")
        mock_chunk.assert_called_once()
        mock_large.assert_not_called()

        # Test large text
        mock_check_size.return_value = True
        mock_large.return_value = "Translated large"

        result = translate_text("Large text", "en", "es")
        self.assertEqual(result, "Translated large")
        mock_large.assert_called_once()

    @patch('text.text_processor.openai_client.chat.completions.create')
    def test_analyze_sentiment(self, mock_create):
        mock_create.return_value.choices[0].message.content = "Positive"

        result = analyze_sentiment("Great day!")
        self.assertEqual(result, "Positive")

        mock_create.assert_called_once()

    @patch('text.text_processor.openai_client.chat.completions.create')
    def test_summarize_text(self, mock_create):
        mock_create.return_value.choices[0].message.content = "Summary"

        result = summarize_text("Long text to summarize", max_words=10)
        self.assertEqual(result, "Summary")

        mock_create.assert_called_once()

if __name__ == '__main__':
    unittest.main()