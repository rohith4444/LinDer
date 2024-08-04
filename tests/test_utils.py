import unittest
from unittest.mock import patch
from src.utils.common import get_language_choice, get_filename, load_env_variables

class TestUtilityFunctions(unittest.TestCase):

    @patch('builtins.input', return_value='1')
    def test_get_language_choice(self, mock_input):
        languages = {
            "1": ("English", "en-US"),
            "2": ("Spanish", "es-ES")
        }
        result = get_language_choice("Select a language:", languages)
        self.assertEqual(result, ("English", "en-US"))

    @patch('builtins.input', return_value='')
    def test_get_filename_default(self, mock_input):
        result = get_filename("test", ".txt")
        self.assertEqual(result, "test.txt")

    @patch('builtins.input', return_value='custom')
    def test_get_filename_custom(self, mock_input):
        result = get_filename("test", ".txt")
        self.assertEqual(result, "custom.txt")

    @patch.dict('os.environ', {
        'OPENAI_API_KEY': 'test_key',
        'GOOGLE_APPLICATION_CREDENTIALS': 'test_path'
    })
    def test_load_env_variables_success(self):
        try:
            load_env_variables()
        except EnvironmentError:
            self.fail("load_env_variables() raised EnvironmentError unexpectedly!")

    @patch.dict('os.environ', {})
    def test_load_env_variables_failure(self):
        with self.assertRaises(EnvironmentError):
            load_env_variables()

if __name__ == '__main__':
    unittest.main()