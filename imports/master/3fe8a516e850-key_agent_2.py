import webbrowser
from src.tools.clipboard_vault import save_clipboard_key

LINKS = {
    "USAJOBS_API_KEY": "https://developer.usajobs.gov/APIRequest/Index",
    "ADZUNA_APP_KEY": "https://developer.adzuna.com/signup",
    "NEWSAPI_KEY": "https://newsapi.org/register",
    "GNEWS_API_KEY": "https://gnews.io/",
    "OPENWEATHER_API_KEY": "https://home.openweathermap.org/api_keys",
}

def open_key_site(key_name):
    url = LINKS.get(key_name)
    if not url:
        return "No URL mapped."
    webbrowser.open(url)
    return f"Opened {url}"

def save_from_clipboard(key_name):
    return save_clipboard_key(key_name)
