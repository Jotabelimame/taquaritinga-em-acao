import os
import json
import pandas as pd
import re

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
DADOS_DIR = os.path.join(SITE_DIR, "dados")
JSON_PATH = os.path.join(DADOS_DIR, "locais.json")
HTML_PATH = os.path.join(SITE_DIR, "index.html")
EXCEL_PATH = r"C:\Users\JOTABELIMA\Documents\New project\outputs\019fa346-e115-76d2-91ac-5d44619f1acc\planilha_vendaval_fotos.xlsx"

df_pastas = pd.read_excel(EXCEL_PATH, sheet_name="Pastas da Pasta")
real_folders = []
for idx, row in df_pastas.iterrows():
    p = str(row.get("Pasta / local")).strip()
    if p and p.lower() != "nan":
        real_folders.append(p)

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

existing_locais = data.get("locais", [])
existing_map = {}
for l in existing_locais:
    existing_map[l["nome"].lower().strip()] = l

new_locais = []
id_counter = 1

for folder_name in real_folders:
    if folder_name.lower() in ["videos mp4", "organizado_por_endereco"]:
        continue
        
    f_low = folder_name.lower().strip()
    
    prev = None
    for k, v in existing_map.items():
        if k in f_low or f_low in k:
            prev = v
            break
            
    link_fotos = (prev.get("linkFotos") or prev.get("fotos")) if prev else ""
    status = "concluido" if (link_fotos and link_fotos.strip() != "") else "pendente"
    
    endereco = (prev.get("endereco") if prev else f"{folder_name} - Taquaritinga/SP")
    bairro = (prev.get("bairro") if prev else "Taquaritinga/SP")
    lat = (prev.get("lat") if prev else round(-21.4056 + ((id_counter % 9) - 4) * 0.0035, 6))
    lng = (prev.get("lng") if prev else round(-48.5047 + (((id_counter * 3) % 11) - 5) * 0.0038, 6))
    
    query_map = f"{folder_name}, Taquaritinga SP".replace(" ", "+")
    link_maps = (prev.get("linkMaps") if prev else f"https://www.google.com/maps/search/?api=1&query={query_map}")
    rota = (prev.get("rota") if prev else f"https://www.google.com/maps/dir/?api=1&destination={lat},{lng}")
    
    exibir = True
    if "ubs" in f_low or "posto de saude" in f_low or "posto de saúde" in f_low:
        exibir = False

    new_locais.append({
        "id": id_counter,
        "nome": folder_name,
        "endereco": endereco,
        "bairro": bairro,
        "lat": lat,
        "lng": lng,
        "status": status,
        "linkMaps": link_maps,
        "maps": link_maps,
        "rota": rota,
        "linkFotos": link_fotos or "",
        "fotos": link_fotos or "",
        "exibirNoSite": exibir,
        "dataAtendimento": "27/07/2026"
    })
    id_counter += 1

total_locais = len(new_locais)
total_concluidos = sum(1 for l in new_locais if l["status"] == "concluido" or (l.get("linkFotos") or l.get("fotos")))
total_pendentes = total_locais - total_concluidos

data["total_locais"] = total_locais
data["total_concluidos"] = total_concluidos
data["total_pendentes"] = total_pendentes
data["locais"] = new_locais
data["ultima_atualizacao"] = "28/07/2026 00:16:00 (Pastas Reais E:\\)"

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

print("\n=== SINCRONIZACAO COMPLETA DAS PASTAS REAIS DA UNIDADE E:\\ CONCLUIDA ===")
print(f"Total de locais reais alinhados com a sua pasta: {total_locais}")
print(f"Total de concluidos com fotos: {total_concluidos}")
print(f"Total de pendentes: {total_pendentes}")
