import io, os, re, json, textwrap, pathlib

APP = os.path.expanduser("~/Documents/AI_Relay_Files/relay_finisher/app.py")
with io.open(APP, "r", encoding="utf-8") as f:
    src = f.read()
orig = src

def add_imports(s):
    needed = ["platform", "subprocess", "requests"]
    for mod in needed:
        if not re.search(rf"\bimport\s+{mod}\b", s):
            s = "import " + mod + "\n" + s
    # our modules
    if "import tts" not in s:
        s = "import tts\n" + s
    if "import memory" not in s:
        s = "import memory\n" + s
    return s

VAULT_HELPERS = r'''
def _first_existing_env_file():
    for p in [
        os.path.expanduser("~/Documents/AI_Relay_Files/vault/.env"),
        os.path.expanduser("~/Documents/AI_Relay_Files/ENV/.env"),
        os.path.expanduser("~/.env"),
    ]:
        if os.path.isfile(p):
            return p
    return None

def _parse_dotenv(path:str)->dict:
    vals={}
    try:
        with open(path,"r",encoding="utf-8") as fh:
            for line in fh:
                line=line.strip()
                if not line or line.startswith("#"): continue
                if "=" in line:
                    k,v=line.split("=",1)
                    vals[k.strip()]=v.strip().strip('"').strip("'")
    except Exception: pass
    return vals

def load_env_from_vault()->dict:
    env_file=_first_existing_env_file()
    vals=_parse_dotenv(env_file) if env_file else {}
    # merge with process env
    for k in ["OPENAI_API_KEY","ANTHROPIC_API_KEY","GEMINI_API_KEY","ELEVENLABS_API_KEY","ELEVENLABS_VOICE_ID"]:
        if k in os.environ:
            vals[k]=os.environ[k]
    for k,v in vals.items():
        if k not in os.environ:
            os.environ[k]=v
    return vals
'''

def ensure_vault_helpers(s):
    if "def load_env_from_vault()" in s:
        return s
    # after first function or after imports
    m = re.search(r"\ndef\s+\w+\s*\(", s)
    if m:
        idx = m.start()
        return s[:idx] + "\n" + VAULT_HELPERS + "\n" + s[idx:]
    return s + "\n" + VAULT_HELPERS

SIDEBAR_BLOCK = r'''
# ===== Sidebar: Voice & Keys =====
env_vals = load_env_from_vault()

with st.sidebar:
    st.markdown("### 🔊 Jenny Voice")
    voice_enabled = st.checkbox("Speak replies out loud", value=True, key="jenny_voice_enabled")
    jenny_voice = st.text_input("Voice (macOS)", value=st.session_state.get("jenny_voice_name","Samantha"))
    st.session_state["jenny_voice_name"] = jenny_voice
    jenny_rate = st.slider("Speech rate (WPM)", 120, 240, 175, 5, key="jenny_voice_rate")
    st.caption("Tip: 160–190 sounds natural.")
    st.divider()
    st.markdown("### 🔐 Keys from Vault")
    col1,col2,col3 = st.columns(3)
    col1.metric("OpenAI", "🟢" if env_vals.get("OPENAI_API_KEY") else "🔴")
    col2.metric("Anthropic", "🟢" if env_vals.get("ANTHROPIC_API_KEY") else "🔴")
    col3.metric("Gemini", "🟢" if env_vals.get("GEMINI_API_KEY") else "🔴")
    st.caption("Optional: ElevenLabs for higher-quality TTS if present.")
    st.caption(("ElevenLabs ✅" if env_vals.get("ELEVENLABS_API_KEY") else "ElevenLabs ❌") + " • Voice ID: " + (env_vals.get("ELEVENLABS_VOICE_ID","(default)")))
'''

def insert_sidebar(s):
    if "### 🔊 Jenny Voice" in s:
        return s
    m = re.search(r"st\.set_page_config\([^\)]*\)\s*", s)
    if not m:
        return s + "\n" + SIDEBAR_BLOCK
    idx = m.end()
    return s[:idx] + "\n\n" + SIDEBAR_BLOCK + s[idx:]

