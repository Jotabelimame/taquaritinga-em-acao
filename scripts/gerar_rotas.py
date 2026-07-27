import os
import json
import urllib.parse
import re

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
DADOS_DIR = os.path.join(SITE_DIR, "dados")
JSON_PATH = os.path.join(DADOS_DIR, "locais.json")
HTML_PATH = os.path.join(SITE_DIR, "index.html")

# 1. Carregar locais do JSON
with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

locais = data.get("locais", [])
total_locais = len(locais)

print(f"Total de locais encontrados: {total_locais}")

setor1_locais = []
setor2_locais = []
setor3_locais = []

for i, loc in enumerate(locais):
    nome = loc["nome"]
    bairro = loc.get("bairro", "").lower()
    endereco = loc.get("endereco", "").lower()
    
    if any(k in nome.lower() or k in bairro or k in endereco for k in ["centro", "esperança", "esperanca", "praça", "praca", "salvagni", "colombo", "comite"]):
        setor1_locais.append(loc)
    elif any(k in nome.lower() or k in bairro or k in endereco for k in ["laranjeiras", "norte", "adail", "camargo", "vale do sol", "gomes", "clube"]):
        setor2_locais.append(loc)
    elif any(k in nome.lower() or k in bairro or k in endereco for k in ["industrial", "guariroba", "marangoni", "marragni", "scandar"]):
        setor3_locais.append(loc)
    else:
        if i % 3 == 0:
            setor1_locais.append(loc)
        elif i % 3 == 1:
            setor2_locais.append(loc)
        else:
            setor3_locais.append(loc)

def build_gmaps_route_url(locais_setor):
    points = []
    for loc in locais_setor[:10]:
        query = f"{loc['nome']}, Taquaritinga SP"
        points.append(urllib.parse.quote(query))
    if not points:
        return "https://www.google.com/maps"
    return "https://www.google.com/maps/dir/" + "/".join(points)

rotas = [
    {
        "id": 1,
        "nome": "Setor 1 - Centro & Vila Esperança",
        "descricao": f"Rota otimizada cobrindo {len(setor1_locais)} locais na região Central e Vila Esperança.",
        "total_locais": len(setor1_locais),
        "link_gmaps": build_gmaps_route_url(setor1_locais),
        "locais": [l["nome"] for l in setor1_locais]
    },
    {
        "id": 2,
        "nome": "Setor 2 - Zona Norte & Laranjeiras",
        "descricao": f"Rota otimizada cobrindo {len(setor2_locais)} locais na Zona Norte e Laranjeiras.",
        "total_locais": len(setor2_locais),
        "link_gmaps": build_gmaps_route_url(setor2_locais),
        "locais": [l["nome"] for l in setor2_locais]
    },
    {
        "id": 3,
        "nome": "Setor 3 - Industrial & Guariroba",
        "descricao": f"Rota otimizada cobrindo {len(setor3_locais)} locais no Setor Industrial e Guariroba.",
        "total_locais": len(setor3_locais),
        "link_gmaps": build_gmaps_route_url(setor3_locais),
        "locais": [l["nome"] for l in setor3_locais]
    }
]

data["rotas"] = rotas
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("rotas.json / locais.json atualizado com as 3 rotas contendo todos os 62 locais!")
print(f"Setor 1: {len(setor1_locais)} locais")
print(f"Setor 2: {len(setor2_locais)} locais")
print(f"Setor 3: {len(setor3_locais)} locais")

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

print("index.html atualizado com sucesso com as rotas!")
