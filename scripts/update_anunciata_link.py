import os
import json
import re

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
DADOS_DIR = os.path.join(SITE_DIR, "dados")
JSON_PATH = os.path.join(DADOS_DIR, "locais.json")
HTML_PATH = os.path.join(SITE_DIR, "index.html")
PROCESS_SCRIPT_PATH = os.path.join(SITE_DIR, "scripts", "process_excel.py")

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

locais = data.get("locais", [])

# Atualizar Local #1 (Anunciata Colombo) com o link exato do álbum do Google Fotos
NEW_ALBUM_LINK = "https://photos.app.goo.gl/JMSJy1nzX9ajbdpp8"

for loc in locais:
    if loc["id"] == 1 or "anunciata" in loc["nome"].lower():
        loc["nome"] = "EMEB / Berçário Anunciata Colombo"
        loc["endereco"] = "Rua Salvador Arnoni, 159 - Jardim São Sebastião, Taquaritinga - SP, 15903-112"
        loc["bairro"] = "Jardim São Sebastião"
        loc["lat"] = -21.384556
        loc["lng"] = -48.495396
        loc["linkFotos"] = NEW_ALBUM_LINK
        loc["fotos"] = NEW_ALBUM_LINK
        loc["status"] = "concluido"
        loc["linkMaps"] = "https://www.google.com/maps/search/?api=1&query=Rua+Salvador+Arnoni+159+Taquaritinga+SP"
        print(f"Atualizado Local #{loc['id']}: Status = CONCLUIDO, Link = {NEW_ALBUM_LINK}")

# Recalcular estatísticas
concluidos = sum(1 for l in locais if l["status"] == "concluido" or (l.get("linkFotos") or l.get("fotos")))
pendentes = len(locais) - concluidos

data["total_concluidos"] = concluidos
data["total_pendentes"] = pendentes
data["locais"] = locais

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Sincronizar index.html
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

# Atualizar o link no process_excel.py também para garantir consistência
with open(PROCESS_SCRIPT_PATH, "r", encoding="utf-8") as f:
    process_code = f.read()

process_code = process_code.replace("https://maps.app.goo.gl/bL7oJCt5oQ9SS4Fi7", NEW_ALBUM_LINK)

with open(PROCESS_SCRIPT_PATH, "w", encoding="utf-8") as f:
    f.write(process_code)

print("index.html, locais.json e process_excel.py atualizados com sucesso com o álbum correto do Google Fotos!")
