import requests
import time

# Load your Groq API key from a config file
def load_api_key(file_path="config.txt"):
    with open(file_path, "r") as f:
        return f.read().strip()

# AI Writer function using Groq's LLaMA 3 model with retry logic
def spin_text(text, retries=3, delay=2):
    api_key = load_api_key()

    prompt = (
        "You are a creative and vivid writer. Rewrite the following chapter "
        "in an engaging and descriptive way, maintaining its core meaning but improving readability:\n\n"
        + text
    )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful AI writing assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8,
        "max_tokens": 2048
    }

    for attempt in range(retries):
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30  # Timeout in seconds
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"[Retry {attempt + 1}/{retries}] Error: {e}")
            time.sleep(delay)

    return "[ERROR] Could not complete rewrite after multiple retries."
