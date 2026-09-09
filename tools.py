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
# 2. TOOLS CLICKUP API (V3 ADVANCED)
# ==========================================

def get_clickup_workspace_structure() -> str:
    """
    Membaca seluruh peta/struktur Workspace ClickUp pengguna (Semua Space, Folder, dan List beserta ID-nya).
    Gunakan fungsi ini jika pengguna menanyakan ada folder/space apa saja di ClickUp (misal: AKADEMIK, SIDE HUSTLE, dll)
    atau saat perlu mencari ID dari List tertentu di luar List default.
    """
    api_key = os.getenv("CLICKUP_API_KEY")
    if not api_key:
        return "❌ Error: CLICKUP_API_KEY belum diatur di file .env!"

    headers = {"Authorization": api_key}
    
    try:
        teams_res = requests.get("https://api.clickup.com/api/v2/team", headers=headers)
        if teams_res.status_code != 200:
            return f"❌ Gagal mengambil data Workspace: HTTP {teams_res.status_code}"
        
        teams = teams_res.json().get("teams", [])
        if not teams:
            return "ℹ️ Tidak ditemukan Workspace pada akun ClickUp ini."
        
        output = []
        for team in teams:
            team_id = team["id"]
            output.append(f"🏢 **Workspace: {team['name']}**")
            
            spaces_res = requests.get(f"https://api.clickup.com/api/v2/team/{team_id}/space", headers=headers)
            if spaces_res.status_code == 200:
                spaces = spaces_res.json().get("spaces", [])
                for space in spaces:
                    space_id = space["id"]
                    output.append(f"  🚀 Space: {space['name']}")
                    
                    lists_res = requests.get(f"https://api.clickup.com/api/v2/space/{space_id}/list", headers=headers)
                    if lists_res.status_code == 200:
                        for l in lists_res.json().get("lists", []):
                            output.append(f"    📋 List: {l['name']} (ID: {l['id']})")
                    
                    folders_res = requests.get(f"https://api.clickup.com/api/v2/space/{space_id}/folder", headers=headers)
                    if folders_res.status_code == 200:
                        for folder in folders_res.json().get("folders", []):
                            output.append(f"    📁 Folder: {folder['name']}")
                            for fl in folder.get("lists", []):
                                output.append(f"      📋 List: {fl['name']} (ID: {fl['id']})")
        
        return "\n".join(output) if output else "ℹ️ Struktur Workspace kosong."
    except Exception as e:
        return f"❌ Terjadi kesalahan saat membaca struktur ClickUp: {str(e)}"

def get_clickup_tasks(target_list_id: str = "") -> str:
    """
    Membaca daftar task dari ClickUp List.
    Jika target_list_id diisi, akan membaca List tersebut. Jika dikosongkan, akan memakai List default dari .env.
    """
    api_key = os.getenv("CLICKUP_API_KEY")
    list_id = target_list_id if target_list_id else os.getenv("CLICKUP_LIST_ID")

    if not api_key or not list_id:
        return "❌ Error: API Key atau List ID tidak ditemukan!"

    url = f"https://api.clickup.com/api/v2/list/{list_id}/task"
    headers = {"Authorization": api_key}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            tasks = response.json().get("tasks", [])
            if not tasks:
                return f"ℹ️ Tidak ada task di List ID ({list_id})."

            hasil = []
            for t in tasks:
                status = t.get("status", {}).get("status", "unknown").upper()
                nama = t.get("name", "Tanpa Nama")
                hasil.append(f"• [{status}] {nama}")
            
            return f"📋 Daftar Task ClickUp (List ID: {list_id}):\n" + "\n".join(hasil)
        else:
            return f"❌ Gagal mengambil task: HTTP {response.status_code} - {response.text}"
    except Exception as e:
        return f"❌ Terjadi kesalahan koneksi ClickUp API: {str(e)}"

def create_clickup_task(task_name: str, description: str = "", target_list_id: str = "") -> str:
    """
    Membuat task baru di ClickUp List.
    Jika target_list_id diisi, task dibuat di List tersebut. Jika kosong, dibuat di List default .env.
    """
    api_key = os.getenv("CLICKUP_API_KEY")
    list_id = target_list_id if target_list_id else os.getenv("CLICKUP_LIST_ID")

    if not api_key or not list_id:
        return "❌ Error: API Key atau List ID tidak ditemukan!"

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
            return f"✅ Berhasil membuat task '{data.get('name')}' di List ID {list_id} (Task ID: {data.get('id')})"
        else:
            return f"❌ Gagal membuat task: HTTP {response.status_code} - {response.text}"
    except Exception as e:
        return f"❌ Terjadi kesalahan koneksi ClickUp API: {str(e)}"

# ==========================================
# 3. REGISTRY TOOL V3
# ==========================================
available_tools = [
    get_current_time,
    read_file_content,
    get_clickup_workspace_structure,
    get_clickup_tasks,
    create_clickup_task
]