# Hook: clean user text before sending + save memory after replies
CLEAN_HOOK = r'''
# Clean the user's message for saving (fuzzy de-ramble)
cleaned_msg = memory.fuzzy_clean_user_text(new_msg)
'''

SAVE_AND_SPEAK_HOOK = r'''
# Determine a single canonical Jenny reply (pref order)
pref = (replies.get("Jenny (OpenAI)")
        or replies.get("Jenny (Anthropic)")
        or replies.get("Jenny (Gemini)")
        or next((v for k,v in replies.items() if "Jenny" in k), None))

# Save turn with rolling profile update if possible
summary = memory.rolling_summarize_if_needed(env_vals.get("OPENAI_API_KEY"), st.session_state.conversation_history)
memory.save_turn(raw_user=new_msg, cleaned_user=cleaned_msg, replies=replies,
                 models=[k for k in replies.keys()], context_summary=summary)

# Auto speak
if pref and st.session_state.get("jenny_voice_enabled", True):
    tts.ding()
    tts.speak(pref,
              enabled=True,
              voice=st.session_state.get("jenny_voice_name"),
              rate=st.session_state.get("jenny_voice_rate"),
              eleven_api_key=env_vals.get("ELEVENLABS_API_KEY"),
              eleven_voice_id=env_vals.get("ELEVENLABS_VOICE_ID"))
'''

def add_clean_and_save_hooks(s):
    # after user submits and before API calls, insert CLEAN_HOOK once
    if "fuzzy_clean_user_text" not in s:
        # find "new_msg =" capture area: already have new_msg variable
        s = re.sub(r"st\.session_state\.chat_log \+= .*?\n", lambda m: m.group(0)+CLEAN_HOOK, s, count=1, flags=re.S)
    # after replies loop, add SAVE_AND_SPEAK_HOOK
    if "memory.save_turn(" not in s:
        anchor = re.search(r"\nfor\s+who,\s*text\s+in\s+replies\.items\(\):\s*\n", s)
        if anchor:
            # find end of loop by dedent
            start = anchor.end()
            lines = s[start:].splitlines(True)
            indent = None; end_off = 0
            for i, line in enumerate(lines):
                if indent is None:
                    m = re.match(r"(\s+)\S", line)
                    if m: indent = len(m.group(1))
                    continue
                if line.strip()=="":
                    continue
                m = re.match(r"(\s*)\S", line)
                if m and len(m.group(1)) < indent:
                    end_off = i; break
            else:
                end_off = len(lines)
            insert_at = start + sum(len(l) for l in lines[:end_off])
            s = s[:insert_at] + "\n" + SAVE_AND_SPEAK_HOOK + s[insert_at:]
    return s

# Improve Gemini: use system-like header + role-tagged content (keeps your current approach but cleaner text packing)
def improve_gemini_block(s):
    if "gemini_text" not in s:
        return s
    s = re.sub(r'gemini_text\s*=\s*""', 'gemini_text = ""', s)
    # keep as is; already packing system + history. (Full systemInstruction switch can be done later if desired.)
    return s

# Make sure page title set
def ensure_title(s):
    s = re.sub(r'st\.set_page_config\(page_title="[^"]*",\s*layout="wide"\)',
               'st.set_page_config(page_title="Jenny AI Assistant", layout="wide")',
               s)
    return s

src = add_imports(src)
src = ensure_vault_helpers(src)
src = insert_sidebar(src)
src = add_clean_and_save_hooks(src)
src = improve_gemini_block(src)
src = ensure_title(src)

if src != orig:
    with io.open(APP, "w", encoding="utf-8") as f:
        f.write(src)
    print("✅ Applied voice+memory+vault patch to:", APP)
else:
    print("ℹ️ No changes (already patched).")
