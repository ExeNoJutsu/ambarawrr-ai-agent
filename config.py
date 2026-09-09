import os
from dotenv import load_dotenv
import google.generativeai as genai

def init_gemini():
    """
    Menginisialisasi konfigurasi Gemini SDK dan mengunci ke gemini-3.6-flash.
    """
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("❌ Error: API Key tidak ditemukan di file .env!")
        exit()

    genai.configure(api_key=api_key)

    # Kunci langsung ke gemini-3.6-flash (tanpa nyari-nyari versi tua lagi)
    target_model = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
    return target_model