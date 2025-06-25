from gitlite.error import throw_error
from gitlite.branch import create_branch
from colorama import Fore
from gitlite.bin.utils import is_gitlite_initialized, get_curr_branch
import os

def switch_to(branch_name, create = False):
    existing_branches = os.listdir('.gitlite/refs/heads')
    if create:
        if branch_name in existing_branches:
            return Fore.RED + f"Error: Branch '{branch_name}' already exist!"
        else:
            create_branch(branch_name)
    checkout_branch_path = os.path.join('.gitlite/refs/heads', branch_name)
    curr_branch_path = get_curr_branch()
    if checkout_branch_path == curr_branch_path:
        return Fore.RED + f"Already in {branch_name}!"
    if os.path.exists(checkout_branch_path):
            with open('.gitlite/refs/HEAD', "w") as f:
                f.write(f"ref: refs/heads/{branch_name}\n")
            print(f"Switched to: {branch_name}")
            return None
    else:
        return Fore.RED + f"Error: Branch '{branch_name}' does not exist!"
    

def checkout(cmd: str, branch_name = None, new_branch = None):
    if not is_gitlite_initialized():
        return Fore.RED + "Repository not initalized! Run `gitlite init` to initialize repository"
    if branch_name=="Empty" and new_branch=="Empty": 
        return throw_error(cmd, False)
    elif branch_name and branch_name!="Empty":
        return switch_to(branch_name)
    elif new_branch and new_branch!="Empty":
        return switch_to(new_branch, True)
    else:
        return throw_error(cmd, True)