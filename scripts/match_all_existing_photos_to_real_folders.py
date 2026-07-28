import os
import json
import re

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
DADOS_DIR = os.path.join(SITE_DIR, "dados")
JSON_PATH = os.path.join(DADOS_DIR, "locais.json")
HTML_PATH = os.path.join(SITE_DIR, "index.html")
ADMIN_PATH = os.path.join(SITE_DIR, "admin.html")

known_photos = {
    "anunciata": "https://photos.app.goo.gl/JMSJy1nzX9ajbdpp8",
    "prefeitura": "https://photos.app.goo.gl/nx1uPz13BJmPBHEi6",
    "comite": "https://photos.app.goo.gl/WTVQgcxGrK2UgjCh8",
    "guariroba": "https://photos.app.goo.gl/2wWme9DCJPBdJyZM6",
    "recapex": "https://photos.app.goo.gl/yg4eRxLRCuXXXXUT9",
    "residencias": "https://photos.app.goo.gl/cvmhGtEaN2Tvc2Tw8",
    "scandar": "https://photos.app.goo.gl/ZJMuSzKDzQnzfDX1A",
    "parise": "https://photos.app.goo.gl/DoyFymckr14T448c9",
    "admo lui": "https://photos.app.goo.gl/2UDfbHg7URsesdEu9",
    "caetano decaro": "https://photos.app.goo.gl/bvSxyHa8EtgdY9x16",
    "calil jose": "https://photos.app.goo.gl/JeSnuDeX5RJveKpx8",
    "calil": "https://photos.app.goo.gl/JeSnuDeX5RJveKpx8",
    "heitor alves": "https://photos.app.goo.gl/w3Kns8cGNRCysGgMA",
    "perissinoti": "https://photos.app.goo.gl/Wg2z9Tkd6GZnpaGv5",
    "perissinotto": "https://photos.app.goo.gl/Wg2z9Tkd6GZnpaGv5",
    "camargo": "https://photos.app.goo.gl/nMXoz7drUgEPrVZp9",
    "zupanni": "https://photos.app.goo.gl/6gRJ7JWaZhxB2fvk8",
    "zuppani": "https://photos.app.goo.gl/6gRJ7JWaZhxB2fvk8",
    "adail": "https://photos.app.goo.gl/CnxBj426CBxfnVev9",
    "estevam": "https://photos.app.goo.gl/i6pCatFeZ3KNjrMK9",
    "mathilde": "https://photos.app.goo.gl/vfUG8JBz7uq3tcDv9",
    "modesto": "https://photos.app.goo.gl/7k2SoaRFMmrc1wM56",
    "franco": "https://photos.app.goo.gl/LgNKd7JbHKCTycjK7",
    "terazzi": "https://photos.app.goo.gl/Kc1GbYHQkSjsuymKA",
    "ubs ii": "https://photos.app.goo.gl/fYJ5x9QDgmHmSajx5"
}

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

locais = data.get("locais", [])

concluidos = 0
for loc in locais:
    nome_low = loc["nome"].lower()
    
    for k, photo_url in known_photos.items():
        if k in nome_low:
            loc["linkFotos"] = photo_url
            loc["fotos"] = photo_url
            loc["status"] = "concluido"
            break
            
    link = loc.get("linkFotos") or loc.get("fotos") or ""
    if link.strip() != "":
        loc["linkFotos"] = link.strip()
        loc["fotos"] = link.strip()
        loc["status"] = "concluido"
        concluidos += 1
        print(f"Concluido #{loc['id']} - {loc['nome']}")
    else:
        loc["status"] = "pendente"

data["total_concluidos"] = concluidos
data["total_pendentes"] = len(locais) - concluidos

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

print("\n=== VINCULO COMPLETO DAS FOTOS COM AS PASTAS REAIS ===")
print(f"Total de locais reais: {len(locais)}")
print(f"Total de concluidos com fotos (VERDES): {concluidos}")
print(f"Total de pendentes (faltam enviar): {len(locais) - concluidos}")
