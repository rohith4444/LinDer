import unittest
from unittest.mock import patch, MagicMock
from src.speech.speech_processor import process_audio, process_audio_file, transcribe_audio, transcribe_large_audio, text_to_speech, text_to_speech_large

class TestSpeechProcessor(unittest.TestCase):

    @patch('speech.speech_processor.transcribe_large_audio')
    @patch('speech.speech_processor.transcribe_audio')
    @patch('speech.speech_processor.text_to_speech_large')
    @patch('speech.speech_processor.text_to_speech')
    def test_process_audio(self, mock_tts, mock_tts_large, mock_transcribe, mock_transcribe_large):
        # Test transcription of small audio
        mock_transcribe.return_value = "Transcribed text"
        result = process_audio(b'small_audio_content', 'transcribe', language_code='en-US')
        self.assertEqual(result, "Transcribed text")
        mock_transcribe.assert_called_once()
        mock_transcribe_large.assert_not_called()

        # Test transcription of large audio
        mock_transcribe_large.return_value = "Transcribed large text"
        result = process_audio(b'large_audio_content' * 1000000, 'transcribe', language_code='en-US')
        self.assertEqual(result, "Transcribed large text")
        mock_transcribe_large.assert_called_once()

        # Test text-to-speech for small text
        mock_tts.return_value = b'audio_content'
        result = process_audio("Small text", 'text_to_speech', language_code='en-US', voice_gender='FEMALE')
        self.assertEqual(result, b'audio_content')
        mock_tts.assert_called_once()
        mock_tts_large.assert_not_called()

        # Test text-to-speech for large text
        mock_tts_large.return_value = [b'audio_content1', b'audio_content2']
        result = process_audio("Large text" * 1000, 'text_to_speech', language_code='en-US', voice_gender='FEMALE')
        self.assertEqual(result, [b'audio_content1', b'audio_content2'])
        mock_tts_large.assert_called_once()

    @patch('speech.speech_processor.process_audio')
    @patch('speech.speech_processor.write_file')
    @patch('speech.speech_processor.save_audio')
    def test_process_audio_file(self, mock_save_audio, mock_write_file, mock_process_audio):
        mock_process_audio.return_value = "Processed content"
        
        # Test transcribe operation
        result = process_audio_file('input.wav', 'output.txt', 'transcribe', language_code='en-US')
        self.assertEqual(result, 'output.txt')
        mock_write_file.assert_called_once_with("Processed content", 'output.txt')

        # Test text_to_speech operation
        mock_process_audio.return_value = b'audio_content'
        result = process_audio_file('input.txt', 'output.mp3', 'text_to_speech', language_code='en-US', voice_gender='FEMALE')
        self.assertEqual(result, 'output.mp3')
        mock_save_audio.assert_called_once_with(b'audio_content', 'output')

    @patch('speech.speech_processor.speech_client.recognize')
    def test_transcribe_audio(self, mock_recognize):
        mock_response = MagicMock()
        mock_response.results = [MagicMock(alternatives=[MagicMock(transcript="Transcribed text")])]
        mock_recognize.return_value = mock_response

        result = transcribe_audio(b'audio_content', 'en-US')
        self.assertEqual(result, "Transcribed text")
        mock_recognize.assert_called_once()

    @patch('speech.speech_processor.speech_client.long_running_recognize')
    def test_transcribe_large_audio(self, mock_long_recognize):
        mock_operation = MagicMock()
        mock_operation.result.return_value.results = [
            MagicMock(alternatives=[MagicMock(transcript="Transcribed large text part 1")]),
            MagicMock(alternatives=[MagicMock(transcript="Transcribed large text part 2")])
        ]
        mock_long_recognize.return_value = mock_operation

        result = transcribe_large_audio(b'large_audio_content', 'en-US')
        self.assertEqual(result, "Transcribed large text part 1 Transcribed large text part 2")
        mock_long_recognize.assert_called_once()

    @patch('speech.speech_processor.tts_client.synthesize_speech')
    def test_text_to_speech(self, mock_synthesize):
        mock_synthesize.return_value = MagicMock(audio_content=b'synthesized_audio')

        result = text_to_speech("Test text", 'en-US', 'FEMALE')
        self.assertEqual(result, b'synthesized_audio')
        mock_synthesize.assert_called_once()

    @patch('speech.speech_processor.text_to_speech')
    @patch('speech.speech_processor.split_content')
    def test_text_to_speech_large(self, mock_split, mock_tts):
        mock_split.return_value = ["Chunk1", "Chunk2"]
        mock_tts.side_effect = [b'audio1', b'audio2']

        result = text_to_speech_large("Large text", 'en-US', 'FEMALE')
        self.assertEqual(result, [b'audio1', b'audio2'])
        self.assertEqual(mock_tts.call_count, 2)
        mock_split.assert_called_once_with("Large text", 5000)

if __name__ == '__main__':
    unittest.main()