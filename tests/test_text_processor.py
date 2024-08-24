import unittest
from unittest.mock import patch, MagicMock
from src.text.text_processor import translate_text_chunk, translate_large_text, translate_text, analyze_sentiment, summarize_text, process_text, process_file

# This line imports the unittest module and necessary functions from unittest.mock and the module being tested.

class TestTextProcessor(unittest.TestCase):
    # This class defines a test case for the text_processor module. It inherits from unittest.TestCase.

    @patch('text.text_processor.translate_text')
    @patch('text.text_processor.analyze_sentiment')
    @patch('text.text_processor.summarize_text')
    def test_process_text(self, mock_summarize, mock_analyze, mock_translate):
        # This test method checks the process_text function with different operations.
        # It uses patch decorators to mock the translate_text, analyze_sentiment, and summarize_text functions.

        # Test translation
        process_text("Hello", 'translate', source_lang='en', target_lang='es')
        mock_translate.assert_called_once_with("Hello", 'en', 'es')
        # Calls process_text with 'translate' operation and asserts that mock_translate was called with correct arguments.

        # Test sentiment analysis
        process_text("Great day!", 'analyze_sentiment')
        mock_analyze.assert_called_once_with("Great day!")
        # Calls process_text with 'analyze_sentiment' operation and asserts that mock_analyze was called correctly.

        # Test summarization
        process_text("Long text...", 'summarize', max_words=10)
        mock_summarize.assert_called_once_with("Long text...", 10)
        # Calls process_text with 'summarize' operation and asserts that mock_summarize was called correctly.

        # Test invalid operation
        result = process_text("Test", 'invalid_op')
        self.assertIsNone(result)
        # Tests process_text with an invalid operation and asserts that it returns None.

    @patch('text.text_processor.read_file')
    @patch('text.text_processor.process_text')
    @patch('text.text_processor.write_file')
    def test_process_file(self, mock_write, mock_process, mock_read):
        # This test method checks the process_file function.
        # It mocks read_file, process_text, and write_file functions.

        mock_read.return_value = "File content"
        mock_process.return_value = "Processed content"
        # Sets up return values for the mocked functions.

        result = process_file("input.txt", "output.txt", 'translate', source_lang='en', target_lang='es')
        # Calls process_file with test parameters.

        mock_read.assert_called_once_with("input.txt")
        mock_process.assert_called_once_with("File content", 'translate', source_lang='en', target_lang='es')
        mock_write.assert_called_once_with("Processed content", "output.txt")
        self.assertEqual(result, "output.txt")
        # Asserts that the mocked functions were called correctly and checks the return value.

        # Test processing failure
        mock_process.return_value = None
        result = process_file("input.txt", "output.txt", 'translate', source_lang='en', target_lang='es')
        self.assertIsNone(result)
        # Tests the case where processing fails (returns None) and asserts that the result is None.

    @patch('text.text_processor.openai_client.chat.completions.create')
    def test_translate_text_chunk(self, mock_create):
        # This test method checks the translate_text_chunk function.
        # It mocks the OpenAI API call.

        mock_create.return_value.choices[0].message.content = "Translated text"
        # Sets up the mock to return a specific translation.

        result = translate_text_chunk("Test text", "en", "es")
        self.assertEqual(result, "Translated text")
        # Calls translate_text_chunk and asserts that it returns the expected translation.

        mock_create.assert_called_once()
        # Asserts that the mocked API was called once.

    @patch('text.text_processor.translate_text_chunk')
    @patch('text.text_processor.split_content')
    def test_translate_large_text(self, mock_split, mock_translate_chunk):
        # This test method checks the translate_large_text function.
        # It mocks split_content and translate_text_chunk functions.

        mock_split.return_value = ["Chunk1", "Chunk2"]
        mock_translate_chunk.side_effect = ["Translated1", "Translated2"]
        # Sets up the mocks to return specific values.

        result = translate_large_text("Large text", "en", "es")
        self.assertEqual(result, "Translated1 Translated2")
        # Calls translate_large_text and asserts that it returns the expected combined translation.

        mock_split.assert_called_once_with("Large text", 4000)
        self.assertEqual(mock_translate_chunk.call_count, 2)
        # Asserts that split_content was called once and translate_text_chunk was called twice.

    @patch('text.text_processor.check_text_size')
    @patch('text.text_processor.translate_large_text')
    @patch('text.text_processor.translate_text_chunk')
    def test_translate_text(self, mock_chunk, mock_large, mock_check_size):
        # This test method checks the translate_text function.
        # It tests both small and large text scenarios.

        # Test small text
        mock_check_size.return_value = False
        mock_chunk.return_value = "Translated small"

        result = translate_text("Small text", "en", "es")
        self.assertEqual(result, "Translated small")
        mock_chunk.assert_called_once()
        mock_large.assert_not_called()
        # Tests small text scenario and asserts that only translate_text_chunk was called.

        # Test large text
        mock_check_size.return_value = True
        mock_large.return_value = "Translated large"

        result = translate_text("Large text", "en", "es")
        self.assertEqual(result, "Translated large")
        mock_large.assert_called_once()
        # Tests large text scenario and asserts that translate_large_text was called.

    @patch('text.text_processor.openai_client.chat.completions.create')
    def test_analyze_sentiment(self, mock_create):
        # This test method checks the analyze_sentiment function.
        # It mocks the OpenAI API call.

        mock_create.return_value.choices[0].message.content = "Positive"

        result = analyze_sentiment("Great day!")
        self.assertEqual(result, "Positive")

        mock_create.assert_called_once()
        # Calls analyze_sentiment and asserts that it returns the expected sentiment and that the API was called once.

    @patch('text.text_processor.openai_client.chat.completions.create')
    def test_summarize_text(self, mock_create):
        # This test method checks the summarize_text function.
        # It mocks the OpenAI API call.

        mock_create.return_value.choices[0].message.content = "Summary"

        result = summarize_text("Long text to summarize", max_words=10)
        self.assertEqual(result, "Summary")

        mock_create.assert_called_once()
        # Calls summarize_text and asserts that it returns the expected summary and that the API was called once.

if __name__ == '__main__':
    unittest.main()
    # This block allows the test file to be run as a script, executing all the tests.