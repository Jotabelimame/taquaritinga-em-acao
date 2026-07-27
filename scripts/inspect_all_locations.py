import os
import json
import requests
import time

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
JSON_PATH = os.path.join(SITE_DIR, "dados", "locais.json")

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

locais = data.get("locais", [])
print(f"Total de locais a inspecionar: {len(locais)}\n")

for loc in locais:
    print(f"ID {loc['id']:02d}: {loc['nome']} | Endereço: {loc['endereco']}")
