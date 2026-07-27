import os
import json

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
JSON_PATH = os.path.join(SITE_DIR, "dados", "locais.json")
HTML_PATH = os.path.join(SITE_DIR, "index.html")

with open(JSON_PATH, "r", encoding="utf-8") as f:
    json_data = json.load(f)

json_str = json.dumps(json_data, ensure_ascii=False, indent=2)

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html_content = f.read()

# Substituir a função loadData por dados embutidos + fetch fallback
replacement = f"""const initialData = {json_str};
    let rawLocaisData = initialData.locais || [];
    let activeFilter = 'todos';
    let map = null;
    let markersLayer = null;

    async function loadData() {{
      try {{
        const response = await fetch('dados/locais.json');
        if (response.ok) {{
          const data = await response.json();
          rawLocaisData = data.locais || rawLocaisData;
          updateStats(data);
        }} else {{
          updateStats(initialData);
        }}
      }} catch (err) {{
        updateStats(initialData);
      }}
      renderGrid();
      initMap();
    }}"""

html_content = html_content.replace(
    "let rawLocaisData = [];\n    let activeFilter = 'todos';\n    let map = null;\n    let markersLayer = null;\n\n    // Carregar JSON de dados de forma assíncrona ou fallback\n    async function loadData() {\n      try {\n        const response = await fetch('dados/locais.json');\n        if (!response.ok) throw new Error('Network response was not ok');\n        const data = await response.json();\n        rawLocaisData = data.locais || [];\n        updateStats(data);\n        renderGrid();\n        initMap();\n      } catch (err) {\n        console.warn('Carregamento via fetch falhou, tentando carregar dados diretamente.', err);\n        // Tentar buscar se houver var local ou fallback\n        renderGrid();\n        initMap();\n      }\n    }",
    replacement
)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Dados do JSON incorporados com sucesso em index.html!")
