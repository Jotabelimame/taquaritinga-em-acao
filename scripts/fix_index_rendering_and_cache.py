import os
import json
import re
import time

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
DADOS_DIR = os.path.join(SITE_DIR, "dados")
JSON_PATH = os.path.join(DADOS_DIR, "locais.json")
HTML_PATH = os.path.join(SITE_DIR, "index.html")

# 1. Garantir que locais.json tem linkFotos, fotos e status = "concluido" para Caetano Decaro e todos com fotos
with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

locais = data.get("locais", [])

concluidos = 0
for loc in locais:
    link = loc.get("linkFotos") or loc.get("fotos") or ""
    if link.strip() != "":
        loc["linkFotos"] = link.strip()
        loc["fotos"] = link.strip()
        loc["status"] = "concluido"
        concluidos += 1
    else:
        if loc.get("status") != "concluido":
            loc["status"] = "pendente"

data["total_concluidos"] = concluidos
data["total_pendentes"] = len(locais) - concluidos
data["ultima_atualizacao"] = f"27/07/2026 {time.strftime('%H:%M:%S')}"

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 2. Atualizar index.html
with open(HTML_PATH, "r", encoding="utf-8") as f:
    html_text = f.read()

json_full_str = json.dumps(data, ensure_ascii=False, indent=2)

# Atualizar initialData
new_html = re.sub(
    r"const initialData = \{.*?\};\n    let rawLocaisData =",
    f"const initialData = {json_full_str};\n    let rawLocaisData =",
    html_text,
    flags=re.DOTALL
)

# Garantir que hasFotos e isConcluido no JS do index.html olhem TANTO linkFotos QUANTO fotos
render_fix_old = r"const hasFotos = item\.linkFotos && item\.linkFotos\.trim\(\) !== '';"
render_fix_new = r"const hasFotos = (item.linkFotos && item.linkFotos.trim() !== '') || (item.fotos && item.fotos.trim() !== '');\n        const isConcluido = item.status === 'concluido' || hasFotos;"

new_html = re.sub(render_fix_old, render_fix_new, new_html)

# Adicionar cache buster no fetch('dados/locais.json')
fetch_old = r"fetch\('dados/locais\.json'\)"
fetch_new = f"fetch('dados/locais.json?v={int(time.time())}')"
new_html = re.sub(fetch_old, fetch_new, new_html)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(new_html)

print("\n=== INDEX.HTML E LOCAIS.JSON CORRIGIDOS COM CACHE-BUSTER ===")
print(f"Total de locais: {len(locais)}")
print(f"Total de concluídos com botão VERDE de fotos: {concluidos}")
print("Nenhum local com fotos ficará mais como 'Pendente' ou 'Sem Fotos'!")
