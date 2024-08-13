# Speech and Text Processing Application

This application provides various speech and text processing capabilities, including speech-to-text, text-to-speech, translation, sentiment analysis, and text summarization.

## Features

- Speech to Text conversion
- Text to Speech conversion
- Text Translation
- Sentiment Analysis
- Text Summarization
- Speech to Speech Translation

## Prerequisites

- Python 3.7 or higher
- Google Cloud account with Speech-to-Text and Text-to-Speech APIs enabled
- OpenAI API key

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/speech-text-processing-app.git
   cd speech-text-processing-app
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   Create a `.env` file in the project root and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   GOOGLE_APPLICATION_CREDENTIALS=./secrets/your_credentials_file.json
   ```

## Setting up Google Cloud Credentials

1. Obtain your Google Cloud credentials JSON file from the Google Cloud Console.

2. Create a `secrets` directory in the project root:
   ```
   mkdir secrets
   ```

3. Place your Google Cloud credentials JSON file in the `secrets` directory.

4. Ensure that your `.env` file has the `GOOGLE_APPLICATION_CREDENTIALS` variable pointing to this file:
   ```
   GOOGLE_APPLICATION_CREDENTIALS=./secrets/your_credentials_file.json
   ```

Note: The `secrets` directory is git-ignored to prevent accidental commits of sensitive information. Make sure to securely share the credentials file with team members through a secure channel, not through version control.

## Logging

This project uses a comprehensive logging system to track operations and aid in debugging. For more information on how logging is implemented and how to use it in development, please see the [Logging Documentation](docs/logging.md).

## Usage

Run the main application:
```
python src/main.py
```

Follow the on-screen prompts to use the various features of the application.

## Running Tests

To run the unit tests:
```
python -m unittest discover tests
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

