import os
import sys
import json

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
CREDENTIALS_PATH = os.path.join(SITE_DIR, "credentials.json")
TOKEN_PATH = os.path.join(SITE_DIR, "token.json")

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/photoslibrary.sharing', 'https://www.googleapis.com/auth/drive.file']

def authenticate_with_code(code_str):
    code_str = code_str.strip()
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
    flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
    flow.fetch_token(code=code_str)
    creds = flow.credentials
    with open(TOKEN_PATH, 'w') as token:
        token.write(creds.to_json())
    print(f"✅ TOKEN SALVO COM SUCESSO EM: {TOKEN_PATH}")
    return creds

if __name__ == "__main__":
    if len(sys.argv) > 1:
        code_input = sys.argv[1]
        authenticate_with_code(code_input)
    else:
        print("Uso: python exchange_code.py <codigo_copiado_do_google>")
