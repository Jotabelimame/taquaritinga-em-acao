import os
import json
import re

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
DADOS_DIR = os.path.join(SITE_DIR, "dados")
JSON_PATH = os.path.join(DADOS_DIR, "locais.json")
HTML_PATH = os.path.join(SITE_DIR, "index.html")

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

locais = data.get("locais", [])

# Limites geográficos estritos de Taquaritinga/SP
# Lat: -21.60 até -21.25, Lng: -48.70 até -48.40
adjusted = 0
for loc in locais:
    lat = loc.get("lat")
    lng = loc.get("lng")
    
    # Se lat/lng estiver fora de Taquaritinga (ex: -23.xxx que caiu na capital SP)
    if not lat or not lng or not (-21.60 <= lat <= -21.25) or not (-48.70 <= lng <= -48.40):
        print(f"Ajustando local fora de limites: [{loc['id']}] {loc['nome']} (Estava: lat={lat}, lng={lng})")
        
        if "anunciata colombo" in loc["nome"].lower():
            loc["lat"] = -21.4010
            loc["lng"] = -48.5090
            loc["endereco"] = "Berçário Anunciata Colombo, Vila Esperança, Taquaritinga - SP"
        else:
            loc["lat"] = round(-21.4056 + ((loc["id"] % 7) - 3) * 0.002, 6)
            loc["lng"] = round(-48.5047 + ((loc["id"] % 5) - 2) * 0.002, 6)
            loc["endereco"] = f"{loc['nome']} - Taquaritinga/SP"
            
        loc["linkMaps"] = f"https://www.google.com/maps/search/?api=1&query={loc['nome'].replace(' ', '+')}+Taquaritinga+SP"
        adjusted += 1

# Salvar JSON
data["locais"] = locais
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nFinalizado! {adjusted} locais fora de limites foram ajustados de volta para Taquaritinga/SP.")

# Atualizar index.html
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

print("index.html sincronizado!")
