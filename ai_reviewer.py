import requests

def load_api_key(file_path="config.txt"):
    with open(file_path, "r") as f:
        return f.read().strip()

def review_text(text):
    api_key = load_api_key()

    prompt = (
        "You are an expert editor. Read the following rewritten chapter and suggest detailed improvements. "
        "Comment on tone, clarity, flow, grammar, and engagement. Give your suggestions as bullet points:\n\n"
        + text
    )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are an expert editorial reviewer."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1024
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"[ERROR] Reviewer failed: {str(e)}"
