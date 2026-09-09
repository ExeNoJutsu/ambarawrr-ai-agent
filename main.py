import google.generativeai as genai
from config import init_gemini
from memory import load_raw_history, save_raw_history, get_gemini_history
from tools import available_tools

# 1. Inisialisasi Model Aktif (config.py)
active_model_name = init_gemini()

# 2. Load Memory Percakapan (memory.py)
history_data = load_raw_history()
gemini_history = get_gemini_history(history_data)

# 3. System Instruction & Pengaturan Model dengan Tools Registry
system_instruction = (
    "Lu adalah AMBARAWRR AI Agent V2, asisten cerdas, responsif, dan gaul. "
    "Gunakan bahasa yang santai tapi tetap jelas. "
    "Kamu memiliki akses ke tools eksekusi fungsi Python. "
    "Jika pengguna menanyakan waktu/tanggal, selalu gunakan fungsi get_current_time()!"
)

model = genai.GenerativeModel(
    model_name=active_model_name,
    system_instruction=system_instruction,
    tools=available_tools
)

# Enable Automatic Function Calling agar Gemini otomatis memanggil fungsi Python lokal
chat = model.start_chat(history=gemini_history, enable_automatic_function_calling=True)

print(f"=== AMBARAWRR AI AGENT V2 ONLINE ===")
print(f"🤖 Model Aktif : {active_model_name}")
print(f"🛠️  Tools Registry: {[t.__name__ for t in available_tools]}")

# 4. Loop Utama Percakapan
while True:
    pesan_user = input("\nLu: ")

    if pesan_user.lower() in ['exit', 'keluar']:
        print("Agent offline. Sampai jumpa!")
        break

    if not pesan_user.strip():
        continue

    # Indikator visual agar tidak berasa hang
    print("Ambarawrr Agent: ⏳ Sedang memproses...", end="\r", flush=True)

    try:
        # Kirim pesan tanpa stream=True (karena automatic function calling aktif)
        response = chat.send_message(pesan_user)
        
        # Bersihkan baris indikator lalu cetak jawaban akhir
        print(" " * 40, end="\r") 
        print(f"Ambarawrr Agent: {response.text}")

        # Simpan Percakapan ke history.json
        history_data.append({"role": "user", "content": pesan_user})
        history_data.append({"role": "model", "content": response.text})
        save_raw_history(history_data)

    except Exception as e:
        print(f"\n❌ Terjadi kesalahan: {e}")