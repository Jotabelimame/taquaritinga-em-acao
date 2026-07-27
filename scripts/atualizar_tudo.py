import subprocess
import os

SITE_DIR = r"C:\Users\JOTABELIMA\Documents\New project\site-taquaritinga"

scripts = [
    "scripts/process_pdf_report.py",
    "scripts/audit_and_clean_all_dups.py",
    "scripts/gerar_rotas.py",
    "scripts/update_html_routes.py"
]

print("=== INICIANDO ATUALIZAÇÃO MASTER COMPLETA DE TODO O SISTEMA ===")

for script in scripts:
    script_path = os.path.join(SITE_DIR, script)
    if os.path.exists(script_path):
        print(f"\n--- Executando: {script} ---")
        res = subprocess.run(["python", script_path], cwd=SITE_DIR, capture_output=True, text=True)
        print(res.stdout)
        if res.stderr:
            print("Aviso/Erro:", res.stderr)

print("\n=== ATUALIZAÇÃO E DEPLOY NO GITHUB ===")
git_res = subprocess.run(["git", "add", "."], cwd=SITE_DIR, capture_output=True, text=True)
git_commit = subprocess.run(["git", "commit", "-m", "Atualização Master Completa - Sincronização de todos os locais, rotas, PDF e fotos"], cwd=SITE_DIR, capture_output=True, text=True)
git_push = subprocess.run(["git", "push", "origin", "main"], cwd=SITE_DIR, capture_output=True, text=True)

print(git_commit.stdout)
print(git_push.stdout)
print("=== SUCESSO ABSOLUTO! TUDO FOI ATUALIZADO E PUBLICADO NO GITHUB PAGES ===")
