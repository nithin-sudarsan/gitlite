import os
from gitlite.add import read_index
from colorama import Fore
from gitlite.bin.TreeItem import TreeItem
import pickle
from gitlite.bin.CommitObject import CommitObject
from gitlite.bin.utils import sha1, get_all_files,get_curr_branch,get_treehashes, get_TreeItems

def get_current_file_dict():
    all_files = get_all_files()
    current_file_dict = {}
    for file in all_files:
        current_file_dict[file] = sha1(file)
    return current_file_dict

def check_status():
    staged:dict[str, TreeItem] = {}
    staged = read_index(staged)
    staged_files = []
    unstaged_files = []
    modified_files = []
    commit_file_dict = {}
    current_file_dict = {}

    current_file_dict = get_current_file_dict()

# =========================================================================================

    # get current branch
    curr_branch_path = get_curr_branch()

    # get current commit object
    object_path = '.gitlite/objects'
    commit_hash = None
    commit_object = None

    try:
        with open(curr_branch_path, 'rb') as f:
            if len(f.peek()) > 0:
                    commit_hash = pickle.loads(f.read().strip())

        with open(os.path.join(object_path, commit_hash), 'rb') as f:
            if len(f.peek()) > 0:
                    commit_object: CommitObject = pickle.loads(f.read())
    except Exception as e:
        print("No previous commits in this branch")
    
    if commit_object:
        treehashes = []
        treehashes = get_treehashes(object_path, commit_object)
        for each in treehashes:
            try:
                with open(os.path.join(object_path, each), 'rb') as f:
                    staged_previous_commit = pickle.loads(f.read())
                    treeItems: list[TreeItem] = list(get_TreeItems(staged_previous_commit))
                    for item in treeItems:
                        if item.filename not in commit_file_dict.keys():
                            commit_file_dict[item.filename] = item.hash
            except Exception as e:
                return e
    
# =========================================================================================

    del_keys = []
    for key, value in current_file_dict.items():
        if key in commit_file_dict.keys(): 
            if commit_file_dict[key] == value:
                del_keys.append(key)
            else:
                modified_files.append(key)
    current_file_dict = {key: value for key, value in current_file_dict.items() if key not in del_keys}

# =========================================================================================

    for key, value in current_file_dict.items():
        if key in staged:
            file_hash = sha1(key)
            if file_hash == value:
                staged_files.append(key)
            else:
                modified_files.append(key)
        else:
            unstaged_files.append(key)
# =========================================================================================
    
    if len(modified_files) > 0:
        print(f"\nModified files:")
        for file in modified_files:
            print(Fore.RED + f"\t{file}")
        print(Fore.RESET)
    if len(unstaged_files) > 0:
        print(f"\nUntracked files:")
        for file in unstaged_files:
            print(Fore.RED + f"\t{file}")
        print(Fore.RESET)
    if len(staged_files) > 0:
        print(f"\nStaged files:")
        for file in staged_files:
            print(Fore.GREEN + f"\t{file}")
        print(Fore.RESET)

def status():
    if os.path.exists('.gitlite/index'):
        check_status()
        return None
    else:
        return Fore.RED + "Repository not initalized! Run `gitlite init` to initialize repository"