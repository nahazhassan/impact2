from flask import Flask, render_template, request
from newspaper import Article
import nltk
import torch
from transformers import pipeline

nltk.download('punkt')
# Removed nltk.download('punkt_tab') as it is not a valid resource
# Ensure 'punkt' is downloaded properly
import nltk
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Load summarization pipeline from transformers
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_webpage(url):
    try:
        article = Article(url)
        # Set user-agent header to improve download success
        article.user_agent = 'Mozilla/5.0'
        article.download()
        article.parse()
        article.nlp()
        # Check if summary attribute exists and is not empty
        if hasattr(article, 'summary') and article.summary:
            return article.summary
        else:
            # Fallback: use transformers summarizer on article text
            if article.text:
                max_chunk = 5000
                text = article.text.replace("\n", " ")
                sentences = text.split('. ')
                current_chunk = ''
                chunks = []
                for sentence in sentences:
                    if len(current_chunk) + len(sentence) + 1 <= max_chunk:
                        current_chunk += sentence + '. '
                    else:
                        chunks.append(current_chunk.strip())
                        current_chunk = sentence + '. '
                if current_chunk:
                    chunks.append(current_chunk.strip())

                summary = ''
                for chunk in chunks:
                    out = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
                    summary += out[0]['summary_text'] + ' '
                return summary.strip()
            else:
                return "Error summarizing webpage: No article text found."
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return f"Error summarizing webpage: {e}\nDetails:\n{error_details}"

def summarize_text(text):
    try:
        # Hugging Face summarization pipeline has max token limits, so chunk if needed
        max_chunk = 5000
        text = text.replace("\n", " ")
        sentences = text.split('. ')
        current_chunk = ''
        chunks = []
        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 1 <= max_chunk:
                current_chunk += sentence + '. '
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + '. '
        if current_chunk:
            chunks.append(current_chunk.strip())

        summary = ''
        for chunk in chunks:
            out = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
            summary += out[0]['summary_text'] + ' '

        return summary.strip()
    except Exception as e:
        return f"Error summarizing text: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = ''
    error = ''
    if request.method == 'POST':
        url = request.form.get('url')
        text = request.form.get('text')
        if url:
            summary = summarize_webpage(url)
        elif text:
            summary = summarize_text(text)
        else:
            error = "Please provide either a URL or text to summarize."
    return render_template('index.html', summary=summary, error=error)

from flask import jsonify

@app.route('/api/summarize', methods=['POST'])
def api_summarize():
    url = request.form.get('url')
    text = request.form.get('text')
    if not url and not text:
        return jsonify({'error': 'Please provide either a URL or text to summarize.'}), 400
    if url:
        summary = summarize_webpage(url)
    else:
        summary = summarize_text(text)
    return jsonify({'summary': summary})

import logging
import threading
import time
import os
import sys

logging.basicConfig(level=logging.INFO)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        logging.error("Shutdown function not found.")
        return False
    logging.info("Shutdown function found. Shutting down server...")
    func()
    return True

@app.route('/shutdown', methods=['POST'])
def shutdown():
    success = shutdown_server()
    if success:
        # Start a timer to force exit if shutdown hangs
        def force_exit():
            time.sleep(5)
            logging.error("Forcing server exit after timeout.")
            os._exit(0)
        threading.Thread(target=force_exit).start()
        return 'Server shutting down...'
    else:
        # Fallback: forcibly exit the process immediately
        logging.error("Forcing server exit as shutdown function not found.")
        os._exit(0)
        return 'Server shutdown function not found. Forcing exit.', 200

if __name__ == '__main__':
    # Disable reloader to avoid issues with shutdown
    app.run(debug=True, use_reloader=False)
