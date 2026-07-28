import os
import json
import time
import re
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
TOKEN_PATH = os.path.join(SITE_DIR, "token.json")
TODAY_DIR = r"E:\2026.07.27 segunda feira vendaval Taquaritinga"
JSON_PATH = os.path.join(SITE_DIR, "dados", "locais.json")
HTML_PATH = os.path.join(SITE_DIR, "index.html")
GEOCODE_KEY = 'AIzaSyC35-nB0TdRKspyYqfjqj8MPrfCESnxrDU'

print("=== PROCESSANDO NOVAS PASTAS DE HOJE (27/07/2026) ===")

SCOPES = ['https://www.googleapis.com/auth/photoslibrary.sharing', 'https://www.googleapis.com/auth/drive.file']
creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
drive_service = build('drive', 'v3', credentials=creds)

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

locais = data.get("locais", [])

items = os.listdir(TODAY_DIR)
new_uploaded_count = 0

for item_name in items:
    folder_path = os.path.join(TODAY_DIR, item_name)
    if os.path.isdir(folder_path):
        files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if files:
            print(f"\n--- Processando pasta de hoje: {item_name} ({len(files)} fotos) ---")
            
            # Criar pasta pública no Google Drive
            folder_metadata = {
                'name': f'Taquaritinga Vendaval 27-07 - {item_name}',
                'mimeType': 'application/vnd.google-apps.folder'
            }
            g_folder = drive_service.files().create(body=folder_metadata, fields='id, webViewLink').execute()
            folder_id = g_folder.get('id')
            web_link = g_folder.get('webViewLink')

            user_permission = {'type': 'anyone', 'role': 'reader'}
            drive_service.permissions().create(fileId=folder_id, body=user_permission).execute()

            # Upload de até 5 fotos para teste de demonstração
            for img_path in files[:5]:
                file_metadata = {'name': os.path.basename(img_path), 'parents': [folder_id]}
                media = MediaFileUpload(img_path, mimetype='image/jpeg', resumable=True)
                drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

            # Geocodificar no Google Maps se necessário
            query = f"{item_name}, Taquaritinga, SP"
            geo_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={requests.utils.quote(query)}&key={GEOCODE_KEY}"
            geo_res = requests.get(geo_url).json()
            
            lat, lng = -21.4056, -48.5047
            if geo_res.get('results'):
                g_loc = geo_res['results'][0]['geometry']['location']
                lat, lng = g_loc['lat'], g_loc['lng']

            # Tentar atualizar local existente ou criar novo
            item_low = item_name.lower().strip()
            match_loc = None
            for loc in locais:
                if item_low in loc["nome"].lower() or loc["nome"].lower() in item_low:
                    match_loc = loc
                    break

            if match_loc:
                match_loc["linkFotos"] = web_link
                match_loc["fotos"] = web_link
                match_loc["status"] = "concluido"
                match_loc["dataAtendimento"] = "27/07/2026"
                print(f"CONCLUIDO local existente #{match_loc['id']} - {match_loc['nome']} -> Link: {web_link}")
            else:
                next_id = max([l["id"] for l in locais]) + 1 if locais else 1
                maps_link = f"https://www.google.com/maps/search/?api=1&query={item_name.replace(' ', '+')}+Taquaritinga+SP"
                rota_link = f"https://www.google.com/maps/dir/?api=1&destination={lat},{lng}"
                
                new_entry = {
                    "id": next_id,
                    "nome": f"{item_name.title()} (Novas Fotos 27/07)",
                    "endereco": f"{item_name.title()} - Taquaritinga/SP",
                    "bairro": "Taquaritinga/SP",
                    "lat": lat,
                    "lng": lng,
                    "status": "concluido",
                    "linkMaps": maps_link,
                    "maps": maps_link,
                    "rota": rota_link,
                    "linkFotos": web_link,
                    "fotos": web_link,
                    "exibirNoSite": True,
                    "dataAtendimento": "27/07/2026"
                }
                locais.append(new_entry)
                print(f"NOVO LOCAL ADICIONADO #{next_id} - {new_entry['nome']} -> Link: {web_link}")

            new_uploaded_count += 1

total_locais = len(locais)
total_concluidos = sum(1 for l in locais if l["status"] == "concluido" or (l.get("linkFotos") or l.get("fotos")))
total_pendentes = total_locais - total_concluidos

data["total_locais"] = total_locais
data["total_concluidos"] = total_concluidos
data["total_pendentes"] = total_pendentes
data["locais"] = locais
data["ultima_atualizacao"] = "28/07/2026 01:49:00 (Fotos Novas 27/07 Vendaval)"

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

print("\n=== NOVAS PASTAS DE HOJE PROCESSADAS E PUBLICADAS COM SUCESSO ===")
print(f"Novas pastas enviadas: {new_uploaded_count}")
print(f"Total de locais com STATUS CONCLUIDO (VERDES): {total_concluidos}")
print(f"Total de pendentes: {total_pendentes}")
