import os
import json
import re

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
JSON_PATH = os.path.join(SITE_DIR, "dados", "locais.json")
HTML_PATH = os.path.join(SITE_DIR, "index.html")

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

rotas = data.get("rotas", [])
r1 = rotas[0]
r2 = rotas[1]
r3 = rotas[2]

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html_text = f.read()

# Atualizar os links e detalhes das rotas no HTML
routes_html_replacement = f"""<div class="routes-grid">
      <div class="route-card">
        <div class="route-icon">
          <i class="fa-solid fa-compass"></i>
        </div>
        <h3>{r1['nome']}</h3>
        <p>Rota otimizada cobrindo <strong>{r1['total_locais']} locais</strong> na região Central e Vila Esperança.</p>
        <ul class="route-list">
          <li><i class="fa-solid fa-circle"></i> Berçário Anunciata Colombo</li>
          <li><i class="fa-solid fa-circle"></i> EMEB Dr. Estevam Schlobach Salvagni</li>
          <li><i class="fa-solid fa-circle"></i> Av. Vicente José Parise / Av. Paulo Roberto Scandar</li>
          <li><i class="fa-solid fa-circle"></i> EMEB Mathilde Menon & ETAM</li>
          <li><i class="fa-solid fa-circle"></i> + {r1['total_locais'] - 4} outros locais no setor</li>
        </ul>
        <a href="{r1['link_gmaps']}" target="_blank" class="btn btn-maps" style="width: 100%;">
          <i class="fa-solid fa-location-arrow"></i> Abrir Rota Setor 1 ({r1['total_locais']} Locais)
        </a>
      </div>

      <div class="route-card">
        <div class="route-icon" style="background: rgba(16, 185, 129, 0.2); color: var(--secondary);">
          <i class="fa-solid fa-truck-ramp-box"></i>
        </div>
        <h3>{r2['nome']}</h3>
        <p>Rota otimizada cobrindo <strong>{r2['total_locais']} locais</strong> na Zona Norte e Laranjeiras.</p>
        <ul class="route-list">
          <li><i class="fa-solid fa-circle"></i> Conjunto Habitacional Dr. Adail Nunes da Silva</li>
          <li><i class="fa-solid fa-circle"></i> Av. Mário da Silva Camargo</li>
          <li><i class="fa-solid fa-circle"></i> Av. Heitor Alves Gomes (Vale do Sol)</li>
          <li><i class="fa-solid fa-circle"></i> Clube do Funcionário Público</li>
          <li><i class="fa-solid fa-circle"></i> + {r2['total_locais'] - 4} outros locais no setor</li>
        </ul>
        <a href="{r2['link_gmaps']}" target="_blank" class="btn btn-maps" style="width: 100%;">
          <i class="fa-solid fa-location-arrow"></i> Abrir Rota Setor 2 ({r2['total_locais']} Locais)
        </a>
      </div>

      <div class="route-card">
        <div class="route-icon" style="background: rgba(245, 158, 11, 0.2); color: var(--accent);">
          <i class="fa-solid fa-industry"></i>
        </div>
        <h3>{r3['nome']}</h3>
        <p>Rota otimizada cobrindo <strong>{r3['total_locais']} locais</strong> no Setor Industrial e Guariroba.</p>
        <ul class="route-list">
          <li><i class="fa-solid fa-circle"></i> Recapex Marangoni (Setor Industrial)</li>
          <li><i class="fa-solid fa-circle"></i> Distrito de Guariroba (Residências & Escolas)</li>
          <li><i class="fa-solid fa-circle"></i> Escola Municipal Modesto Bohrer</li>
          <li><i class="fa-solid fa-circle"></i> Posto de Saúde Paraíso</li>
          <li><i class="fa-solid fa-circle"></i> + {r3['total_locais'] - 4} outros locais no setor</li>
        </ul>
        <a href="{r3['link_gmaps']}" target="_blank" class="btn btn-maps" style="width: 100%;">
          <i class="fa-solid fa-location-arrow"></i> Abrir Rota Setor 3 ({r3['total_locais']} Locais)
        </a>
      </div>
    </div>"""

# Substituir o conteúdo antigo de routes-grid
html_text = re.sub(r'<div class="routes-grid">.*?</div>\s*</div>', routes_html_replacement, html_text, flags=re.DOTALL)

# Re-injetar initialData com a versão completa do JSON
json_full_str = json.dumps(data, ensure_ascii=False, indent=2)
html_text = re.sub(
    r"const initialData = \{.*?\};\n    let rawLocaisData =",
    f"const initialData = {json_full_str};\n    let rawLocaisData =",
    html_text,
    flags=re.DOTALL
)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_text)

print("index.html atualizado com sucesso com as novas rotas!")
