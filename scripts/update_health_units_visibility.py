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

health_count = 0
for loc in locais:
    nome_lower = loc["nome"].lower()
    if "ubs" in nome_lower or "unidade de saúde" in nome_lower or "unidade de saude" in nome_lower or "postinho" in nome_lower:
        loc["exibirNoSite"] = False
        loc["reservado"] = True
        health_count += 1
        print(f"Reservado (Oculto no site público): {loc['nome']}")
    else:
        loc["exibirNoSite"] = True
        loc["reservado"] = False

visiveis = [l for l in locais if l.get("exibirNoSite", True)]
concluidos_publicos = sum(1 for l in visiveis if l["status"] == "concluido" or (l.get("linkFotos") or l.get("fotos")))
pendentes_publicos = len(visiveis) - concluidos_publicos

data["total_locais_publicos"] = len(visiveis)
data["total_concluidos_publicos"] = concluidos_publicos
data["total_pendentes_publicos"] = pendentes_publicos
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

filter_js = """    let rawLocaisData = (initialData && initialData.locais) ? initialData.locais.filter(l => l.exibirNoSite !== false) : [];"""
new_html = re.sub(r"let rawLocaisData = \(initialData && initialData\.locais\) \? initialData\.locais : \[\];", filter_js, new_html)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(new_html)

print("\n=== RESERVA DE UNIDADES DE SAUDE APLICADA ===")
print(f"Total de locais no sistema: {len(locais)}")
print(f"Unidades de Saúde reservadas/ocultas: {health_count}")
print(f"Locais exibidos publicamente: {len(visiveis)}")
print("locais.json e index.html atualizados com sucesso!")
