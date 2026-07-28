import os

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
HTML_PATH = os.path.join(SITE_DIR, "index.html")

with open(HTML_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# Remover tudo entre rotas e footer
import re
text = re.sub(r'</div>\s*<div class="support-item">.*?<footer>', '</div>\n\n  </main>\n\n  <!-- Footer -->\n    <footer>', text, flags=re.DOTALL)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(text)

print("SUCCESS: Suporte, WhatsApp e telefones uteis removidos do index.html!")
