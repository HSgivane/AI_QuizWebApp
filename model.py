import requests, os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

def ask_openrouter(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        session.mount('https://', HTTPAdapter(max_retries=retries))

        r = session.post(url, headers=headers, json=data, timeout=60)
        r.raise_for_status()
        response = r.json()
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Ошибка: {e}\n\nОтвет от сервера:\n{r.text if 'r' in locals() else ''}"
