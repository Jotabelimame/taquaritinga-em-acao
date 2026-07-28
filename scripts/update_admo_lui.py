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

ADMO_FOTOS = "https://photos.app.goo.gl/2UDfbHg7URsesdEu9"
ADMO_MAPS = "https://maps.app.goo.gl/pRzNfKbXQzqYbAe7"
ADMO_ROTA = "https://www.google.com/maps/dir/?api=1&destination=-21.408549,-48.513281"

found = False
for loc in locais:
    nome_low = loc["nome"].lower()
    if "admo lui" in nome_low or loc["id"] == 35:
        loc["nome"] = "Avenida Admo Lui"
        loc["endereco"] = "Avenida Admo Lui • Jardim São Carlos • CEP 15906-740"
        loc["bairro"] = "Jardim São Carlos"
        loc["lat"] = -21.408549
        loc["lng"] = -48.513281
        loc["maps"] = ADMO_MAPS
        loc["linkMaps"] = ADMO_MAPS
        loc["rota"] = ADMO_ROTA
        loc["fotos"] = ADMO_FOTOS
        loc["linkFotos"] = ADMO_FOTOS
        loc["status"] = "concluido"
        found = True
        print(f"Atualizado Local #{loc['id']}: {loc['nome']} -> Status: CONCLUIDO | Fotos: {loc['linkFotos']}")

if not found:
    next_id = max([l["id"] for l in locais]) + 1 if locais else 35
    locais.append({
        "id": next_id,
        "nome": "Avenida Admo Lui",
        "endereco": "Avenida Admo Lui • Jardim São Carlos • CEP 15906-740",
        "bairro": "Jardim São Carlos",
        "lat": -21.408549,
        "lng": -48.513281,
        "status": "concluido",
        "maps": ADMO_MAPS,
        "linkMaps": ADMO_MAPS,
        "rota": ADMO_ROTA,
        "fotos": ADMO_FOTOS,
        "linkFotos": ADMO_FOTOS,
        "dataAtendimento": "27/07/2026"
    })
    print(f"Novo Local #{next_id} cadastrado: Avenida Admo Lui!")

total_locais = len(locais)
total_concluidos = sum(1 for l in locais if l["status"] == "concluido" or (l.get("linkFotos") or l.get("fotos")))
total_pendentes = total_locais - total_concluidos

data["total_locais"] = total_locais
data["total_concluidos"] = total_concluidos
data["total_pendentes"] = total_pendentes
data["locais"] = locais

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

print("\n=== ATUALIZACAO DA AVENIDA ADMO LUI CONCLUIDA ===")
print(f"Total locais: {total_locais} | Concluidos: {total_concluidos} | Pendentes: {total_pendentes}")
