# todos/utils.py
import requests

def translate_text(text, target_language):
    url = "https://api.mymemory.translated.net/get"
    params = {
        'q': text,
        'langpair': f'en|{target_language}'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    result = response.json()
    return result['responseData']['translatedText']
