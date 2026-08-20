import os
import psycopg2
from pypdf import PdfReader
import docx2txt

DB_PARAMS = {
    "dbname": "career_assistant",
    "user": "postgres",
    "password": "yourpassword",
    "host": "localhost",
    "port": "5432"
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge_base")

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == '.txt':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f: 
                return f.read()
        elif ext == '.pdf':
            return "".join([page.extract_text() or "" for page in PdfReader(file_path).pages])
        elif ext == '.docx':
            return docx2txt.process(file_path)
    except Exception:
        return ""
    return ""

def operationalize_memory():
    if not os.path.exists(KNOWLEDGE_DIR):
        print(f"📁 Structured knowledge directory built at: {KNOWLEDGE_DIR}")
        os.makedirs(KNOWLEDGE_DIR, exist_ok=True)
        return

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
    except Exception as e:
        print(f"❌ Database Connection Offline: {e}")
        print("💡 Ensure your local PostgreSQL server is running.")
        return
    
    print("🧠 Parsing master documents for AI memory synchronization...")
    sync_count = 0
    
    for category in os.listdir(KNOWLEDGE_DIR):
        cat_path = os.path.join(KNOWLEDGE_DIR, category)
        if not os.path.isdir(cat_path): 
            continue
        
        for file in os.listdir(cat_path):
            file_path = os.path.join(cat_path, file)
            text_content = extract_text(file_path).strip()
            if not text_content: 
                continue
            
            cur.execute("""
                INSERT INTO ai_memory_ledger (fact_key, fact_value, category)
                VALUES (%s, %s, %s)
                ON CONFLICT (fact_key) DO UPDATE SET fact_value = EXCLUDED.fact_value, last_verified_at = CURRENT_TIMESTAMP;
            """, (file, text_content, category))
            sync_count += 1
            
    conn.commit()
    cur.close()
    conn.close()
    print(f"✨ Permanent AI Memory Ledger fully updated. Synchronized {sync_count} source records.")

if __name__ == "__main__":
    operationalize_memory()
