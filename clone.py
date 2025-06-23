from error import throw_error
from colorama import Fore
from bin.utils import is_gitlite_initialized

def clone_repo(link: str):
    # write logic to add files for staging
    # Throw error if link is invalid
    print(f"Cloned repo: {link}")

def clone(cmd:str, link = None):
    if not is_gitlite_initialized():
        return Fore.RED + "Repository not initalized! Run `gitlite init` to initialize repository"
    if link and link!="Empty":
        clone_repo(link)
    else:
        return throw_error(cmd, invalid= True)
    return None