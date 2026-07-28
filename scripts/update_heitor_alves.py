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

FOTOS_HEITOR = "https://photos.app.goo.gl/w3Kns8cGNRCysGgMA"

for loc in locais:
    if loc["id"] == 12 or "heitor alves" in loc["nome"].lower():
        loc["nome"] = "Avenida Heitor Alves Gomes"
        loc["linkFotos"] = FOTOS_HEITOR
        loc["fotos"] = FOTOS_HEITOR
        loc["status"] = "concluido"
        print(f"Atualizado Local #{loc['id']}: {loc['nome']} -> Status: CONCLUIDO | Fotos: {FOTOS_HEITOR}")

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

print("\n=== AV. HEITOR ALVES GOMES ATUALIZADA ===")
print(f"Total locais: {total_locais} | Concluidos: {total_concluidos} | Pendentes: {total_pendentes}")
