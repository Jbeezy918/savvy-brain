from pathlib import Path
from playwright.sync_api import sync_playwright

VAULT = Path.home() / ".govcon_vault/sessions"
WHITELIST = Path.home() / "GOVCON_AI/configs/session_whitelist.txt"

def allowed_domains():
    return [x.strip() for x in WHITELIST.read_text().splitlines() if x.strip()]

def save_session(domain):
    if domain not in allowed_domains():
        return f"BLOCKED: {domain} not whitelisted."

    VAULT.mkdir(parents=True, exist_ok=True)
    out = VAULT / f"{domain}.json"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"https://{domain}", wait_until="domcontentloaded")
        input(f"Log into {domain}, then press ENTER here to save session...")
        context.storage_state(path=str(out))
        browser.close()

    out.chmod(0o600)
    return f"Saved session: {out}"

def list_sessions():
    VAULT.mkdir(parents=True, exist_ok=True)
    return [p.name for p in VAULT.glob("*.json")]
