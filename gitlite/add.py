import os
import sys
import pickle
from gitlite.error import throw_error
from gitlite.bin.TreeItem import TreeItem
from gitlite.bin.FileType import FileType
from colorama import Fore
from gitlite.bin.utils import check_stage,sha1,get_all_files,is_gitlite_initialized

def read_index(staged) -> dict[str, TreeItem]:
    try:
        with open(".gitlite/index", 'rb') as f:
            if len(f.peek()) > 0:
                staged = pickle.load(f)
        return staged
    except:
        return Fore.RED + "Repository not intialized. Run `gitlite init` to initialize repository."

def stage_files(paths, staged, added_files, skipped_files):
    for path in paths:
        if os.path.isfile(path):
            file = path
            try:
                file_hash = sha1(file)
            except Exception as e:
                print(Fore.RED + f"Error processing {file}: {e}")
                sys.exit(1)
            object_path = os.path.join('.gitlite/objects', file_hash)
            if os.path.exists(object_path):
                print(f"No latest changes in {file}")
                continue
            file_skipped, can_stage = check_stage(file, file_hash, staged)
            if file_skipped:
                skipped_files.append(file_skipped)
            if can_stage:
                staged[file] = TreeItem(filename = file, hash = file_hash, filetype = FileType.BLOB)
                added_files.append(file)
        elif os.path.isdir(path):
            dir_files = get_all_files(path)
            stage_files(dir_files, staged,added_files, skipped_files)
    return staged, added_files, skipped_files
        
def write_to_index(staged):
    try:
        with open(".gitlite/index", "wb") as f:
            pickle.dump(staged, f)
            print(Fore.GREEN + """Staging complete!
""")
    except Exception as e:
        print(Fore.RED + f"Error writing files to index: {e}")
        sys.exit(1)

def add_path(paths: list[str]):
    # write logic to add files for staging
    staged:dict[str, TreeItem] = {}

    # read index file
    staged = read_index(staged)

    if (type(staged)!= str):
    
        # stage each file in args
        added_files = []
        skipped_files = []
        staged, added_files, skipped_files = stage_files(paths, staged, added_files, skipped_files)
        if len(skipped_files) > 0:
            print("Skipped (no new changes or already staged): ")
            for file in skipped_files:
                print(f"\t{file}")
            print(Fore.RESET)
        if len(added_files) > 0:
            print("Added: ")
            for file in added_files:
                print(Fore.GREEN + f"\t{file}")
            print(Fore.RESET)
            
        # write to index file
        write_to_index(staged)
    else:
        return staged

def add(cmd:str, paths = None):
    if not is_gitlite_initialized():
        return Fore.RED + "Repository not initalized! Run `gitlite init` to initialize repository"
    if paths and len(paths):
        err = add_path(paths)
    else:
        return throw_error(cmd, invalid= True)
    return err