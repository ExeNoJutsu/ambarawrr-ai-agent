import json
import os
from dotenv import load_dotenv
import google.generativeai as genai

# 1. Load API Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: API Key tidak ditemukan di file .env!")
    exit()

genai.configure(api_key=api_key)

# 2. Hardcode Model Tercepat (Ganti string ini sesuai nama model yang sukses di terminal lu)
MODEL_NAME = 'gemini-3.6-flash'

# 3. Setup Memori Ringan
HISTORY_FILE = "history.json"
history_data = []

if os.path.exists(HISTORY_FILE):
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history_data = json.load(f)
    except Exception:
        history_data = []

# BATASI MEMORI: Cuma kirim 10 percakapan terakhir biar payload API tetep kencang
MAX_HISTORY = 10
recent_history = history_data[-MAX_HISTORY:]

gemini_history = [
    {"role": item["role"], "parts": [item["content"]]} 
    for item in recent_history
]

# 4. Inisialisasi Chat
model = genai.GenerativeModel(MODEL_NAME)
chat = model.start_chat(history=gemini_history)

print(f"=== AMBARAWRR AI AGENT V1 ONLINE ({MODEL_NAME}) ===")

# 5. Loop Percakapan Utama
while True:
    pesan_user = input("\nLu: ")
    
    if pesan_user.lower() in ['exit', 'keluar']:
        print("Agent offline. Sampai jumpa!")
        break
        
    if not pesan_user.strip():
        continue

    print("Ambarawrr Agent: ", end="", flush=True)

    try:
        # Stream response langsung tanpa tunda
        response = chat.send_message(pesan_user, stream=True)
        full_response = ""
        
        for chunk in response:
            print(chunk.text, end="", flush=True)
            full_response += chunk.text
        print()

        # Update file history.json di latar belakang
        history_data.append({"role": "user", "content": pesan_user})
        history_data.append({"role": "model", "content": full_response})

        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)

    except Exception as e:
        print(f"\n❌ Terjadi kesalahan: {e}")