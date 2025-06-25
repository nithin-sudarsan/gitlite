from gitlite.bin.utils import is_gitlite_initialized, get_curr_branch, get_commit_history
from colorama import Fore
from gitlite.bin.CommitObject import CommitObject

def branch_logs(branch = None):
    branch_name = None
    if branch:
        branch_name = branch
        commit_history: dict[CommitObject] = get_commit_history(branch)
    else:
        branch_name = get_curr_branch().split('/')[-1]
        commit_history: dict[CommitObject] = get_commit_history()
   
    if len(commit_history) != 0:
        print(f"Displaying logs of branch: {Fore.GREEN + branch_name + Fore.RESET}")
        for commit_hash, commit_object in commit_history.items():
            print("Commit: " + Fore.YELLOW + commit_hash + Fore.RESET)
            print("Date: " + commit_object.timestamp.strftime("%b %d, %Y %H:%M:%S %z"))
            print(f"\t{commit_object.message}")
            print("\n")
    else:
        return Fore.RED + f"No commits in branch: {branch_name}!"
    return None


def log(branch_name = None):
    if not is_gitlite_initialized():
        return Fore.RED + "Repository not initalized! Run `gitlite init` to initialize repository"
    if branch_name != "Empty":
        err = branch_logs(branch_name)
    else:
        err = branch_logs()
    return err