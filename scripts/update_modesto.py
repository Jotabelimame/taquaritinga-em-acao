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

LAT = -21.407018
LNG = -48.510202
NOME = "EMEB Modesto de Souza Dias"
ENDERECO = "R. Enês Réis Rodrigues, 71 - Jd. Bela Vista, Taquaritinga - SP, 15905-004"
BAIRRO = "Jardim Bela Vista"

MAPS = f"https://www.google.com/maps/search/?api=1&query={NOME.replace(' ', '+')}+Taquaritinga+SP"
ROTA = f"https://www.google.com/maps/dir/?api=1&destination={LAT},{LNG}"

found = False
for loc in locais:
    nome_low = loc["nome"].lower()
    if loc["id"] == 21 or "modesto de souza" in nome_low:
        loc["nome"] = NOME
        loc["endereco"] = ENDERECO
        loc["bairro"] = BAIRRO
        loc["lat"] = LAT
        loc["lng"] = LNG
        loc["maps"] = MAPS
        loc["linkMaps"] = MAPS
        loc["rota"] = ROTA
        found = True
        print(f"Atualizado Local #{loc['id']}: {loc['nome']} -> {loc['endereco']} ({loc['lat']}, {loc['lng']})")

if not found:
    next_id = max([l["id"] for l in locais]) + 1 if locais else 21
    new_loc = {
        "id": next_id,
        "nome": NOME,
        "endereco": ENDERECO,
        "bairro": BAIRRO,
        "lat": LAT,
        "lng": LNG,
        "status": "pendente",
        "maps": MAPS,
        "linkMaps": MAPS,
        "rota": ROTA,
        "linkFotos": "",
        "fotos": "",
        "dataAtendimento": "27/07/2026"
    }
    locais.append(new_loc)
    print(f"Novo Local #{next_id} cadastrado: {NOME}!")

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

print("\n=== ATUALIZACAO DA EMEB MODESTO DE SOUZA DIAS CONCLUIDA ===")
print(f"Total locais: {total_locais} | Concluidos: {total_concluidos} | Pendentes: {total_pendentes}")
