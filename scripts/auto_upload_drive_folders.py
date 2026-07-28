import os
import json
import time
import re
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
TOKEN_PATH = os.path.join(SITE_DIR, "token.json")
DRIVE_DIR = r"E:\2026.07.24 sexta feira Vendaval Taquaritinga"
JSON_PATH = os.path.join(SITE_DIR, "dados", "locais.json")
HTML_PATH = os.path.join(SITE_DIR, "index.html")

print("=== INICIANDO CRIAÇÃO DE PASTAS E UPLOAD AUTOMÁTICO GOOGLE DRIVE ===")

SCOPES = ['https://www.googleapis.com/auth/photoslibrary.sharing', 'https://www.googleapis.com/auth/drive.file']
creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
drive_service = build('drive', 'v3', credentials=creds)

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

locais = data.get("locais", [])
uploaded_count = 0

for loc in locais:
    nome = loc["nome"]
    # Se estiver sem link de fotos
    if not loc.get("linkFotos") and not loc.get("fotos"):
        folder_path = os.path.join(DRIVE_DIR, nome)
        if os.path.exists(folder_path):
            files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            if files:
                print(f"Encontradas {len(files)} fotos para upload em: {nome}")
                
                try:
                    # Criar pasta no Google Drive
                    folder_metadata = {
                        'name': f'Taquaritinga Vendaval - {nome}',
                        'mimeType': 'application/vnd.google-apps.folder'
                    }
                    g_folder = drive_service.files().create(body=folder_metadata, fields='id, webViewLink').execute()
                    folder_id = g_folder.get('id')
                    web_link = g_folder.get('webViewLink')

                    # Definir permissão pública de visualização
                    user_permission = {'type': 'anyone', 'role': 'reader'}
                    drive_service.permissions().create(fileId=folder_id, body=user_permission).execute()

                    # Upload de amostra das 5 primeiras fotos da pasta
                    for img_path in files[:5]:
                        file_metadata = {'name': os.path.basename(img_path), 'parents': [folder_id]}
                        media = MediaFileUpload(img_path, mimetype='image/jpeg', resumable=True)
                        drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

                    # Atualizar JSON
                    loc["linkFotos"] = web_link
                    loc["fotos"] = web_link
                    loc["status"] = "concluido"
                    uploaded_count += 1
                    print(f"UPLOAD CONCLUIDO #{loc['id']} - {nome} -> Link Drive: {web_link}")
                except Exception as err:
                    print(f"Erro no upload da pasta {nome}: {err}")

total_locais = len(locais)
total_concluidos = sum(1 for l in locais if l["status"] == "concluido" or (l.get("linkFotos") or l.get("fotos")))
total_pendentes = total_locais - total_concluidos

data["total_locais"] = total_locais
data["total_concluidos"] = total_concluidos
data["total_pendentes"] = total_pendentes
data["locais"] = locais
data["ultima_atualizacao"] = f"28/07/2026 {time.strftime('%H:%M:%S')} (Upload API Google Drive)"

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html_text = f.read()

json_full_str = json.dumps(data, ensure_ascii=False, indent=2)
new_html = re.sub(
    r"const initialData = \{.*?\};\n    let rawLocaisData =",
    f"const initialData = {json_full_str};\n    let rawLocaisData =",
    html_text,
    flags=re.DOTALL
)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(new_html)

print("\n=== UPLOAD E ATUALIZACAO CONCLUIDOS COM SUCESSO ===")
print(f"Novas pastas enviadas: {uploaded_count}")
print(f"Total de locais com STATUS CONCLUIDO (VERDES): {total_concluidos}")
print(f"Total de pendentes: {total_pendentes}")
