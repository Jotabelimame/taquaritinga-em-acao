import os
import json

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
CREDENTIALS_PATH = os.path.join(SITE_DIR, "credentials.json")
TOKEN_PATH = os.path.join(SITE_DIR, "token.json")

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/photoslibrary.sharing', 'https://www.googleapis.com/auth/drive.file']

flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
# Usar a URI padrão de aplicativos desktop
flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'

auth_url, _ = flow.authorization_url(prompt='consent')

print("=== AUTENTICAÇÃO DIRETA DO GOOGLE (SEM LOCALHOST) ===")
print("\n1. Abra este link no seu navegador:")
print(auth_url)
print("\n2. Faça login, clique em Permitir e COPIE o código que aparecerá na tela do Google.")
