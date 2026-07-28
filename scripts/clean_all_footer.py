import os

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
HTML_PATH = os.path.join(SITE_DIR, "index.html")

with open(HTML_PATH, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if '<!-- How to Support Section -->' in line or 'fa-hand-holding-heart' in line:
        skip = True
        continue
    if skip and '<!-- Footer -->' in line:
        skip = False
    if not skip:
        new_lines.append(line)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("SUCCESS: Secao de apoio, PIX e telefones uteis completamente removidos do index.html!")
