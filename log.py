from bin.utils import is_gitlite_initialized, get_curr_branch, get_commit_history
from colorama import Fore
from bin.CommitObject import CommitObject

def branch_logs(branch = None):
    if branch:
        print(f"Displaying logs of branch: {Fore.GREEN + branch + Fore.RESET}")
        commit_history: dict[CommitObject] = get_commit_history(branch)
    else:
        print(f"\nDisplaying logs of current branch: {Fore.GREEN + get_curr_branch().split('/')[-1] + Fore.RESET}\n")
        commit_history: dict[CommitObject] = get_commit_history()
   
    for commit_hash, commit_object in commit_history.items():
        print("Commit: " + Fore.YELLOW + commit_hash + Fore.RESET)
        print("Date: " + commit_object.timestamp.strftime("%b %d, %Y %H:%M:%S %z"))
        print(f"\t{commit_object.message}")
        print("\n")
    return None


def log(branch_name = None):
    if not is_gitlite_initialized():
        return Fore.RED + "Repository not initalized! Run `gitlite init` to initialize repository"
    if branch_name != "Empty":
        err = branch_logs(branch_name)
    else:
        err = branch_logs()
    return err