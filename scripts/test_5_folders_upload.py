import os
import json
import time

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
CREDENTIALS_PATH = os.path.join(SITE_DIR, "credentials.json")
TOKEN_PATH = os.path.join(SITE_DIR, "token.json")
DRIVE_DIR = r"E:\2026.07.24 sexta feira Vendaval Taquaritinga"
JSON_PATH = os.path.join(SITE_DIR, "dados", "locais.json")

test_folders = [
    {"id": 23, "nome": "Emilio Giroto"},
    {"id": 25, "nome": "escola Santa Cecilia ETAM"},
    {"id": 26, "nome": "francisco romano"},
    {"id": 27, "nome": "general Osorio igreja matriz"},
    {"id": 29, "nome": "Josephina mantese morcelli pinsetta"}
]

print("=== TESTE DE AUTENTICAÇÃO E UPLOAD DO BLOCO DE 5 PASTAS ===")
print("Verificando estrutura das 5 pastas de teste no drive E:\\...")

for item in test_folders:
    folder_path = os.path.join(DRIVE_DIR, item["nome"])
    exists = os.path.exists(folder_path)
    count = len(os.listdir(folder_path)) if exists else 0
    print(f"Pastas ID #{item['id']} ({item['nome']}): Existe={exists} | Arquivos={count}")

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials

    SCOPES = ['https://www.googleapis.com/auth/photoslibrary.sharing', 'https://www.googleapis.com/auth/drive.file']

    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("\nOpening browser window for one-time Google OAuth authorization...")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
    print("\n✅ GOOGLE OAUTH AUTENTICADO COM SUCESSO!")
except Exception as e:
    print(f"\nAviso de Autenticação/Dependência: {e}")
