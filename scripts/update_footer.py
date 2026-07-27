import os
import re

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
HTML_PATH = os.path.join(SITE_DIR, "index.html")

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html_text = f.read()

# Atualizar o footer para incluir a identificação da Defesa Civil e o link da Área Administrativa
footer_content = """  <footer>
    <p>Coordenadoria Municipal de Defesa Civil • Taquaritinga/SP</p>
    <p>Painel de Transparência Vendaval • Atualizado em <span id="lbl-atualizacao">27/07/2026</span></p>
    <p style="margin-top: 8px;">
      <a href="admin.html" style="color: #94a3b8; text-decoration: underline; font-size: 0.85rem;">
        <i class="fa-solid fa-user-gear"></i> Área Administrativa / Auditoria
      </a>
    </p>
  </footer>"""

html_text = re.sub(r"<footer>.*?</footer>", footer_content, html_text, flags=re.DOTALL)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_text)

print("Footer do index.html atualizado com sucesso!")
