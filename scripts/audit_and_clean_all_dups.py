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
print(f"Total de registros antes da auditoria: {len(locais)}")

seen_keys = set()
unique_locais = []
removed_count = 0

for loc in locais:
    nome = loc["nome"].strip()
    endereco = loc.get("endereco", "").strip()
    
    key = nome.lower().replace("prédio da prefeitura municipal", "prefeitura").replace("prefeitura municipal", "prefeitura").replace("comitê de crise da prefeitura", "prefeitura")
    key = re.sub(r"\s+", " ", key).strip()
    
    if key in seen_keys:
        print(f"Removendo duplicata encontrada: ID #{loc.get('id')} - {nome}")
        removed_count += 1
    else:
        seen_keys.add(key)
        unique_locais.append(loc)

for new_id, loc in enumerate(unique_locais, start=1):
    loc["id"] = new_id

total_locais = len(unique_locais)
total_concluidos = sum(1 for l in unique_locais if l["status"] == "concluido" or (l.get("linkFotos") or l.get("fotos")))
total_pendentes = total_locais - total_concluidos

data["total_locais"] = total_locais
data["total_concluidos"] = total_concluidos
data["total_pendentes"] = total_pendentes
data["locais"] = unique_locais
data["ultima_atualizacao"] = "27/07/2026 14:43:00 (Desduplicado)"

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

print("\n=== AUDITORIA E LIMPEZA CONCLUIDA ===")
print(f"Total de registros desduplicados mantidos: {total_locais}")
print(f"Total de concluidos (com fotos): {total_concluidos}")
print(f"Total de pendentes: {total_pendentes}")
print(f"Duplicatas eliminadas: {removed_count}")
