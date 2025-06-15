import os
import shutil
from error import throw_error

def init_repo(print_msg, new_dir=""):
    # Write logic to intialize repository
    # if repository already exists, throw error message to def init 
    #   From def init return that error message instead of None
    if new_dir!="":
        try:
            os.mkdir(new_dir)
            os.chdir(new_dir)
        except FileExistsError:
            print(f"Directory '{new_dir}' already exists.")
        except Exception as e:
            print(f"An error occurred: {e}")
            
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
                print(f"Error creating INDEX file: {e}")
                pass
            for c in contents:
                try:
                    os.makedirs(c, 0o777)
                except:
                    print("Unable to create ", c)

            try:
                with open("refs/HEAD", "w") as f:
                    f.write("ref: refs/heads/main\n")
            except Exception as e:
                print(f"Error creating HEAD file: {e}")
            try:
                with open("refs/heads/main", "w") as f:
                    pass
            except Exception as e:
                print(f"Error creating main branch: {e}")

        except Exception as e:
            print(e)
        if print_msg:
            print("Initialised an empty gitLite repository")

    except FileExistsError:
        shutil.rmtree(dir_name, ignore_errors=False)
        init_repo(False, "")
        print(f"Reinitialize gitLite repository in '{os.path.dirname(os.getcwd())}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    

def init(cmd:str, dir = None):
    if dir and dir!="Empty":
        init_repo(True, dir)
    elif dir and dir=="Empty":
        init_repo(True, "")
    else:
        return throw_error(cmd, invalid= True)
    return None