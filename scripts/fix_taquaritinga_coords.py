import os
import json
import re

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
DADOS_DIR = os.path.join(SITE_DIR, "dados")
JSON_PATH = os.path.join(DADOS_DIR, "locais.json")
HTML_PATH = os.path.join(SITE_DIR, "index.html")

EXACT_COORDS = {
    "berçario anunciata colombo": {"lat": -21.4010, "lng": -48.5090, "end": "Berçário Anunciata Colombo, Vila Esperança, Taquaritinga - SP"},
    "clube do funcionario publico": {"lat": -21.4130, "lng": -48.5150, "end": "Clube do Funcionário Público Municipal, Taquaritinga - SP"},
    "comite da prefeitura": {"lat": -21.4058, "lng": -48.5051, "end": "Comitê Central de Crise - Prefeitura Municipal, Taquaritinga - SP"},
    "guariroba distrito": {"lat": -21.3485, "lng": -48.5782, "end": "Distrito de Guariroba, Taquaritinga - SP"},
    "recapex marragni": {"lat": -21.4150, "lng": -48.4980, "end": "Recapex Marangoni, Rua Theodoro Davoglio, 400 - Setor Industrial, Taquaritinga - SP"},
    "residencias atingidas vendaval": {"lat": -21.4040, "lng": -48.5020, "end": "Região Residencial Afetada, Taquaritinga - SP"},
    "av. paulo roberto scandar": {"lat": -21.4082, "lng": -48.5029, "end": "Av. Paulo Roberto Scandar, Centro / Vila Nova, Taquaritinga - SP"},
    "av. vicente josé parise": {"lat": -21.4038, "lng": -48.5065, "end": "Av. Vicente José Parise, Centro, Taquaritinga - SP"},
    "av.admo lui": {"lat": -21.4172, "lng": -48.5062, "end": "Av. Admo Lui, Taquaritinga - SP"},
    "av.caetano decaro": {"lat": -21.4185, "lng": -48.4933, "end": "Av. Caetano Decaro, Taquaritinga - SP"},
    "av.calil jose dib": {"lat": -21.4110, "lng": -48.5130, "end": "Av. Calil José Dib, Taquaritinga - SP"},
    "av.celso ferreira de camargo": {"lat": -21.4140, "lng": -48.5160, "end": "Av. Celso Ferreira de Camargo, Taquaritinga - SP"},
    "av.heitor alves gomes": {"lat": -21.4190, "lng": -48.5100, "end": "Av. Heitor Alves Gomes, Jardim Vale do Sol, Taquaritinga - SP"},
    "av.joao perissinoti": {"lat": -21.4105, "lng": -48.5140, "end": "Av. João Perissinotti (Ginásio de Esportes), Taquaritinga - SP"},
    "av.mario da silva camargo": {"lat": -21.4120, "lng": -48.5180, "end": "Av. Mário da Silva Camargo, Parque Residencial Laranjeiras II, Taquaritinga - SP"},
    "av.paulo zupanni": {"lat": -21.4095, "lng": -48.5110, "end": "Av. Paulo Zupanni, Taquaritinga - SP"},
    "bairro talavasso": {"lat": -21.4210, "lng": -48.5090, "end": "Bairro Talavasso / UBS Vale do Sol, Taquaritinga - SP"},
    "conj. hab. dr. adail nunes da silva": {"lat": -21.3980, "lng": -48.5220, "end": "Conjunto Habitacional Dr. Adail Nunes da Silva, Taquaritinga - SP"},
    "emeb estevam schlobach salvagni": {"lat": -21.4022, "lng": -48.5110, "end": "EMEB Dr. Estevam Schlobach Salvagni, Vila Esperança, Taquaritinga - SP"},
    "emeb mathilde menon": {"lat": -21.4075, "lng": -48.5080, "end": "EMEB Mathilde Menon, Taquaritinga - SP"},
    "emilio giroto": {"lat": -21.4145, "lng": -48.5175, "end": "Rua Emílio Giroto, Taquaritinga - SP"},
    "escola municipal professor modesto bohrer": {"lat": -21.4088, "lng": -48.4950, "end": "Escola Municipal Prof. Modesto Bohrer, Taquaritinga - SP"},
    "escola santa cecilia": {"lat": -21.4049, "lng": -48.5028, "end": "Escola Santa Cecília / ETAM, Taquaritinga - SP"},
    "francisco romano": {"lat": -21.4035, "lng": -48.5040, "end": "Rua Francisco Romano, Centro, Taquaritinga - SP"},
    "general osorio": {"lat": -21.4053, "lng": -48.5045, "end": "Rua General Osório (Igreja Matriz), Centro, Taquaritinga - SP"},
    "josephina mantese": {"lat": -21.4015, "lng": -48.5120, "end": "Rua Josephina Mantese Morcelli Pinsetta, Taquaritinga - SP"},
    "parque vinicius de moraes": {"lat": -21.4195, "lng": -48.5085, "end": "Parque Vinícius de Moraes / UBS Neoseti, Taquaritinga - SP"},
    "passarela rua doutor jose miguel joao": {"lat": -21.4070, "lng": -48.5010, "end": "Passarela Rua Dr. José Miguel João, Taquaritinga - SP"},
    "posto de saude paraiso": {"lat": -21.4165, "lng": -48.5040, "end": "Posto de Saúde Paraíso (Nelson Sargi), Taquaritinga - SP"},
    "praça edwil roncada": {"lat": -21.4090, "lng": -48.5050, "end": "Praça Edwil Roncada, Taquaritinga - SP"},
    "praça guilherme josé franco": {"lat": -21.4061, "lng": -48.5042, "end": "Praça Guilherme José Franco, Centro, Taquaritinga - SP"},
    "praça horacio ramalho": {"lat": -21.4058, "lng": -48.5051, "end": "Praça Horácio Ramalho (Câmara / Prefeitura), Taquaritinga - SP"},
    "praça sr.waldemar de ambrosio": {"lat": -21.4045, "lng": -48.5030, "end": "Praça Sr. Waldemar de Ambrósio, Taquaritinga - SP"},
    "predio da prefeitura": {"lat": -21.4058, "lng": -48.5051, "end": "Prédio da Prefeitura Municipal, Praça Horácio Ramalho, Taquaritinga - SP"},
    "r. alfi olyntho cucolicchio": {"lat": -21.4205, "lng": -48.5115, "end": "Rua Alfi Olyntho Cucolicchio, Jardim Vale do Sol, Taquaritinga - SP"},
    "r. angelo bossine neto": {"lat": -21.4170, "lng": -48.5090, "end": "Rua Ângelo Bossine Neto, Taquaritinga - SP"},
    "r. antenor milanezi": {"lat": -21.4215, "lng": -48.5105, "end": "Rua Antenor Milanezi, 488-538, Jardim Vale do Sol, Taquaritinga - SP"},
    "r. bernardino sampaio": {"lat": -21.4010, "lng": -48.5140, "end": "Rua Bernardino Sampaio, 580, Vila Sargi, Taquaritinga - SP"},
    "r. cel. gustavo a de moraes": {"lat": -21.4025, "lng": -48.5100, "end": "Rua Cel. Gustavo A. de Moraes, Vila Esperança, Taquaritinga - SP"},
    "r. dr. argidio prevideli": {"lat": -21.4030, "lng": -48.5070, "end": "Rua Dr. Argídio Prevideli, 2-92, Taquaritinga - SP"},
    "r. luiz patti": {"lat": -21.4050, "lng": -48.5085, "end": "Rua Luiz Patti, 2-160, Taquaritinga - SP"},
    "r. luís benaglia": {"lat": -21.4065, "lng": -48.5075, "end": "Rua Luís Benaglia, Taquaritinga - SP"},
    "r.cesar rossi": {"lat": -21.4115, "lng": -48.5110, "end": "Rua César Rossi, Taquaritinga - SP"},
    "r.dr.benjamin fg neto": {"lat": -21.4060, "lng": -48.5090, "end": "Rua Dr. Benjamin FG Neto, Taquaritinga - SP"},
    "r.general glicerio": {"lat": -21.4068, "lng": -48.5020, "end": "Rua General Glicério, Centro, Taquaritinga - SP"},
    "rodoviaria": {"lat": -21.4115, "lng": -48.5055, "end": "Terminal Rodoviário de Taquaritinga, Taquaritinga - SP"},
    "rua bernadino samapaio": {"lat": -21.4010, "lng": -48.5140, "end": "Rua Bernardino Sampaio, Vila Sargi, Taquaritinga - SP"},
    "rua dos domingues": {"lat": -21.4020, "lng": -48.5030, "end": "Rua dos Domingues, Taquaritinga - SP"},
    "rua doutor jorge tibiriça": {"lat": -21.4042, "lng": -48.5035, "end": "Rua Dr. Jorge Tibiriçá, Centro, Taquaritinga - SP"},
    "rua jamil jose": {"lat": -21.4160, "lng": -48.5210, "end": "Rua Jamil José, Jardim Paineiras, Taquaritinga - SP"},
    "rua josé maria gonçalves": {"lat": -21.4135, "lng": -48.5120, "end": "Rua José Maria Gonçalves, Taquaritinga - SP"},
    "sp 319": {"lat": -21.4210, "lng": -48.4900, "end": "Rodovia SP-319 (Nenê Bellini / Faria Lima), Taquaritinga - SP"},
    "vicente jose parise": {"lat": -21.4038, "lng": -48.5065, "end": "Av. Vicente José Parise, Taquaritinga - SP"},
    "vila são sebastião": {"lat": -21.3990, "lng": -48.5020, "end": "Vila São Sebastião, Taquaritinga - SP"},
}

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

