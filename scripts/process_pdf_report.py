import os
import json
import re
import pypdf

PDF_PATH = r"C:\Users\JOTABELIMA\Desktop\relatorio parcial do lugares atingidos.pdf"
SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
DADOS_DIR = os.path.join(SITE_DIR, "dados")
JSON_PATH = os.path.join(DADOS_DIR, "locais.json")
HTML_PATH = os.path.join(SITE_DIR, "index.html")

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

locais = data.get("locais", [])
print(f"Total de locais existentes no JSON: {len(locais)}")

reader = pypdf.PdfReader(PDF_PATH)
pdf_links = []

for page in reader.pages:
    if '/Annots' in page:
        annots = page['/Annots']
        for annot in annots:
            obj = annot.get_object()
            if '/A' in obj and '/URI' in obj['/A']:
                uri = obj['/A']['/URI']
                pdf_links.append(uri)

print(f"Hiperlinks extraidos do PDF: {len(pdf_links)}")

maps_links = [l for l in pdf_links if "google.com/maps" in l]
photos_links = [l for l in pdf_links if "photos.app.goo.gl" in l]

print(f"Links de Albuns de Fotos encontrados: {len(photos_links)}")

pdf_items = [
    {
        "nome": "EMEB Dr. Estevam Schlobach Salvagni",
        "endereco": "R. Cel. Gustavo A. de Moraes, 1704 - Vila Esperança - CEP 15900-000",
        "bairro": "Vila Esperança",
        "lat": -21.409558, "lng": -48.515813,
        "fotos": "https://photos.app.goo.gl/i6pCatFeZ3KNjrMK9"
    },
    {
        "nome": "Distrito de Guariroba",
        "endereco": "Distrito de Guariroba - Taquaritinga/SP - CEP 15900-000",
        "bairro": "Guariroba",
        "lat": -21.406900, "lng": -48.508000,
        "fotos": "https://photos.app.goo.gl/2wWme9DCJPBdJyZM6"
    },
    {
        "nome": "Residências Atingidas",
        "endereco": "Residências Atingidas Vendaval - Taquaritinga/SP - CEP 15900-000",
        "bairro": "Taquaritinga/SP",
        "lat": -21.406900, "lng": -48.508000,
        "fotos": "https://photos.app.goo.gl/cvmhGtEaN2Tvc2Tw8"
    },
    {
        "nome": "Clube da Assoc. dos Func. Públicos",
        "endereco": "Av. Francisco e Manuel Penteado, 171 - Conj. Hab. Manoel Lopes Moreno - CEP 15900-000",
        "bairro": "Conj. Hab. Manoel Lopes Moreno",
        "lat": -21.407150, "lng": -48.507820,
        "fotos": "https://photos.app.goo.gl/TSftLsucvZLWmLCp6"
    },
    {
        "nome": "Comitê de Crise da Prefeitura",
        "endereco": "R. Romeu Mársico, 200 - Centro - CEP 15900-000",
        "bairro": "Centro",
        "lat": -21.412022, "lng": -48.498371,
        "fotos": "https://photos.app.goo.gl/WTVQgcxGrK2UgjCh8"
    },
    {
        "nome": "Recapex Marangoni",
        "endereco": "R. Theodoro Davoglio, 400 - Setor Industrial - CEP 15900-000",
        "bairro": "Setor Industrial",
        "lat": -21.412700, "lng": -48.481882,
        "fotos": "https://photos.app.goo.gl/yg4eRxLRCuXXXXUT9"
    },
    {
        "nome": "Av. Paulo Roberto Scandar",
        "endereco": "Av. Paulo Roberto Scandar - Centro/Vila Nova - CEP 15900-001",
        "bairro": "Centro / Vila Nova",
        "lat": -21.402952, "lng": -48.508923,
        "fotos": "https://photos.app.goo.gl/ZJMuSzKDzQnzfDX1A"
    },
    {
        "nome": "Av. Vicente José Parise",
        "endereco": "Av. Vicente José Parise - Centro - CEP 15900-000",
        "bairro": "Centro",
        "lat": -21.404579, "lng": -48.497498,
        "fotos": "https://photos.app.goo.gl/DoyFymckr14T448c9"
    },
    {
        "nome": "Av. Mário da Silva Camargo",
        "endereco": "Av. Mário da Silva Camargo - Pq. Res. Laranjeiras II - CEP 15904-166",
        "bairro": "Pq. Res. Laranjeiras II",
        "lat": -21.406900, "lng": -48.508000,
        "fotos": "https://photos.app.goo.gl/nMXoz7drUgEPrVZp9"
    },
    {
        "nome": "Conj. Hab. Dr. Adail Nunes da Silva",
        "endereco": "Conj. Hab. Dr. Adail Nunes da Silva - CEP 15903-130/166",
        "bairro": "Dr. Adail Nunes da Silva",
        "lat": -21.385902, "lng": -48.492420,
        "fotos": "https://photos.app.goo.gl/CnxBj426CBxfnVev9"
    },
    {
        "nome": "Praça Guilherme José Franco",
        "endereco": "Praça Guilherme José Franco, 70-677 - Centro - CEP 15900-000",
        "bairro": "Centro",
        "lat": -21.397250, "lng": -48.510337,
        "fotos": "https://photos.app.goo.gl/LgNKd7JbHKCTycjK7"
    },
    {
        "nome": "Casa Terazzi",
        "endereco": "R. José Lourenço Machado, 62 - Jd. Ribeirãozinho - CEP 15901-096",
        "bairro": "Jd. Ribeirãozinho",
        "lat": -21.402488, "lng": -48.493295,
        "fotos": "https://photos.app.goo.gl/Kc1GbYHQkSjsuymKA"
    },
    {
        "nome": "UBS II Ederaldo A. P. Marques",
        "endereco": "Av. Heitor Alves Gomes, s/nº - Jd. Vale do Sol - CEP 15904-056",
        "bairro": "Jd. Vale do Sol",
        "lat": -21.402309, "lng": -48.483320,
        "fotos": "https://photos.app.goo.gl/fYJ5x9QDgmHmSajx5"
    }
]

