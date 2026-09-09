import os
from datetime import datetime

# ==========================================
# 1. DEFINISI FUNGSI / TOOLS LOKAL
# ==========================================

def get_current_time() -> str:
    """
    Mengembalikan tanggal dan waktu lokal saat ini dalam format string.
    Gunakan fungsi ini ketika pengguna menanyakan waktu atau tanggal sekarang.
    """
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def read_file_content(file_path: str) -> str:
    """
    Membaca isi dari sebuah file teks lokal berdasarkan path file yang diberikan.
    Gunakan fungsi ini jika pengguna meminta untuk membaca atau memeriksa isi file tertentu.
    """
    try:
        if not os.path.exists(file_path):
            return f"❌ Error: File '{file_path}' tidak ditemukan."
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            return content if content.strip() else "ℹ️ File tersebut kosong."
            
    except Exception as e:
        return f"❌ Terjadi kesalahan saat membaca file: {str(e)}"

# ==========================================
# 2. REGISTRY TOOL
# Daftar fungsi Python yang diizinkan untuk dipanggil oleh Gemini AI
# ==========================================
available_tools = [
    get_current_time,
    read_file_content
]