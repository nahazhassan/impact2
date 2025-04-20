# AI Summarizer

This is a simple web application built with Flask that allows users to summarize either a webpage URL or raw text using state-of-the-art NLP models.

## Features

- Summarize the main content of any webpage by providing its URL.
- Summarize raw text input directly.
- Uses the `newspaper3k` library to extract article content from URLs.
- Uses Hugging Face's `transformers` pipeline with the `facebook/bart-large-cnn` model for summarization.
- Responsive and user-friendly web interface.
- Added a "Close Server" button in the web interface to gracefully terminate the Flask server.

## Requirements

- Python 3.7 or higher
- The following Python packages (listed in `requirements.txt`):
  - Flask
  - newspaper3k
  - nltk
  - torch
  - transformers

## Installation

1. Clone the repository or download the source code.

2. Navigate to the `ai_summarizer` directory:

   ```bash
   cd ai_summarizer
   ```

3. (Optional but recommended) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

4. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

5. Download necessary NLTK data:

   The app automatically downloads the `punkt` tokenizer data on startup, but if you want to download it manually, run:

   ```python
   python -m nltk.downloader punkt
   ```

## Usage

1. Run the Flask app:

   ```bash
   python app.py
   ```

2. Open your web browser and go to:

   ```
   http://127.0.0.1:5000/
   ```

3. Use the web interface to either:

   - Enter a URL of an article/webpage to summarize.
   - Or enter raw text to summarize.

4. Click the **Summarize** button to get the summary.

5. To stop the server, use the **Close Server** button on the web page. It will prompt for confirmation before shutting down the Flask server gracefully.

## Notes

- The summarization model has token limits, so long texts or articles are chunked and summarized in parts.
- The app uses a user-agent header to improve webpage download success.
- If you encounter errors related to missing NLTK data, ensure the `punkt` tokenizer is installed.

## License

This project is open source and free to use.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [newspaper3k](https://newspaper.readthedocs.io/en/latest/)
- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [NLTK](https://www.nltk.org/)
