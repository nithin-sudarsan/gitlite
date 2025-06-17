import os
from add import read_index
from colorama import Fore, Style
from bin.TreeItem import TreeItem
from bin.utils import sha1, get_all_files

def check_status():
    all_files = get_all_files()
    staged:dict[str, TreeItem] = {}
    staged = read_index(staged)
    staged_files = []
    unstaged_files = []
    modified_files = []
    for file in all_files:
        if file not in staged:
            unstaged_files.append(file)
        else:
            if staged[file].hash == sha1(file):
                staged_files.append(file)
            else:
                modified_files.append(file)
    if len(modified_files) > 0:
        print(f"\nModified files:")
        for file in modified_files:
            print(Fore.RED + f"\t{file}")
    print(Style.RESET_ALL)
    if len(unstaged_files) > 0:
        print(f"\nUntracked files:")
        for file in unstaged_files:
            print(Fore.RED + f"\t{file}")
    print(Style.RESET_ALL)
    if len(staged_files) > 0:
        print(f"\nStaged files:")
        for file in staged_files:
            print(Fore.GREEN + f"\t{file}")
    print(Style.RESET_ALL)


def status():
    if os.path.exists('.gitlite/index'):
        check_status()
        return None
    else:
        return Fore.RED + "Repository not initalized! Run `gitlite init` to initialize repository"