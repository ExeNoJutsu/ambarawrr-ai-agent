import os
import requests
from datetime import datetime

# ==========================================
# 1. TOOLS LOKAL DASAR
# ==========================================

def get_current_time() -> str:
    """
    Mengembalikan tanggal dan waktu lokal saat ini dalam format string (YYYY-MM-DD HH:MM:SS).
    Gunakan fungsi ini ketika pengguna menanyakan waktu, jam, atau tanggal sekarang.
    """
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def read_file_content(file_path: str) -> str:
    """
    Membaca isi dari sebuah file teks lokal berdasarkan path file yang diberikan.
    Gunakan fungsi ini jika pengguna meminta untuk membaca atau memeriksa file.
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
# 2. TOOLS CLICKUP API (V3)
# ==========================================

def get_clickup_tasks() -> str:
    """
    Membaca dan mengambil daftar task/tugas dari ClickUp List pengguna.
    Gunakan fungsi ini saat pengguna meminta untuk membaca task, melihat ringkasan harian,
    atau mengecek agenda kerjaan di ClickUp.
    """
    api_key = os.getenv("CLICKUP_API_KEY")
    list_id = os.getenv("CLICKUP_LIST_ID")

    if not api_key or not list_id:
        return "❌ Error: CLICKUP_API_KEY atau CLICKUP_LIST_ID belum diatur di file .env!"

    url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
    headers = {"Authorization": api_key}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            tasks = response.json().get("tasks", [])
            if not tasks:
                return "ℹ️ Tidak ada task di ClickUp List ini."

            hasil = []
            for t in tasks:
                status = t.get("status", {}).get("status", "unknown").upper()
                nama = t.get("name", "Tanpa Nama")
                hasil.append(f"• [{status}] {nama}")
            
            return "📋 Daftar Task ClickUp Saat Ini:\n" + "\n".join(hasil)
        else:
            return f"❌ Gagal mengambil task ClickUp: HTTP {response.status_code} - {response.text}"
    except Exception as e:
        return f"❌ Terjadi kesalahan koneksi ClickUp API: {str(e)}"

def create_clickup_task(task_name: str, description: str = "") -> str:
    """
    Membuat task/tugas baru di ClickUp List pengguna.
    Gunakan fungsi ini ketika pengguna meminta untuk menambahkan, membuat, atau mencatat task baru ke ClickUp.
    """
    api_key = os.getenv("CLICKUP_API_KEY")
    list_id = os.getenv("CLICKUP_LIST_ID")

    if not api_key or not list_id:
        return "❌ Error: CLICKUP_API_KEY atau CLICKUP_LIST_ID belum diatur di file .env!"

    url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "name": task_name,
        "description": description
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code in [200, 201]:
            data = response.json()
            return f"✅ Berhasil membuat task ClickUp: '{data.get('name')}' (ID: {data.get('id')})"
        else:
            return f"❌ Gagal membuat task ClickUp: HTTP {response.status_code} - {response.text}"
    except Exception as e:
        return f"❌ Terjadi kesalahan koneksi ClickUp API: {str(e)}"

# ==========================================
# 3. REGISTRY TOOL V3
# ==========================================
available_tools = [
    get_current_time,
    read_file_content,
    get_clickup_tasks,
    create_clickup_task
]