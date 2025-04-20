document.getElementById('summarizeBtn').addEventListener('click', async () => {
  const url = document.getElementById('urlInput').value.trim();
  const text = document.getElementById('textInput').value.trim();
  const errorDiv = document.getElementById('error');
  const summaryDiv = document.getElementById('summary');

  errorDiv.textContent = '';
  summaryDiv.textContent = '';

  if (!url && !text) {
    errorDiv.textContent = 'Please provide either a URL or text to summarize.';
    return;
  }

  const formData = new FormData();
  if (url) {
    formData.append('url', url);
  } else {
    formData.append('text', text);
  }

  document.getElementById('summarizeBtn').disabled = true;
  document.getElementById('summarizeBtn').textContent = 'Summarizing...';

  try {
    const response = await fetch('http://localhost:5000/api/summarize', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `Server error: ${response.statusText}`);
    }

    const data = await response.json();

    summaryDiv.textContent = data.summary || 'No summary found.';
  } catch (err) {
    errorDiv.textContent = `Error: ${err.message}`;
  } finally {
    document.getElementById('summarizeBtn').disabled = false;
    document.getElementById('summarizeBtn').textContent = 'Summarize';
  }
});
