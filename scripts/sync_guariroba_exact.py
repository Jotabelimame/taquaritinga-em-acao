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

GUARIROBA_FOTOS = "https://photos.app.goo.gl/2wWme9DCJPBdJyZM6"
GUARIROBA_MAPS = "https://www.google.com/maps/place/Distrito+Guariroba,+Taquaritinga+-+SP"
GUARIROBA_ROTA = "https://www.google.com/maps/dir/?api=1&destination=-21.406900,-48.508000"

guariroba_entries = []
for idx, loc in enumerate(locais):
    if "guariroba" in loc["nome"].lower():
        guariroba_entries.append(idx)

print(f"Ocorrências de Guariroba no locais.json: {guariroba_entries}")

if guariroba_entries:
    first_idx = guariroba_entries[0]
    locais[first_idx]["nome"] = "Distrito de Guariroba"
    locais[first_idx]["endereco"] = "Distrito de Guariroba • Taquaritinga/SP • CEP 15900-000"
    locais[first_idx]["bairro"] = "Guariroba"
    locais[first_idx]["lat"] = -21.406900
    locais[first_idx]["lng"] = -48.508000
    locais[first_idx]["rota"] = GUARIROBA_ROTA
    locais[first_idx]["maps"] = GUARIROBA_MAPS
    locais[first_idx]["linkMaps"] = GUARIROBA_MAPS
    locais[first_idx]["fotos"] = GUARIROBA_FOTOS
    locais[first_idx]["linkFotos"] = GUARIROBA_FOTOS
    locais[first_idx]["status"] = "concluido"

    # Se houver mais de um registro de Guariroba, remover os duplicados
    for del_idx in sorted(guariroba_entries[1:], reverse=True):
        locais.pop(del_idx)
        print(f"Removida duplicata de Guariroba no índice {del_idx}")

# Reindexar IDs
for new_id, loc in enumerate(locais, start=1):
    loc["id"] = new_id

total_locais = len(locais)
total_concluidos = sum(1 for l in locais if l["status"] == "concluido" or (l.get("linkFotos") or l.get("fotos")))
total_pendentes = total_locais - total_concluidos

data["total_locais"] = total_locais
data["total_concluidos"] = total_concluidos
data["total_pendentes"] = total_pendentes
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

print("\n=== DADOS EXATOS DO DISTRITO DE GUARIROBA ATUALIZADOS ===")
print(f"Total locais: {total_locais} | Concluídos: {total_concluidos} | Pendentes: {total_pendentes}")
