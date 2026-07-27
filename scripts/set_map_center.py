import os
import re

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
HTML_PATH = os.path.join(SITE_DIR, "index.html")

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html_text = f.read()

# Atualizar o ponto central do mapa no Leaflet para -21.423708, -48.510894
new_html = re.sub(
    r"L\.map\('map'\)\.setView\(\[-?\d+\.\d+,\s*-?\d+\.\d+\],\s*\d+\)",
    "L.map('map').setView([-21.423708, -48.510894], 14)",
    html_text
)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(new_html)

print("Ponto central do mapa atualizado no index.html!")
