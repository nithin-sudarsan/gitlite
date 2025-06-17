import hashlib
from bin.TreeItem import TreeItem
import os
import sys
from colorama import Fore, Style

def sha1(file_name) -> str:
    try:
        file_hash = calculate_sha1(file_name)
        return file_hash
    except Exception as e:
        print(f"Unable to read {file_name}: {e}")
        sys.exit(1)

def calculate_sha1(file_path):
    sha1_hash = hashlib.sha1()
    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(4096)
            if not chunk:
                break
            sha1_hash.update(chunk)
    return sha1_hash.hexdigest()


def check_stage(file: str, file_hash: str, staged: dict[str, TreeItem]):
    if os.path.exists(os.path.join(".gitlite/objects", file_hash)):
        print(f"No latest changes to stage in {file}")
        return file, False

    if staged and file in staged and staged[file].hash == file_hash:
        return file, False
    
    return None, True

def parse_gitignore():
    try:
        with open('.gitignore') as f:
            patterns = f.readlines()
            return patterns
    except:
        return None
    
def get_all_files(root = None):
    if root!= None:
        root_dir = root
    else:
        root_dir = '.'
    relative_dir_path = []
    for dirpath, _, filenames in os.walk(root_dir, topdown = True):
        for filename in filenames:
            if filename.startswith('.'):
                continue
            required_paths = os.path.relpath(os.path.join(dirpath, filename), root_dir)
            if not required_paths.startswith('.'):
                relative_dir_path.append(required_paths)
    gitignore_patterns = parse_gitignore()
    for pattern in gitignore_patterns:
        relative_dir_path = [path for path in relative_dir_path if pattern not in path]
    return relative_dir_path
