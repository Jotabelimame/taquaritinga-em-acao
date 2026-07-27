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

# Atualizar Local #1 (Anunciata Colombo) com o link de fotos e status CONCLUÍDO
for loc in locais:
    if loc["id"] == 1 or "anunciata" in loc["nome"].lower():
        loc["nome"] = "EMEB / Berçário Anunciata Colombo"
        loc["endereco"] = "Rua Salvador Arnoni, 159 - Jardim São Sebastião, Taquaritinga - SP, 15903-112"
        loc["bairro"] = "Jardim São Sebastião"
        loc["lat"] = -21.384556
        loc["lng"] = -48.495396
        loc["linkFotos"] = "https://maps.app.goo.gl/bL7oJCt5oQ9SS4Fi7"
        loc["fotos"] = "https://maps.app.goo.gl/bL7oJCt5oQ9SS4Fi7"
        loc["status"] = "concluido"
        loc["linkMaps"] = "https://www.google.com/maps/search/?api=1&query=Rua+Salvador+Arnoni+159+Taquaritinga+SP"
        print(f"Atualizado Local #{loc['id']}: Status = CONCLUIDO, LinkFotos = {loc['linkFotos']}")

# Recalcular contadores totais
concluidos = sum(1 for l in locais if l["status"] == "concluido" or (l.get("linkFotos") or l.get("fotos")))
pendentes = len(locais) - concluidos

data["total_concluidos"] = concluidos
data["total_pendentes"] = pendentes
data["locais"] = locais

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Atualizar index.html com dados sincronizados
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

print("index.html e locais.json salvos com sucesso com o status CONCLUIDO!")
