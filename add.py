import os
import sys
import pickle
from error import throw_error
from bin.TreeItem import TreeItem
from bin.FileType import FileType
from colorama import Fore,Style
from bin.utils import can_stage, sha1

def read_index(staged) -> dict[str, TreeItem]:
    try:
        with open(".gitlite/index", 'rb') as f:
            if len(f.peek()) > 0:
                staged = pickle.load(f)
        return staged
    except Exception as e:
        return Fore.RED + "Repository not intialized. Run `gitlite init` to initialize repository."

def stage_files(files, staged):
    for file in files:
        try:
            file_hash = sha1(file)
        except Exception as e:
            print(Fore.RED + f"Error processing {file}: {e}")
            sys.exit(1)
        object_path = os.path.join('.gitlite/objects', file_hash)
        if os.path.exists(object_path):
            print(f"No latest changes in {file}")
            continue
        
        if can_stage(file, file_hash, staged):
            staged[file] = TreeItem(filename = file, hash = file_hash, filetype = FileType.BLOB)
            print("Added" + Fore.GREEN + f" {file}")
            print(Style.RESET_ALL)
        
def write_to_index(staged):
    try:
        with open(".gitlite/index", "wb") as f:
            pickle.dump(staged, f)
            print(Fore.GREEN + """Staging complete!
""")
    except Exception as e:
        print(Fore.RED + f"Error writing files to index: {e}")
        sys.exit(1)

def add_path(files: list[str]):
    # write logic to add files for staging
    staged:dict[str, TreeItem] = {}

    # read index file
    staged = read_index(staged)

    if (type(staged)!= str):
    
        # stage each file in args
        stage_files(files, staged)
            
        # write to index file
        write_to_index(staged)
    else:
        return staged

def add(cmd:str, paths = None):
    if paths and len(paths):
        err = add_path(paths)
    else:
        return throw_error(cmd, invalid= True)
    return err