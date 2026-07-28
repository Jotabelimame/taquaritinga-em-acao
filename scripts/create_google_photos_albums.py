import os
import json
import time
import requests

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
TOKEN_PATH = os.path.join(SITE_DIR, "token.json")
TODAY_DIR = r"E:\2026.07.27 segunda feira vendaval Taquaritinga"
JSON_PATH = os.path.join(SITE_DIR, "dados", "locais.json")
HTML_PATH = os.path.join(SITE_DIR, "index.html")

print("=== CRIANDO ÁLBUNS NATIVOS NO GOOGLE FOTOS VIA API REST ===")

with open(TOKEN_PATH, "r", encoding="utf-8") as f:
    token_data = json.load(f)

access_token = token_data.get("token")
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# 1. Obter lista de pastas de hoje
folders = [f for f in os.listdir(TODAY_DIR) if os.path.isdir(os.path.join(TODAY_DIR, f))]
print(f"Pastas encontradas em {TODAY_DIR}: {folders}")

created_albums = {}

for f_name in folders:
    album_title = f"Vendaval Taquaritinga 27-07 - {f_name}"
    print(f"\nCriando álbum nativo no Google Fotos: '{album_title}'...")
    
    # Endpoint de criação de álbum do Google Fotos
    url_album = "https://photoslibrary.googleapis.com/v1/albums"
    body_album = {"album": {"title": album_title}}
    
    res = requests.post(url_album, headers=headers, json=body_album)
    if res.status_code == 200:
        album_info = res.json()
        album_id = album_info.get("id")
        product_url = album_info.get("productUrl")
        
        # Compartilhar álbum para obter o link público do Google Fotos
        url_share = f"https://photoslibrary.googleapis.com/v1/albums/{album_id}:share"
        body_share = {"sharedAlbumOptions": {"isCollaborative": "false", "isCommentable": "true"}}
        share_res = requests.post(url_share, headers=headers, json=body_share)
        
        share_url = product_url
        if share_res.status_code == 200:
            share_info = share_res.json()
            share_url = share_info.get("sharedAlbumOptions", {}).get("sharedToken", product_url)
            if share_info.get("shareableUrl"):
                share_url = share_info.get("shareableUrl")

        print(f"✅ ÁLBUM CRIADO COM SUCESSO! Link Google Fotos: {product_url}")
        created_albums[f_name] = product_url
    else:
        print(f"Status {res.status_code}: {res.text}")

print("\n=== RESUMO DOS ÁLBUNS DO GOOGLE FOTOS CRIADOS ===")
for k, v in created_albums.items():
    print(f"• {k} -> {v}")
