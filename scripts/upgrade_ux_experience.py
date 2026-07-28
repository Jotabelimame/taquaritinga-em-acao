import os
import re

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
HTML_PATH = os.path.join(SITE_DIR, "index.html")

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Adicionar estilo de pills de categorias e animações suave de FlyTo
css_upgrade = """
    /* UX Category Pills & Smooth Animations */
    .category-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 15px;
      margin-bottom: 20px;
    }
    .pill-btn {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      padding: 8px 16px;
      border-radius: 9999px;
      font-size: 0.88rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease-in-out;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .pill-btn:hover {
      border-color: var(--primary);
      color: var(--text-main);
      transform: translateY(-1px);
    }
    .pill-btn.active {
      background: var(--primary);
      color: #ffffff;
      border-color: var(--primary);
      box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3);
    }
    .local-card {
      cursor: pointer;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .local-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }
"""

if "</style>" in html:
    html = html.replace("</style>", f"{css_upgrade}\n  </style>")

# 2. Adicionar Pills de Categorias no HTML de controles
pills_html = """
      <!-- Filter Category Pills for Ultra UX -->
      <div class="category-pills" id="categoryPills">
        <button class="pill-btn active" onclick="filtrarCategoria('todas', this)"><i class="fa-solid fa-layer-group"></i> Todas</button>
        <button class="pill-btn" onclick="filtrarCategoria('escola', this)"><i class="fa-solid fa-graduation-cap"></i> Escolas & EMEBs</button>
        <button class="pill-btn" onclick="filtrarCategoria('avenida', this)"><i class="fa-solid fa-road"></i> Avenidas & Ruas</button>
        <button class="pill-btn" onclick="filtrarCategoria('praça', this)"><i class="fa-solid fa-tree"></i> Praças & Parques</button>
        <button class="pill-btn" onclick="filtrarCategoria('bairro', this)"><i class="fa-solid fa-city"></i> Bairros & Distritos</button>
      </div>
"""

if '<div class="filter-buttons">' in html:
    html = html.replace('<div class="filter-buttons">', f'{pills_html}\n      <div class="filter-buttons">')

# 3. Adicionar função FlyTo ao clicar no card para melhor navegabilidade
flyto_js = """
    function focarNoMapa(lat, lng, nome) {
      if (map && lat && lng) {
        map.flyTo([lat, lng], 17, { duration: 1.2 });
        // Encontrar marcador correspondente e abrir popup
        markersLayer.eachLayer(layer => {
          if (layer.getLatLng().lat === lat && layer.getLatLng().lng === lng) {
            layer.openPopup();
          }
        });
        document.getElementById('map').scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }

    let categoriaAtual = 'todas';
    function filtrarCategoria(cat, el) {
      categoriaAtual = cat;
      document.querySelectorAll('.pill-btn').forEach(b => b.classList.remove('active'));
      el.classList.add('active');
      aplicarFiltrosCombinados();
    }

    function aplicarFiltrosCombinados() {
      const termo = document.getElementById('searchInput').value.toLowerCase().trim();
      const filtroStatus = document.querySelector('.filter-btn.active')?.dataset.filter || 'todos';

      const filtrados = rawLocaisData.filter(item => {
        if (!item.exibirNoSite && item.exibirNoSite !== undefined) return false;
        
        // Filtro Status
        const linkFotos = item.linkFotos || item.fotos || '';
        const isConcluido = (item.status === 'concluido') || (linkFotos.trim() !== '');
        if (filtroStatus === 'concluido' && !isConcluido) return false;
        if (filtroStatus === 'pendente' && isConcluido) return false;

        # Filtro Categoria
        const nomeLow = item.nome.toLowerCase();
        if (categoriaAtual === 'escola' && !nomeLow.includes('emeb') && !nomeLow.includes('escola') && !nomeLow.includes('berçário')) return false;
        if (categoriaAtual === 'avenida' && !nomeLow.includes('av') && !nomeLow.includes('rua') && !nomeLow.includes('r.')) return false;
        if (categoriaAtual === 'praça' && !nomeLow.includes('praça') && !nomeLow.includes('praca') && !nomeLow.includes('parque')) return false;
        if (categoriaAtual === 'bairro' && !nomeLow.includes('bairro') && !nomeLow.includes('distrito') && !nomeLow.includes('conj')) return false;

        # Filtro Busca Termo
        if (termo) {
          const endLow = (item.endereco || '').toLowerCase();
          const bairroLow = (item.bairro || '').toLowerCase();
          return nomeLow.includes(termo) || endLow.includes(termo) || bairroLow.includes(termo);
        }
        return true;
      });

      renderizarGrid(filtrados);
      renderizarMapa(filtrados);
    }
"""

if "function renderizarGrid(" in html:
    html = html.replace("function renderizarGrid(", f"{flyto_js}\n\n    function renderizarGrid(")

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("SUCCESS: index.html atualizado com melhorias de UX e navegabilidade em 1 clique!")
