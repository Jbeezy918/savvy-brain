from pathlib import Path
from playwright.sync_api import sync_playwright
from src.tools.key_vault import save_key

VAULT = Path.home() / ".govcon_vault/sessions"

SERVICES = {
    "usajobs": ("https://developer.usajobs.gov/APIRequest/Index", "USAJOBS_API_KEY"),
    "adzuna": ("https://developer.adzuna.com/signup", "ADZUNA_APP_KEY"),
    "linkedin": ("https://www.linkedin.com/developers/apps", "LINKEDIN_CLIENT_SECRET"),
    "google": ("https://console.cloud.google.com/apis/credentials", "GOOGLE_API_KEY"),
    "facebook": ("https://developers.facebook.com/apps/", "FACEBOOK_APP_SECRET"),
    "telegram": ("https://t.me/BotFather", "TELEGRAM_BOT_TOKEN"),
    "newsapi": ("https://newsapi.org/register", "NEWSAPI_KEY"),
    "gnews": ("https://gnews.io/", "GNEWS_API_KEY"),
    "openweather": ("https://home.openweathermap.org/api_keys", "OPENWEATHER_API_KEY"),
    "newsapi": ("https://newsapi.org/register", "NEWSAPI_KEY"),
    "gnews": ("https://gnews.io/", "GNEWS_API_KEY"),
    "openweather": ("https://home.openweathermap.org/api_keys", "OPENWEATHER_API_KEY"),
    "newsapi": ("https://newsapi.org/register", "NEWSAPI_KEY"),
    "gnews": ("https://gnews.io/", "GNEWS_API_KEY"),
    "openweather": ("https://home.openweathermap.org/api_keys", "OPENWEATHER_API_KEY"),
}

def collect_key(service):
    if service not in SERVICES:
        return f"Unknown service: {service}"

    url, env_name = SERVICES[service]
    VAULT.mkdir(parents=True, exist_ok=True)
    state = VAULT / f"{service}.json"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=str(state)) if state.exists() else browser.new_context()
        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded")

        print(f"Opened {service}: {url}")
        print("Do the site clicks/login. Copy the key. Paste it here.")
        key = input(f"{env_name}: ").strip()

        if key:
            save_key(env_name, key)
            msg = f"Saved {env_name} to vault."
        else:
            msg = "No key entered."

        context.storage_state(path=str(state))
        browser.close()
        return msg

if __name__ == "__main__":
    import sys
    print(collect_key(sys.argv[1]))
