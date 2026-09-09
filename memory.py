import json
import os

HISTORY_FILE = "history.json"
MAX_HISTORY = 10

def load_raw_history():
    """Membaca riwayat mentah dari berkas history.json."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_raw_history(history_data):
    """Menyimpan riwayat percakapan ke berkas history.json."""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"⚠️ Gagal menyimpan memori: {e}")

def get_gemini_history(history_data):
    """Mengambil N pesan terakhir (Sliding Window) dan mengubahnya ke format SDK Gemini."""
    recent_history = history_data[-MAX_HISTORY:]
    return [
        {"role": item["role"], "parts": [item["content"]]} 
        for item in recent_history
    ]