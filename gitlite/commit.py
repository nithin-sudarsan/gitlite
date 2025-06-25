from gitlite.error import throw_error
from gitlite.bin.TreeItem import TreeItem
from gitlite.bin.CommitObject import CommitObject
from gitlite.add import read_index
import pickle
import os
from colorama import Fore
import hashlib
from gitlite.bin.utils import is_gitlite_initialized, get_curr_branch, merge_trees

def build_tree(staged):
    fs_hierarchy = {}
    for path, tree_item in staged.items():
        current_level = fs_hierarchy # current_level acts as a pointer to fs_hierarchy (points to the root directory)
        parts = path.split('/')
        for i, part in enumerate(parts):
            if i == len(parts) - 1: # reached a file
                current_level[part] = tree_item
            else: # reached a directory
                if part not in current_level:
                    current_level[part] = {} # create an empty part
                current_level = current_level[part] # move inside the empty part

    return fs_hierarchy

def commit_staged(message: str):

    committed = False

    object_path  = os.path.join('.gitlite','objects')

    staged:dict[str, TreeItem] = {}
    staged = read_index(staged) # this "staged" has to be used to construct the tree object.

    if not len(staged) > 0:
        return Fore.RED + "Nothing to commit!"
    
    """
    Step 1:
        - Build the tree
        - create its hash
        - create a file inside .gitlite/objects to dump tree
        - dump tree (has to be done as pickle dump)
    """
    tree = build_tree(staged)
    tree_object = pickle.dumps(tree)
    tree_hash = hashlib.sha1(tree_object).hexdigest()

    tree_object_path = os.path.join(object_path, tree_hash)
    os.makedirs(os.path.dirname(tree_object_path), exist_ok=True)
    with open(tree_object_path, 'wb') as f:
        f.write(tree_object)

    """
    Step 2:
        - Get the current branch name and the branch path info
    """
    curr_branch_path = get_curr_branch()

    """
    Step 3:
        - Check if the current branch is poinitng to a parent commit
        - If yes use, the parent commit
        - If not, keep parent commit None
    """
    parent_commit_hash = None
    # check if the file exisits
    if os.path.exists(curr_branch_path):
        try:
            with open(curr_branch_path, 'rb') as f:
                if len(f.peek()) > 0:
                    parent_hash = pickle.loads(f.read().strip())
                    if (os.path.exists(os.path.join(object_path, parent_hash))):
                        parent_commit_hash = parent_hash
        except Exception as e:
            return Fore.YELLOW + f"Warning: Could not read parent commit: {e}"
    """
    Step 4:
        - Create a commit object
        - Create a hash for the commit object
        - dump the commit object as bytes inside /objects/commit_hash file
    """
    commit_object = CommitObject(message, tree_hash, parent_commit_hash)

    commit_object_bytes = pickle.dumps(commit_object)
    commit_hash = hashlib.sha1(commit_object_bytes).hexdigest()

    commit_obj_path = os.path.join(object_path, commit_hash)
    os.makedirs(os.path.dirname(commit_obj_path), exist_ok=True)
    with open(commit_obj_path, 'wb') as f:
        f.write(commit_object_bytes)

    """
    Step 5:
        - Update the branch pointer
        - Basically the current branch we're in should point to the lates commit hash
    """
    with open(curr_branch_path, 'wb') as f:
        f.write(pickle.dumps(commit_hash))
        committed = True
    
    """
    Step 6:
        - Clear staging area
    """
    if committed:
        with open('.gitlite/index','wb') as f:
            f.truncate(0)

    print(Fore.GREEN + f"Committed with hash: {commit_hash[:5]}")
    return None

def commit_amend(message: str):
    # write logic to amend to previous commit
    committed = False

   # get current branch
    curr_branch_path = get_curr_branch()

    # get current commit object
    object_path = '.gitlite/objects'
    commit_hash = None
    commit_object = None
    old_tree = None

    try:
        with open(curr_branch_path, 'rb') as f:
            if len(f.peek()) > 0:
                commit_hash = pickle.loads(f.read().strip())
        with open(os.path.join(object_path, commit_hash), 'rb') as f:
            if len(f.peek()) > 0:
                commit_object: CommitObject = pickle.loads(f.read())
        with open(os.path.join(object_path, commit_object.treehash),'rb') as f:
            if len(f.peek()) > 0:
                old_tree = pickle.loads(f.read())
    except Exception as e:
        print("No previous commits in this branch")


    
    staged:dict[str, TreeItem] = {}
    staged = read_index(staged) # this "staged" has to be used to construct the tree object.
    
    # after getting old tree , add new items from staged to the old tree 
    new_tree = build_tree(staged)
    if old_tree:
        new_tree = merge_trees(old_tree, new_tree)
    else:
        return Fore.RED + "Error reading exisiting commit!"
    
    new_tree_object = pickle.dumps(new_tree)
    new_tree_hash = hashlib.sha1(new_tree_object).hexdigest()

    new_tree_object_path = os.path.join(object_path, new_tree_hash)
    os.makedirs(os.path.dirname(new_tree_object_path), exist_ok=True)
    with open(new_tree_object_path, 'wb') as f:
        f.write(new_tree_object)

    if commit_object.treehash != new_tree_hash:
        # 1. delete old treehash object
        if os.path.exists(os.path.join(object_path, commit_object.treehash)):
            os.remove(os.path.join(object_path, commit_object.treehash))

        new_commit_object: CommitObject = CommitObject(message, new_tree_hash, commit_object.parenthash)
        commit_object_bytes = pickle.dumps(new_commit_object)
        new_commit_hash = hashlib.sha1(commit_object_bytes).hexdigest()

        commit_obj_path = os.path.join(object_path, new_commit_hash)
        os.makedirs(os.path.dirname(commit_obj_path), exist_ok=True)
        with open(commit_obj_path, 'wb') as f:
            f.write(commit_object_bytes)

        # 2. delete old commithash object
        if os.path.exists(os.path.join(object_path, commit_hash)):
            os.remove(os.path.join(object_path, commit_hash))

        # 3. write new commit_object
        with open(curr_branch_path, 'wb') as f:
            f.write(pickle.dumps(new_commit_hash))
            committed = True
        
        if committed:
            with open('.gitlite/index','wb') as f:
                f.truncate(0)
        
        print(Fore.GREEN + f"Amended to previous commit. New commit hash: {new_commit_hash[:5]}")
        return None
    else:
        return Fore.RED + "Error while amending to previous commit"

def commit(cmd:str, message = None, amend = None):
    if not is_gitlite_initialized():
        return Fore.RED + "Repository not initalized! Run `gitlite init` to initialize repository"
    if message and message == "Empty" and amend and amend == "Empty":
        return throw_error(cmd, invalid= True)
    elif not message and amend and amend == "Empty":
        return Fore.RED + "No commit message found. Aborting!"
    elif amend and amend != "Empty":
        return commit_amend(amend)
    elif message and message != "Empty" :
        return commit_staged(message)
    else:
        return throw_error(cmd, invalid= True)
    return None