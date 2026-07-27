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
print(f"Total antes da desduplicação: {len(locais)}")

# Identificar todas as ocorrências de Prefeitura / Comitê de Crise
prefeitura_indices = []
for idx, loc in enumerate(locais):
    nome_lower = loc["nome"].lower()
    if "prefeitura" in nome_lower or "comitê de crise" in nome_lower or "comite de crise" in nome_lower:
        prefeitura_indices.append(idx)

print(f"Ocorrências de Prefeitura encontradas: {len(prefeitura_indices)} nos índices {prefeitura_indices}")

# Manter apenas a PRIMEIRA ocorrência da Prefeitura e remover as duplicadas
if len(prefeitura_indices) > 1:
    # Atualizar o primeiro registro com todos os dados completos
    first_idx = prefeitura_indices[0]
    locais[first_idx]["nome"] = "Prédio da Prefeitura Municipal / Comitê de Crise"
    locais[first_idx]["endereco"] = "Rua Romeu Mársico, 200 - Centro, Taquaritinga - SP, CEP 15900-000"
    locais[first_idx]["bairro"] = "Centro"
    locais[first_idx]["lat"] = -21.411747
    locais[first_idx]["lng"] = -48.498400
    locais[first_idx]["status"] = "concluido"
    locais[first_idx]["linkMaps"] = "https://maps.app.goo.gl/z2FN85uoQDLSHSmW8"
    locais[first_idx]["linkFotos"] = "https://photos.app.goo.gl/nx1uPz13BJmPBHEi6"
    locais[first_idx]["fotos"] = "https://photos.app.goo.gl/nx1uPz13BJmPBHEi6"
    
    # Remover os índices duplicados do final para o começo
    for idx_to_remove in sorted(prefeitura_indices[1:], reverse=True):
        removed = locais.pop(idx_to_remove)
        print(f"Removida duplicata de Prefeitura com ID #{removed['id']}")

# Reindexar os IDs para ficarem sequenciais (1, 2, 3, ...)
for new_id, loc in enumerate(locais, start=1):
    loc["id"] = new_id

# Recalcular estatísticas
total_locais = len(locais)
total_concluidos = sum(1 for l in locais if l["status"] == "concluido" or (l.get("linkFotos") or l.get("fotos")))
total_pendentes = total_locais - total_concluidos

data["total_locais"] = total_locais
data["total_concluidos"] = total_concluidos
data["total_pendentes"] = total_pendentes
data["locais"] = locais

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Atualizar index.html com dados sincronizados sem duplicatas
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

print("\n=== DESDUPLICAÇÃO CONCLUÍDA DA PREFEITURA ===")
print(f"Total de locais finais: {total_locais}")
print(f"Concluídos: {total_concluidos}")
print(f"Pendentes: {total_pendentes}")
print("locais.json e index.html salvos sem duplicatas!")
