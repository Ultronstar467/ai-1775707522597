```javascript
document.addEventListener('DOMContentLoaded', () => {
    // IMPORTANT: Replace this with your actual AWS API Gateway Invoke URL
    // Example: https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com
    const API_BASE_URL = 'YOUR_API_GATEWAY_URL_HERE'; 

    const textInput = document.getElementById('textInput');
    const processBtn = document.getElementById('processBtn');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const resultDisplay = document.getElementById('resultDisplay');
    const originalTextSpan = document.getElementById('originalText');
    const processedTextSpan = document.getElementById('processedText');
    const timestampSpan = document.getElementById('timestamp');
    const processorInfoSpan = document.getElementById('processorInfo');
    const errorDisplay = document.getElementById('errorDisplay');
    const errorMessageP = document.getElementById('errorMessage');

    processBtn.addEventListener('click', async () => {
        const inputText = textInput.value.trim();

        // Clear previous results and errors
        resultDisplay.style.display = 'none';
        errorDisplay.style.display = 'none';
        errorMessageP.textContent = '';
        loadingIndicator.style.display = 'flex'; // Show loading indicator

        if (!inputText) {
            errorMessageP.textContent = "Input text cannot be empty!";
            errorDisplay.style.display = 'block';
            loadingIndicator.style.display = 'none';
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/run`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ input: inputText }),
            });

            const data = await response.json();

            if (response.ok) {
                originalTextSpan.textContent = data.original_input;
                processedTextSpan.textContent = data.processed_output;
                timestampSpan.textContent = new Date(data.timestamp).toLocaleString();
                processorInfoSpan.textContent = data.processor_info;
                resultDisplay.style.display = 'block';
            } else {
                // Handle API errors (e.g., validation errors from FastAPI)
                errorMessageP.textContent = data.detail || `Error: ${response.status} ${response.statusText}`;
                errorDisplay.style.display = 'block';
            }
        } catch (error) {
            console.error('Fetch error:', error);
            errorMessageP.textContent = `Network error or server unreachable: ${error.message}`;
            errorDisplay.style.display = 'block';
        } finally {
            loadingIndicator.style.display = 'none'; // Hide loading indicator
        }
    });
});
```