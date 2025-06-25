from gitlite.error import throw_error
from colorama import Fore
from gitlite.bin.utils import is_gitlite_initialized, get_curr_branch
import os
import shutil

heads_path = '.gitlite/refs/heads'

def show_all_branches():
    # write logic to show all branches
    curr_branch = get_curr_branch().split('/')[-1]
    all_branches = os.listdir(heads_path)
    if len(all_branches) == 0:
        return "Error reading branches"
    else:
        for branch in all_branches:
            if branch == curr_branch:
                print(Fore.GREEN + f"-> {branch}" + Fore.RESET)
            else:
                print(f"   {branch}")
        return None

def create_branch(branch_name):
    curr_branch_path = get_curr_branch()
    curr_branch_name = curr_branch_path.split('/')[-1]
    new_branch_path = os.path.join(heads_path, branch_name)

    try:
        with open(new_branch_path, "w") as f:
            pass
    except FileExistsError:
        return Fore.RED + f"A branch named '{branch_name}' already exists."
    try:
        shutil.copyfile(curr_branch_path, new_branch_path)
        print(f"New branch created: {branch_name}")
        return None
    except FileNotFoundError:
        return Fore.RED + f"Error: Branch '{curr_branch_name}' not found!"
    except Exception as e:
        return f"An error occurred: {e}"
    
    # here we created a new branch from the curr_branch but we did not checkout to it
    # hence curr_branch still points to the old branch, not the new branch


def rename_branch(new_name):
    # Write logic to rename current branch
    if len(new_name) == 2: # [old branch, new_branch]
        old_branch_path = os.path.join(heads_path, new_name[0])
    else:
        old_branch_path = get_curr_branch()
    new_branch_path = os.path.join(heads_path, new_name[-1])

    try:
        os.rename(old_branch_path, new_branch_path)
        print(f"Branch '{old_branch_path.split('/')[-1]}' renamed to '{new_name[-1]}' successfully.")
        # change ref in HEAD
        if old_branch_path == get_curr_branch():
            with open('.gitlite/refs/HEAD', "w") as f:
                f.write(f"ref: refs/heads/{new_name[-1]}\n")
        return None
    except OSError as e:
        return Fore.RED + f"Branch '{old_branch_path.split('/')[-1]}' does not exist!"


def delete_branch(branch_name):
    # Write logic to delete branch
    # throw error if trying to delete current branch
    delete_branch_path = os.path.join(heads_path, branch_name)
    curr_branch_path = get_curr_branch()

    if delete_branch_path == curr_branch_path:
        return Fore.RED + f"Cannot delete current branch!"
    else:
        try:
            os.remove(delete_branch_path)
            print(f"Deleted branch: {branch_name}")
            return None
        except FileNotFoundError as e:
            return Fore.RED + f"Error: Branch you're trying to delete does not exist!"

def branch(cmd: str, new_branch = None, rename = None, delete = None):
    if not is_gitlite_initialized():
        return Fore.RED + "Repository not initalized! Run `gitlite init` to initialize repository"
    if new_branch=="Empty" and rename=="Empty" and delete=="Empty": 
        show_all_branches()
    else:
        if rename and rename!="Empty" and len(rename) < 3:
            return rename_branch(rename)
        elif delete and delete!="Empty":
            return delete_branch(delete)
        elif new_branch and new_branch!="Empty":
            create_branch(new_branch)
        else:
            return throw_error(cmd, True)
    return None