"""
Interfaz con GitHub API para repositorio privado.
Requiere un Personal Access Token (PAT) de GitHub con permiso 'repo'.

Cómo generar el token:
1. GitHub -> Settings -> Developer settings -> Personal access tokens -> Tokens (classic)
2. Generate new token -> marca el scope 'repo'
3. Copia el token y ponlo en la variable de entorno GITHUB_TOKEN

Uso:
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
python github_interfaz.py
"""

import os
import requests

# ---- Configuración ----
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OWNER = "victorhugoramirezsalgado-boop"
REPO = "Vhrs-"
BASE_URL = "https://api.github.com"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
}


def check_token():
    if not TOKEN:
        raise SystemExit(
            "Falta GITHUB_TOKEN. Configúralo como variable de entorno antes de correr el script."
        )


def get_repo_info():
    """Trae metadatos básicos del repositorio."""
    url = f"{BASE_URL}/repos/{OWNER}/{REPO}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    data = r.json()
    print(f"Repo: {data['full_name']}")
    print(f"Privado: {data['private']}")
    print(f"Descripción: {data.get('description')}")
    print(f"Última actualización: {data['updated_at']}")
    return data


def list_files(path=""):
    """Lista archivos/carpetas en la raíz o en un path dado."""
    url = f"{BASE_URL}/repos/{OWNER}/{REPO}/contents/{path}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    items = r.json()
    for item in items:
        print(f"[{item['type']}] {item['path']}")
    return items


def get_file_content(path):
    """Trae el contenido de un archivo específico (por ejemplo 'main.py')."""
    import base64
    url = f"{BASE_URL}/repos/{OWNER}/{REPO}/contents/{path}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    data = r.json()
    content = base64.b64decode(data["content"]).decode("utf-8")
    return content


def get_issue(issue_number):
    """Trae título, cuerpo y comentarios de un issue."""
    url = f"{BASE_URL}/repos/{OWNER}/{REPO}/issues/{issue_number}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    issue = r.json()
    print(f"\n--- Issue #{issue_number}: {issue['title']} ---")
    print(f"Estado: {issue['state']}")
    print(f"Cuerpo:\n{issue['body']}\n")
    comments_url = issue["comments_url"]
    rc = requests.get(comments_url, headers=HEADERS)
    rc.raise_for_status()
    comments = rc.json()
    for c in comments:
        print(f"[Comentario de {c['user']['login']}]: {c['body']}\n")
    return issue


def get_workflow_runs(workflow_file="publish.yml"):
    """Trae las últimas ejecuciones de un GitHub Actions workflow (útil para depurar fallos)."""
    url = f"{BASE_URL}/repos/{OWNER}/{REPO}/actions/workflows/{workflow_file}/runs"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    runs = r.json().get("workflow_runs", [])
    for run in runs[:5]:
        print(f"Run #{run['run_number']} - {run['status']} - conclusión: {run['conclusion']} - {run['created_at']}")
    return runs


if __name__ == "__main__":
    check_token()
    get_repo_info()
    print("\n--- Archivos en la raíz ---")
    list_files()

    # Ejemplos de uso (descomenta lo que necesites):
    # print(get_file_content("main.py"))
    # get_issue(1)
    # get_workflow_runs("publish.yml")
