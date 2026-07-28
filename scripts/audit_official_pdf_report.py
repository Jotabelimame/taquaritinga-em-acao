import os
import json
import re

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
JSON_PATH = os.path.join(SITE_DIR, "dados", "locais.json")
HTML_PATH = os.path.join(SITE_DIR, "index.html")

# Dados oficiais extraídos do relatório em PDF da Defesa Civil
pdf_items = [
    {
        "num": "01",
        "nome": "EMEB Dr. Estevam Schlobach Salvagni",
        "endereco": "R. Cel. Gustavo A. de Moraes, 1704 • Vila Esperança • CEP 15900-000",
        "bairro": "Vila Esperança",
        "lat": -21.409558,
        "lng": -48.515813
    },
    {
        "num": "02",
        "nome": "Distrito de Guariroba",
        "endereco": "Guariroba • Taquaritinga/SP • CEP 15900-000",
        "bairro": "Distrito de Guariroba",
        "lat": -21.406900,
        "lng": -48.508000
    },
    {
        "num": "03",
        "nome": "Residências Atingidas",
        "endereco": "Taquaritinga/SP • CEP 15900-000",
        "bairro": "Taquaritinga/SP",
        "lat": -21.406900,
        "lng": -48.508000
    },
    {
        "num": "04",
        "nome": "Clube da Assoc. dos Func. Públicos",
        "endereco": "Av. Francisco e Manuel Penteado, 171 • Conj. Hab. Manoel Lopes Moreno • CEP 15900-000",
        "bairro": "Conj. Hab. Manoel Lopes Moreno",
        "lat": -21.407150,
        "lng": -48.507820
    },
    {
        "num": "05",
        "nome": "Comitê de Crise da Prefeitura",
        "endereco": "R. Romeu Mársico, 200 • Centro • CEP 15900-000",
        "bairro": "Centro",
        "lat": -21.412022,
        "lng": -48.498371
    },
    {
        "num": "06",
        "nome": "Recapex Marangoni",
        "endereco": "R. Theodoro Davoglio, 400 • Setor Industrial • CEP 15900-000",
        "bairro": "Setor Industrial",
        "lat": -21.41269985,
        "lng": -48.48188180
    },
    {
        "num": "09",
        "nome": "Av. Paulo Roberto Scandar",
        "endereco": "Av. Paulo Roberto Scandar • Centro/Vila Nova • CEP 15900-001",
        "bairro": "Centro/Vila Nova",
        "lat": -21.402952,
        "lng": -48.508923
    },
    {
        "num": "10",
        "nome": "Av. Vicente José Parise",
        "endereco": "Av. Vicente José Parise • Centro • CEP 15900-000",
        "bairro": "Centro",
        "lat": -21.404579,
        "lng": -48.497498
    },
    {
        "num": "11",
        "nome": "Av. Mário da Silva Camargo",
        "endereco": "Av. Mário da Silva Camargo • Pq. Res. Laranjeiras II • CEP 15904-166",
        "bairro": "Pq. Res. Laranjeiras II",
        "lat": -21.406900,
        "lng": -48.508000
    },
    {
        "num": "12",
        "nome": "Conj. Hab. Dr. Adail Nunes da Silva",
        "endereco": "Conj. Hab. Dr. Adail Nunes da Silva • CEP 15903-130/166",
        "bairro": "Conj. Hab. Dr. Adail Nunes da Silva",
        "lat": -21.385902,
        "lng": -48.492420
    },
    {
        "num": "19",
        "nome": "Praça Guilherme José Franco",
        "endereco": "Praça Guilherme José Franco, 70-677 • Centro • CEP 15900-000",
        "bairro": "Centro",
        "lat": -21.397250,
        "lng": -48.510337
    },
    {
        "num": "--",
        "nome": "Casa Terazzi",
        "endereco": "R. José Lourenço Machado, 62 • Jd. Ribeirãozinho • CEP 15901-096",
        "bairro": "Jd. Ribeirãozinho",
        "lat": -21.402488,
        "lng": -48.493295
    },
    {
        "num": "--",
        "nome": "UBS II Ederaldo A. P. Marques",
        "endereco": "Av. Heitor Alves Gomes, s/nº • Jd. Vale do Sol • CEP 15904-056",
        "bairro": "Jd. Vale do Sol",
        "lat": -21.402309,
        "lng": -48.483320,
        "exibirNoSite": False
    }
]

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

locais = data.get("locais", [])

updated_count = 0
for item in pdf_items:
    nome_low = item["nome"].lower().replace("dr.", "").replace("prof.", "").strip()
    match = None
    for l in locais:
        l_low = l["nome"].lower()
        if nome_low in l_low or l_low in nome_low:
            match = l
            break
            
    if match:
        match["nome"] = item["nome"]
        match["endereco"] = item["endereco"]
        match["bairro"] = item["bairro"]
        match["lat"] = round(item["lat"], 6)
        match["lng"] = round(item["lng"], 6)
        match["maps"] = f"https://www.google.com/maps/search/?api=1&query={item['lat']},{item['lng']}"
        match["linkMaps"] = match["maps"]
        match["rota"] = f"https://www.google.com/maps/dir/?api=1&destination={item['lat']},{item['lng']}"
        if "exibirNoSite" in item:
            match["exibirNoSite"] = item["exibirNoSite"]
        updated_count += 1
        print(f"AUDITADO #{match['id']} - {match['nome']} -> GPS: {match['lat']}, {match['lng']}")

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

print("\n=== AUDITORIA COMPLETA DO RELATÓRIO DA DEFESA CIVIL FINALIZADA ===")
print(f"Total de registros auditados e atualizados com o PDF oficial: {updated_count}")
