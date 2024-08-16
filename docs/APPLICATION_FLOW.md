# Application Flow Documentation

This document outlines the flow of method calls for each feature in our Speech and Text Processing Application.

## 1. Speech to Text (Same Language)
```
main.py: handle_speech_to_text
├── common.py: get_language_choice
├── speech_processor.py: record_audio
│   └── common.py: generate_unique_filename
├── speech_processor.py: process_audio
    └── speech_processor.py: transcribe_audio or transcribe_large_audio
        └── speech_processor.py: speech_client.recognize
```

## 2. Speech to Text with Translation
```
main.py: handle_speech_to_text
├── common.py: get_language_choice
├── speech_processor.py: record_audio
│   └── common.py: generate_unique_filename
├── speech_processor.py: process_audio
│   └── speech_processor.py: transcribe_audio or transcribe_large_audio
│       └── speech_processor.py: speech_client.recognize
└── text_processor.py: process_text
    └── text_processor.py: translate_text
        └── text_processor.py: translate_text_chunk or translate_large_text
            └── text_processor.py: openai_client.chat.completions.create
```

## 3. Text to Speech (Same Language)
```
main.py: handle_text_to_speech
├── common.py: get_language_choice
├── speech_processor.py: process_audio
│   └── speech_processor.py: text_to_speech or text_to_speech_large
│       └── speech_processor.py: tts_client.synthesize_speech
├── speech_processor.py: play_audio
└── speech_processor.py: save_audio or save_large_audio (if user chooses to save)
    └── common.py: write_file
```

## 4. Text to Speech with Translation
```
main.py: handle_text_to_speech
├── common.py: get_language_choice
├── text_processor.py: process_text
│   └── text_processor.py: translate_text
│       └── text_processor.py: translate_text_chunk or translate_large_text
│           └── text_processor.py: openai_client.chat.completions.create
├── speech_processor.py: process_audio
│   └── speech_processor.py: text_to_speech or text_to_speech_large
│       └── speech_processor.py: tts_client.synthesize_speech
├── speech_processor.py: play_audio
└── speech_processor.py: save_audio or save_large_audio (if user chooses to save)
    └── common.py: write_file
```

## 5. Text Translation
```
main.py: handle_text_translation
├── common.py: get_language_choice
└── text_processor.py: process_text
    └── text_processor.py: translate_text
        └── text_processor.py: translate_text_chunk or translate_large_text
            └── text_processor.py: openai_client.chat.completions.create
```

## 6. Speech to Speech Translation
```
main.py: handle_speech_to_speech
├── common.py: get_language_choice
├── speech_processor.py: record_audio
│   └── common.py: generate_unique_filename
├── speech_processor.py: process_audio
│   ├── speech_processor.py: transcribe_audio or transcribe_large_audio
│   │   └── speech_processor.py: speech_client.recognize
│   └── text_processor.py: process_text
│       └── text_processor.py: translate_text
│           └── text_processor.py: translate_text_chunk or translate_large_text
│               └── text_processor.py: openai_client.chat.completions.create
├── speech_processor.py: process_audio
│   └── speech_processor.py: text_to_speech or text_to_speech_large
│       └── speech_processor.py: tts_client.synthesize_speech
├── speech_processor.py: play_audio
└── speech_processor.py: save_audio or save_large_audio (if user chooses to save)
    └── common.py: write_file
```

## 7. Document Translation
```
main.py: handle_document_translation
├── common.py: get_language_choice
├── text_processor.py: process_file
    ├── common.py: read_file
    ├── text_processor.py: process_text
    │   └── text_processor.py: translate_text
    │       └── text_processor.py: translate_text_chunk or translate_large_text
    │           └── text_processor.py: openai_client.chat.completions.create
    └── common.py: write_file
```

## 8. Generate Audio Book
```
main.py: handle_audio_book_generation
├── common.py: get_language_choice
├── common.py: read_file
├── text_processor.py: process_text (if source_lang != target_lang)
│   └── text_processor.py: translate_text
│       └── text_processor.py: translate_text_chunk or translate_large_text
│           └── text_processor.py: openai_client.chat.completions.create
├── speech_processor.py: process_audio
│   └── speech_processor.py: text_to_speech or text_to_speech_large
│       └── speech_processor.py: tts_client.synthesize_speech
├── speech_processor.py: save_audio or save_large_audio
└── speech_processor.py: play_audio (if user chooses to play)
```

## 9. Audio File to Text File (with Translation)
```
main.py: handle_audio_to_text_translation
├── common.py: get_language_choice
├── speech_processor.py: process_audio_file
│   ├── speech_processor.py: process_audio
│   │   └── speech_processor.py: transcribe_audio or transcribe_large_audio
│   │       └── speech_processor.py: speech_client.recognize
│   └── text_processor.py: process_text
│       └── text_processor.py: translate_text
│           └── text_processor.py: translate_text_chunk or translate_large_text
│               └── text_processor.py: openai_client.chat.completions.create
└── common.py: write_file
```

## 10. Audio File to Audio File Translation
```
main.py: handle_audio_to_audio_translation
├── common.py: get_language_choice
└── speech_processor.py: process_audio_file
    ├── speech_processor.py: process_audio
    │   ├── speech_processor.py: transcribe_audio or transcribe_large_audio
    │   │   └── speech_processor.py: speech_client.recognize
    │   └── text_processor.py: process_text
    │       └── text_processor.py: translate_text
    │           └── text_processor.py: translate_text_chunk or translate_large_text
    │               └── text_processor.py: openai_client.chat.completions.create
    └── speech_processor.py: text_to_speech or text_to_speech_large
        └── speech_processor.py: tts_client.synthesize_speech
```

## 11. Sentiment Analysis
```
main.py: handle_sentiment_analysis
└── text_processor.py: process_text
    └── text_processor.py: analyze_sentiment
        └── text_processor.py: openai_client.chat.completions.create
```

## 12. Text Summarization
```
main.py: handle_text_summarization
└── text_processor.py: process_text
    └── text_processor.py: summarize_text
        └── text_processor.py: openai_client.chat.completions.create
```

This document provides a comprehensive overview of the method call flow for each feature in our application. It serves as a valuable reference for understanding the application's architecture and the interactions between different modules.