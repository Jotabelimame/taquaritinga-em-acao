import os
import re

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"
HTML_PATH = os.path.join(SITE_DIR, "index.html")
ADMIN_PATH = os.path.join(SITE_DIR, "admin.html")

# 1. Atualizar index.html
with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Substituir título e cabeçalho
html = html.replace("<title>Transparência Vendaval 2026 - Taquaritinga/SP</title>", "<title>Taquaritinga em Ação - Monitoramento Vendaval 2026</title>")
html = html.replace("Portal de transparência e monitoramento", "Portal de monitoramento")
html = html.replace("<h1>Portal de Transparência - Vendaval</h1>", "<h1>Taquaritinga em Ação - Vendaval 2026</h1>")
html = html.replace("Painel de Transparência Vendaval", "Taquaritinga em Ação")

# Remover a seção inteira "Como Apoiar as Famílias Atingidas" (PIX, Telefones úteis, etc)
support_pattern = r'<!-- How to Support Section -->\s*<h2 class="section-title">.*?</h2>\s*<div class="support-card">.*?</div>'
html = re.sub(support_pattern, '', html, flags=re.DOTALL)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("SUCCESS: index.html atualizado! Texto de transparencia, chave PIX e telefones uteis removidos!")

# 2. Atualizar admin.html
with open(ADMIN_PATH, "r", encoding="utf-8") as f:
    admin_html = f.read()

admin_html = admin_html.replace("<title>Painel de Administração • Auditoria GPS & Fotos</title>", "<title>Taquaritinga em Ação • Painel de Administração</title>")

with open(ADMIN_PATH, "w", encoding="utf-8") as f:
    f.write(admin_html)

print("SUCCESS: admin.html atualizado!")