atualizados = 0

for p_item in pdf_items:
    p_name = p_item["nome"].lower().strip()
    match = None
    for loc in locais:
        l_name = loc["nome"].lower().strip()
        if p_name in l_name or l_name in p_name:
            match = loc
            break
            
    if match:
        match["nome"] = p_item["nome"]
        match["endereco"] = p_item["endereco"]
        match["bairro"] = p_item["bairro"]
        match["lat"] = p_item["lat"]
        match["lng"] = p_item["lng"]
        match["linkFotos"] = p_item["fotos"]
        match["fotos"] = p_item["fotos"]
        match["status"] = "concluido"
        query_map = f"{match['nome']}, {match['endereco']}".replace(" ", "+")
        match["linkMaps"] = f"https://www.google.com/maps/search/?api=1&query={query_map}"
        atualizados += 1
        print(f"Atualizado do PDF: {match['nome']} -> Status: CONCLUIDO | Fotos: {match['linkFotos']}")
    else:
        next_id = max([l["id"] for l in locais]) + 1 if locais else 1
        query_map = f"{p_item['nome']}, {p_item['endereco']}".replace(" ", "+")
        new_loc = {
            "id": next_id,
            "nome": p_item["nome"],
            "endereco": p_item["endereco"],
            "bairro": p_item["bairro"],
            "lat": p_item["lat"],
            "lng": p_item["lng"],
            "status": "concluido",
            "linkMaps": f"https://www.google.com/maps/search/?api=1&query={query_map}",
            "linkFotos": p_item["fotos"],
            "fotos": p_item["fotos"],
            "dataAtendimento": "26/07/2026"
        }
        locais.append(new_loc)
        atualizados += 1
        print(f"Novo local do PDF adicionado: {new_loc['nome']} -> Status: CONCLUIDO | Fotos: {new_loc['linkFotos']}")

for loc in locais:
    if loc["id"] == 1 or "anunciata" in loc["nome"].lower():
        loc["linkFotos"] = "https://photos.app.goo.gl/JMSJy1nzX9ajbdpp8"
        loc["fotos"] = "https://photos.app.goo.gl/JMSJy1nzX9ajbdpp8"
        loc["status"] = "concluido"

concluidos = sum(1 for l in locais if l["status"] == "concluido" or (l.get("linkFotos") or l.get("fotos")))
pendentes = len(locais) - concluidos

data["total_locais"] = len(locais)
data["total_concluidos"] = concluidos
data["total_pendentes"] = pendentes
data["locais"] = locais
data["ultima_atualizacao"] = "26/07/2026 18:00:00 (Relatorio Defesa Civil)"

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

print("\n=== SUCESSO! ===")
print(f"Total de locais processados: {len(locais)}")
print(f"Total de locais ATENDIDOS/CONCLUIDOS (com fotos): {concluidos}")
print(f"Total de locais PENDENTES: {pendentes}")
print("locais.json e index.html atualizados com sucesso!")
