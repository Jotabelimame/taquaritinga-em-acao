import os
import json
import re

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
DADOS_DIR = os.path.join(SITE_DIR, "dados")
JSON_PATH = os.path.join(DADOS_DIR, "locais.json")
HTML_PATH = os.path.join(SITE_DIR, "index.html")
ADMIN_PATH = os.path.join(SITE_DIR, "admin.html")

pdf_photos = {
    "guariroba": "https://photos.app.goo.gl/2wWme9DCJPBdJyZM6",
    "recapex": "https://photos.app.goo.gl/yg4eRxLRCuXXXXUT9",
    "residencias": "https://photos.app.goo.gl/cvmhGtEaN2Tvc2Tw8",
    "estevam": "https://photos.app.goo.gl/i6pCatFeZ3KNjrMK9",
    "clube": "https://photos.app.goo.gl/TSftLsucvZLWmLCp6",
    "comitê": "https://photos.app.goo.gl/WTVQgcxGrK2UgjCh8",
    "comite": "https://photos.app.goo.gl/WTVQgcxGrK2UgjCh8",
    "scandar": "https://photos.app.goo.gl/ZJMuSzKDzQnzfDX1A",
    "parise": "https://photos.app.goo.gl/DoyFymckr14T448c9",
    "camargo": "https://photos.app.goo.gl/nMXoz7drUgEPrVZp9",
    "adail": "https://photos.app.goo.gl/CnxBj426CBxfnVev9",
    "franco": "https://photos.app.goo.gl/LgNKd7JbHKCTycjK7",
    "terazzi": "https://photos.app.goo.gl/Kc1GbYHQkSjsuymKA",
    "ubs ii": "https://photos.app.goo.gl/fYJ5x9QDgmHmSajx5"
}

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

locais = data.get("locais", [])

concluidos_count = 0
for loc in locais:
    nome_low = loc["nome"].lower()
    
    for key, photo_url in pdf_photos.items():
        if key in nome_low:
            loc["linkFotos"] = photo_url
            loc["fotos"] = photo_url
            break

    link = loc.get("linkFotos") or loc.get("fotos") or ""
    if link.strip() != "":
        loc["status"] = "concluido"
        concluidos_count += 1
        print(f"Concluido #{loc['id']} - {loc['nome']} -> {link}")
    else:
        if loc.get("status") != "concluido":
            loc["status"] = "pendente"

data["total_concluidos"] = concluidos_count
data["total_pendentes"] = len(locais) - concluidos_count

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

with open(ADMIN_PATH, "r", encoding="utf-8") as f:
    admin_text = f.read()

admin_fix = """            dadosLocais.forEach((item, idx) => {
                const linkFotos = item.linkFotos || item.fotos || '';
                const isConcluido = (item.status === 'concluido') || (linkFotos.trim() !== '');
                const statusStr = isConcluido ? 'Concluído' : 'Pendente';"""

admin_text = re.sub(
    r"dadosLocais\.forEach\(\(item, idx\) => \{.*?const statusStr = isConcluido \? 'Concluído' : 'Pendente';",
    admin_fix,
    admin_text,
    flags=re.DOTALL
)

with open(ADMIN_PATH, "w", encoding="utf-8") as f:
    f.write(admin_text)

print("\n=== AJUSTE E HARMONIZACAO DE FOTOS E STATUS CONCLUIDO ===")
print(f"Total de locais: {len(locais)}")
print(f"Total de locais com STATUS CONCLUIDO (Verde): {concluidos_count}")
print("locais.json, index.html e admin.html atualizados com sucesso!")
