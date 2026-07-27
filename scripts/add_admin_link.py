import os
import re

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
HTML_PATH = os.path.join(SITE_DIR, "index.html")

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html_text = f.read()

# Adicionar o link do painel admin no footer do index.html
admin_footer_link = '<p style="margin-top: 10px;"><a href="admin.html" style="color: #64748b; text-decoration: underline; font-size: 0.8rem;"><i class="fa-solid fa-user-gear"></i> Painel de Administração & Auditoria GPS</a></p>'

if "admin.html" not in html_text:
    html_text = html_text.replace("</footer>", f"{admin_footer_link}\n  </footer>")

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_text)

print("Link do Painel Admin adicionado ao footer do index.html!")
