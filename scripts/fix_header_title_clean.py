import os
import re

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
HTML_PATH = os.path.join(SITE_DIR, "index.html")

with open(HTML_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# Substituir qualquer ocorrência de Portal de Transparência
text = re.sub(r'<h1>.*?Portal de Transparência.*?</h1>', '<h1>Taquaritinga em Ação</h1>', text, flags=re.IGNORECASE)
text = re.sub(r'Portal de Transparência - Vendaval', 'Taquaritinga em Ação', text, flags=re.IGNORECASE)
text = re.sub(r'Portal de Transparência', 'Taquaritinga em Ação', text, flags=re.IGNORECASE)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(text)

print("SUCCESS: Título H1 do cabeçalho alterado para 'Taquaritinga em Ação'!")
