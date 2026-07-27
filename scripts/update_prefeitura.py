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

PREFEITURA_FOTOS = "https://photos.app.goo.gl/nx1uPz13BJmPBHEi6"
PREFEITURA_MAPS = "https://maps.app.goo.gl/z2FN85uoQDLSHSmW8"

found = False
for loc in locais:
    nome_lower = loc["nome"].lower()
    if "predio da prefeitura" in nome_lower or "prédio da prefeitura" in nome_lower or "prefeitura" in nome_lower:
        loc["nome"] = "Prédio da Prefeitura Municipal"
        loc["endereco"] = "R. Romeu Mársico, 200 - Taquaritinga, SP, 15900-000"
        loc["bairro"] = "Centro"
        loc["lat"] = -21.411747
        loc["lng"] = -48.498400
        loc["linkMaps"] = PREFEITURA_MAPS
        loc["linkFotos"] = PREFEITURA_FOTOS
        loc["fotos"] = PREFEITURA_FOTOS
        loc["status"] = "concluido"
        found = True
        print(f"Atualizado Local #{loc['id']}: {loc['nome']} -> {loc['endereco']} ({loc['lat']}, {loc['lng']}) - Status: CONCLUIDO")

if not found:
    next_id = max([l["id"] for l in locais]) + 1 if locais else 1
    locais.append({
        "id": next_id,
        "nome": "Prédio da Prefeitura Municipal",
        "endereco": "R. Romeu Mársico, 200 - Taquaritinga, SP, 15900-000",
        "bairro": "Centro",
        "lat": -21.411747,
        "lng": -48.498400,
        "status": "concluido",
        "linkMaps": PREFEITURA_MAPS,
        "linkFotos": PREFEITURA_FOTOS,
        "fotos": PREFEITURA_FOTOS,
        "dataAtendimento": "27/07/2026"
    })
    print(f"Novo Local #{next_id} cadastrado para Prefeitura Municipal!")

# Recalcular contadores
concluidos = sum(1 for l in locais if l["status"] == "concluido" or (l.get("linkFotos") or l.get("fotos")))
pendentes = len(locais) - concluidos

data["total_concluidos"] = concluidos
data["total_pendentes"] = pendentes
data["locais"] = locais

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

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

print("Prefeitura Municipal atualizada com sucesso no locais.json e index.html!")
