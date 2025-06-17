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


def can_stage(file: str, file_hash: str, staged: dict[str, TreeItem]):
    if os.path.exists(os.path.join(".gitlite/objects", file_hash)):
        print(f"No latest changes to stage in {file}")
        return False

    if staged and file in staged and staged[file].hash == file_hash:
        print(f"""
Skipped {Fore.RED} {file} {Style.RESET_ALL}(no new changes or already staged)
              """)
        return False
    
    return True
        