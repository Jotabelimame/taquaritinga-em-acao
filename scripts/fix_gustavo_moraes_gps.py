import os
import json
import re

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
JSON_PATH = os.path.join(SITE_DIR, "dados", "locais.json")
HTML_PATH = os.path.join(SITE_DIR, "index.html")

LAT_EXATA = -21.408216
LNG_EXATA = -48.515968
ENDERECO_OFICIAL = "R. Cel. Gustavo A. de Moraes, 1704 - Vila Esperança, Taquaritinga - SP, CEP 15900-000"

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

locais = data.get("locais", [])

updated = 0
for loc in locais:
    nome_low = loc["nome"].lower()
    end_low = loc.get("endereco", "").lower()
    if "gustavo" in nome_low or "gustavo" in end_low or "estevam" in nome_low:
        loc["lat"] = LAT_EXATA
        loc["lng"] = LNG_EXATA
        loc["endereco"] = ENDERECO_OFICIAL
        query_map = "Rua+Cel.+Gustavo+A.+de+Moraes+Taquaritinga+SP"
        loc["maps"] = f"https://www.google.com/maps/search/?api=1&query={query_map}"
        loc["linkMaps"] = loc["maps"]
        loc["rota"] = f"https://www.google.com/maps/dir/?api=1&destination={LAT_EXATA},{LNG_EXATA}"
        updated += 1
        print(f"GPS E ENDERECO ATUALIZADOS #{loc['id']} - {loc['nome']} -> ({LAT_EXATA}, {LNG_EXATA})")

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

print(f"\n=== CORRECAO DA R. CEL. GUSTAVO A. DE MORAES FINALIZADA ===")
print(f"Total de registros atualizados no mapa: {updated}")
