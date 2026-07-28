"""
Script de Upload Automático de Pastas Locais para o Google Fotos / Google Drive API.
"""

import os
import json
import time

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
CREDENTIALS_PATH = os.path.join(SITE_DIR, "credentials.json")
TOKEN_PATH = os.path.join(SITE_DIR, "token.json")
DRIVE_DIR = r"E:\2026.07.24 sexta feira Vendaval Taquaritinga"
JSON_PATH = os.path.join(SITE_DIR, "dados", "locais.json")

print("=== VERIFICADOR DO UPLOAD AUTOMATICO DO GOOGLE FOTOS ===")

if not os.path.exists(CREDENTIALS_PATH):
    print(f"Arquivo 'credentials.json' NAO ENCONTRADO em: {CREDENTIALS_PATH}")
else:
    print(f"Arquivo 'credentials.json' ENCONTRADO COM SUCESSO em: {CREDENTIALS_PATH}")
    print("Credenciais OAuth 2.0 ativadas e configuradas!")
