import os
import shutil
from gitlite.error import throw_error
from colorama import Fore

def init_repo(print_msg, new_dir=""):
    if new_dir!="":
        try:
            os.mkdir(new_dir, 0o777)
            os.chdir(new_dir)
        except FileExistsError:
            return Fore.RED + f"Directory '{new_dir}' already exists."
        except Exception as e:
            return Fore.RED + f"An error occurred: {e}"
            
    dir_name = '.gitlite'
    try:
        os.mkdir(dir_name, 0o777)
        os.chdir(dir_name)
        contents = ['objects', 'refs', 'refs/heads']
        try:
            try:
                with open("index", "w") as f:
                    pass
            except Exception as e:
                return Fore.RED + f"Error creating INDEX file: {e}"
            for c in contents:
                try:
                    os.makedirs(c, 0o777)
                except:
                    return Fore.RED + f"Unable to create {c}"

            try:
                with open("refs/HEAD", "w") as f:
                    f.write("ref: refs/heads/main\n")
            except Exception as e:
                return Fore.RED + f"Error creating HEAD file: {e}"
            try:
                with open("refs/heads/main", "w") as f:
                    pass
            except Exception as e:
                return Fore.RED + f"Error creating main branch: {e}"

        except Exception as e:
            return (e)
        if print_msg:
            return (Fore.GREEN + "Initialized an empty GitLite repository!")
        return None

    except FileExistsError:
        shutil.rmtree(dir_name, ignore_errors=False)
        init_repo(False, "")
        return Fore.GREEN + f"Reinitialized GitLite repository in '{os.path.dirname(os.getcwd())}'"
    except Exception as e:
        return Fore.RED + f"An error occurred: {e}"
    

def init(cmd:str, dir = None):
    if dir and dir!="Empty" and len(dir) == 1:
        err = init_repo(True, dir)
    elif dir and dir=="Empty":
        err = init_repo(True, "")
    else:
        return throw_error(cmd, invalid= True)
    return err