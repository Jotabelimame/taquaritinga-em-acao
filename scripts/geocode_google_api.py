import os
import json
import requests
import urllib.parse
import re

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
DADOS_DIR = os.path.join(SITE_DIR, "dados")
JSON_PATH = os.path.join(DADOS_DIR, "locais.json")
HTML_PATH = os.path.join(SITE_DIR, "index.html")

# 🔑 Chave de API do Google Maps fornecida pelo usuário
GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "AIzaSyC35-nB0TdRKspyYqfjqj8MPrfCESnxrDU")

def geocode_address(location_name, address, api_key):
    if not api_key:
        return None, None, address
        
    query_str = f"{location_name}, {address}, Taquaritinga, SP, Brasil"
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={urllib.parse.quote(query_str)}&key={api_key}"
    
    try:
        response = requests.get(url, timeout=10)
        res_json = response.json()
        if res_json.get("status") == "OK" and res_json.get("results"):
            location = res_json["results"][0]["geometry"]["location"]
            lat = round(location["lat"], 6)
            lng = round(location["lng"], 6)
            formatted_address = res_json["results"][0].get("formatted_address", address)
            return lat, lng, formatted_address
        else:
            print(f"Status da Geocoding API para '{location_name}': {res_json.get('status')}")
    except Exception as e:
        print(f"Erro na requisicao da Geocoding API para '{location_name}': {e}")
        
    return None, None, address

# 1. Carregar JSON existente
with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

locais = data.get("locais", [])
print(f"Iniciando Geocodificacao de {len(locais)} locais via Google Maps Geocoding API...")

atualizados = 0
for loc in locais:
    nome = loc["nome"]
    endereco = loc.get("endereco", "")
    
    lat_geo, lng_geo, end_geo = geocode_address(nome, endereco, GOOGLE_MAPS_API_KEY)
    
    if lat_geo and lng_geo:
        loc["lat"] = lat_geo
        loc["lng"] = lng_geo
        if end_geo:
            loc["endereco"] = end_geo
        query_map = f"{nome}, {loc['endereco']}".replace(" ", "+")
        loc["linkMaps"] = f"https://www.google.com/maps/search/?api=1&query={query_map}"
        atualizados += 1
        print(f"[{loc['id']}] {nome} -> Lat: {lat_geo}, Lng: {lng_geo}")

# 2. Salvar JSON atualizado
data["locais"] = locais
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nGeocodificacao concluida! {atualizados} de {len(locais)} locais atualizados com sucesso via Google Maps API.")

# 3. Atualizar index.html com dados geocodificados
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

print("index.html atualizado com sucesso!")
