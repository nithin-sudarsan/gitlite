import hashlib
from gitlite.bin.TreeItem import TreeItem
import os
import sys
from colorama import Fore
import pickle
from gitlite.bin.CommitObject import CommitObject
import copy

def welcomeMessage():
    print("Welcome to GitLite!")
    print("Available commands:")
    print("\tinit: Initializes an empty gitlite repository")
    print("\tstatus: Check staging status of files in working tree.")
    print("\tadd: Adds files to staging")
    print("\tcommit: Commit staged files")
    print("\tbranch: Creates a new branch")
    print("\tcheckout: Checkout to branch")
    print("\tclone: Clones a remote repository")
    print("\thelp: Display this help message")

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

def is_gitlite_initialized():
    if not os.path.exists('.gitlite'):
        return False
    elif os.path.exists('.gitlite/objects') and os.path.exists('.gitlite/refs') and os.path.exists('.gitlite/index') and os.path.exists('.gitlite/refs/HEAD'):
        return True
    else:
        return False
    
def get_curr_branch():
    try:
        with open(".gitlite/refs/HEAD", "r") as f:
            head_content = f.readline()
            curr_branch_path = head_content.split(":")[1].strip()
            curr_branch = curr_branch_path.split("/")[-1]
            curr_branch_path = os.path.join('.gitlite', curr_branch_path)
        return curr_branch_path
    except Exception as e:
        print(Fore.RED + f"Error reading HEAD file: {e}")
        sys.exit(1)

def get_treehashes(object_path, commit_object: CommitObject) -> list:
    treehashes = []
    treehashes.append(commit_object.treehash)
    current_commit = commit_object
    while current_commit.parenthash:
        try:
            # open parent commit_object
            with open(os.path.join(object_path, commit_object.parenthash), 'rb') as f:
                if len(f.peek()) > 0:
                    parent_commit_object: CommitObject = pickle.loads(f.read())
                    treehashes.append(parent_commit_object.treehash)
                    current_commit = parent_commit_object
                else:
                    print(f"Warning: Parent commit object not found or empty at {os.path.join(object_path, commit_object.parenthash)}")
                    break
            
        except Exception as e:
            return e
    return treehashes

def get_TreeItems(staged: dict):
    for _, value in staged.items():
        if isinstance(value, dict):
            yield from get_TreeItems(value)
        else:
            yield value

def merge_trees(old_tree: dict, new_tree: dict) -> dict:
    merged_tree = copy.deepcopy(old_tree)

    for key, new_value in new_tree.items():
        if key in merged_tree:
            old_value = merged_tree[key]

            if isinstance(old_value, dict) and isinstance(new_value, dict):
                merged_tree[key] = merge_trees(old_value, new_value)
            else:
                merged_tree[key] = new_value
        else:
            merged_tree[key] = new_value
            
    return merged_tree

def get_commit_history(branch_name = None):
    commit_objects = {}
    object_path = '.gitlite/objects'
    if branch_name:
        branch_path = f".gitlite/refs/heads/{branch_name}"
    else:
        branch_path = get_curr_branch()
    latest_commit_object: CommitObject = None
    latest_commit_hash = None

    try:
        with open(branch_path, 'rb') as f:
            if len(f.peek()) > 0:
                latest_commit_hash = pickle.load(f)
        if latest_commit_hash:
            with open(os.path.join(object_path, latest_commit_hash), 'rb') as f:
                if len(f.peek()) > 0:
                    latest_commit_object = pickle.load(f)
    except:
        return Fore.RED + f"Error in branch: {branch_path.split('/')[-1]}"
    
    if latest_commit_object:
        commit_objects[latest_commit_hash] = latest_commit_object
    else:
        return Fore.RED + "Error: No commits found!"

    while latest_commit_object.parenthash:
        try:
            # open parent commit_object
            with open(os.path.join(object_path, latest_commit_object.parenthash), 'rb') as f:
                if len(f.peek()) > 0:
                    parent_commit_object: CommitObject = pickle.loads(f.read())
                    commit_objects[latest_commit_object.parenthash] = parent_commit_object
                    # commit_objects.append(parent_commit_object)
                    latest_commit_object = parent_commit_object
                else:
                    print(f"Warning: Parent commit object not found or empty at {os.path.join(object_path, latest_commit_object.parenthash)}")
                    break
            
        except Exception as e:
            return e
    return commit_objects