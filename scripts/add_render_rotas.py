import os
import json
import re

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
HTML_PATH = os.path.join(SITE_DIR, "index.html")
JSON_PATH = os.path.join(SITE_DIR, "dados", "locais.json")

with open(JSON_PATH, "r", encoding="utf-8") as f:
    json_data = json.load(f)

json_str = json.dumps(json_data, ensure_ascii=False, indent=2)

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html_content = f.read()

# 1. Garantir id="routesGrid" na div das rotas
html_content = re.sub(
    r'<div class="routes-grid">.*?</div>\s*</div>',
    '<div class="routes-grid" id="routesGrid">\n      <!-- Rotas renderizadas dinamicamente pelo JS -->\n    </div>',
    html_content,
    flags=re.DOTALL
)

# 2. Adicionar função renderRotas e chamar no loadData
js_render_rotas = """
    function renderRotas() {
      const grid = document.getElementById('routesGrid');
      if (!grid) return;
      const rotasData = (initialData && initialData.rotas) ? initialData.rotas : [];

      if (rotasData.length === 0) {
        grid.innerHTML = '<p style="color: var(--text-muted); text-align: center; grid-column: 1/-1;">Nenhuma rota cadastrada.</p>';
        return;
      }

      const icons = ['fa-compass', 'fa-truck-ramp-box', 'fa-industry'];
      const colors = ['var(--primary)', 'var(--secondary)', 'var(--accent)'];
      const bgColors = ['rgba(2, 132, 199, 0.2)', 'rgba(16, 185, 129, 0.2)', 'rgba(245, 158, 11, 0.2)'];

      grid.innerHTML = rotasData.map((rota, idx) => `
        <div class="route-card">
          <div class="route-icon" style="background: ${bgColors[idx % 3]}; color: ${colors[idx % 3]};">
            <i class="fa-solid ${icons[idx % 3]}"></i>
          </div>
          <h3>${escapeHtml(rota.nome)}</h3>
          <p>${escapeHtml(rota.descricao)}</p>
          <ul class="route-list">
            ${(rota.locais || []).slice(0, 4).map(l => `<li><i class="fa-solid fa-circle"></i> ${escapeHtml(l)}</li>`).join('')}
            ${(rota.locais || []).length > 4 ? `<li><i class="fa-solid fa-circle"></i> + ${rota.locais.length - 4} outros locais no setor</li>` : ''}
          </ul>
          <a href="${rota.link_gmaps}" target="_blank" class="btn btn-maps" style="width: 100%;">
            <i class="fa-solid fa-location-arrow"></i> Abrir Rota (${rota.total_locais} Locais)
          </a>
        </div>
      `).join('');
    }
"""

# Injetar renderRotas antes da chamada renderGrid() ou no script
if "function renderRotas()" not in html_content:
    html_content = html_content.replace("function renderGrid() {", js_render_rotas + "\n    function renderGrid() {")

# Garantir que renderRotas() é chamada dentro de loadData()
if "renderRotas();" not in html_content:
    html_content = html_content.replace("renderGrid();\n      initMap();", "renderGrid();\n      renderRotas();\n      initMap();")

# Atualizar const initialData
html_content = re.sub(
    r"const initialData = \{.*?\};\n    let rawLocaisData =",
    f"const initialData = {json_str};\n    let rawLocaisData =",
    html_content,
    flags=re.DOTALL
)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)

print("index.html atualizado com a função renderRotas e renderização dinâmica das rotas!")