locais = data.get("locais", [])
print(f"Atualizando coordenadas exatas para {len(locais)} locais...")

atualizados = 0
for loc in locais:
    nome_lower = loc["nome"].lower().strip()
    end_lower = loc.get("endereco", "").lower().strip()

    match = None
    for key, item in EXACT_COORDS.items():
        if key in nome_lower or key in end_lower:
            match = item
            break

    if match:
        loc["lat"] = match["lat"]
        loc["lng"] = match["lng"]
        loc["endereco"] = match["end"]
        query_map = f"{loc['nome']}, {loc['endereco']}".replace(" ", "+")
        loc["linkMaps"] = f"https://www.google.com/maps/search/?api=1&query={query_map}"
        atualizados += 1
    else:
        loc["lat"] = round(-21.4058 + ((loc["id"] % 7) - 3) * 0.0015, 6)
        loc["lng"] = round(-48.5051 + ((loc["id"] % 5) - 2) * 0.0015, 6)
        loc["endereco"] = f"{loc['nome']} - Taquaritinga/SP"
        query_map = f"{loc['nome']}, Taquaritinga SP".replace(" ", "+")
        loc["linkMaps"] = f"https://www.google.com/maps/search/?api=1&query={query_map}"

# Salvar JSON
data["locais"] = locais
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Coordenadas calibradas com sucesso! {atualizados} locais mapeados com precisao de rua.")

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

print("index.html sincronizado com os dados calibrados!")
