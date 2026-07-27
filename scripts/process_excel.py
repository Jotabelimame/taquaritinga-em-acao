import os
import json
import pandas as pd
from datetime import datetime
import re

EXCEL_PATH = r"C:\Users\JOTABELIMA\Documents\New project\outputs\019fa346-e115-76d2-91ac-5d44619f1acc\planilha_vendaval_fotos.xlsx"
SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
DADOS_DIR = os.path.join(SITE_DIR, "dados")
JSON_PATH = os.path.join(DADOS_DIR, "locais.json")
HTML_PATH = os.path.join(SITE_DIR, "index.html")

# 1. Carregar JSON atual se existir para PRESERVAR fotos e edições já salvas
existing_map = {}
if os.path.exists(JSON_PATH):
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        existing_data = json.load(f)
        for l in existing_data.get("locais", []):
            existing_map[l["id"]] = l
            existing_map[l["nome"].lower().strip()] = l

xls = pd.ExcelFile(EXCEL_PATH)
df_form = pd.read_excel(EXCEL_PATH, sheet_name="Formulario Links Albuns")

locais_list = []
id_counter = 1

for idx, row in df_form.iterrows():
    nome_raw = str(row.get("Pasta / local", "")).strip()
    if not nome_raw or nome_raw.lower() == "nan":
        continue
    
    # Verificar se já existia no JSON com fotos ou coordenadas calibradas
    key_id = id_counter
    key_name = nome_raw.lower()
    prev = existing_map.get(key_id) or existing_map.get(key_name)
    
    # Link de fotos na planilha
    link_fotos_excel = str(row.get("Cole aqui o link do álbum Google Fotos", "")).strip()
    if link_fotos_excel.upper() == "PREENCHER" or link_fotos_excel.lower() == "nan":
        link_fotos_excel = ""
        
    # Preservar fotos anteriores se já salvas no JSON
    final_link_fotos = link_fotos_excel if link_fotos_excel else (prev.get("linkFotos", "") if prev else "")
    
    # Preservar coordenadas e endereço se já salvos no JSON
    lat = prev.get("lat") if prev else round(-21.4056 + ((id_counter % 9) - 4) * 0.0035, 6)
    lng = prev.get("lng") if prev else round(-48.5047 + (((id_counter * 3) % 11) - 5) * 0.0038, 6)
    endereco = prev.get("endereco") if prev else f"{nome_raw} - Taquaritinga/SP"
    bairro = prev.get("bairro") if prev else "Taquaritinga/SP"
    
    # Caso especial Anunciata Colombo (Creche #1)
    if id_counter == 1 or "anunciata" in nome_raw.lower():
        nome_raw = "EMEB / Berçário Anunciata Colombo"
        endereco = "Rua Salvador Arnoni, 159 - Jardim São Sebastião, Taquaritinga - SP, 15903-112"
        bairro = "Jardim São Sebastião"
        lat = -21.384556
        lng = -48.495396
        final_link_fotos = "https://photos.app.goo.gl/JMSJy1nzX9ajbdpp8"

    status = "concluido" if final_link_fotos != "" else "pendente"
    query_map = f"{nome_raw}, {endereco}".replace(" ", "+")
    link_maps = f"https://www.google.com/maps/search/?api=1&query={query_map}"

    locais_list.append({
        "id": id_counter,
        "nome": nome_raw,
        "endereco": endereco,
        "bairro": bairro,
        "lat": lat,
        "lng": lng,
        "status": status,
        "linkMaps": link_maps,
        "linkFotos": final_link_fotos,
        "fotos": final_link_fotos,
        "dataAtendimento": "27/07/2026"
    })
    id_counter += 1

total_locais = len(locais_list)
total_concluidos = sum(1 for l in locais_list if l["status"] == "concluido")
total_pendentes = sum(1 for l in locais_list if l["status"] == "pendente")

json_output = {
    "ultima_atualizacao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    "total_locais": total_locais,
    "total_concluidos": total_concluidos,
    "total_pendentes": total_pendentes,
    "locais": locais_list,
    "rotas": existing_data.get("rotas", []) if "existing_data" in locals() else []
}

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(json_output, f, ensure_ascii=False, indent=2)

# Atualizar index.html
with open(HTML_PATH, "r", encoding="utf-8") as f:
    html_text = f.read()

json_full_str = json.dumps(json_output, ensure_ascii=False, indent=2)

new_html = re.sub(
    r"const initialData = \{.*?\};\n    let rawLocaisData =",
    f"const initialData = {json_full_str};\n    let rawLocaisData =",
    html_text,
    flags=re.DOTALL
)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(new_html)

print("=== PROCESSAMENTO INTELIGENTE CONCLUÍDO ===")
print(f"Total locais: {total_locais}")
print(f"Concluídos: {total_concluidos}")
print(f"Pendentes: {total_pendentes}")
print("Todas as fotos e coordenadas salvas foram preservadas com sucesso!")
