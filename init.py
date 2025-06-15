from error import throw_error

def initNewRepo():
    # Write logic to intialize repository
    # if repository already exists, throw error message to def init 
    #   From def init return that error message instead of None

    print("Initialised an empty gitlite repository")

def initRepo(dir):
    # Write logic to intialize repository
    # if repository already exists, throw error message to def init 
    #   From def init return that error message instead of None
    print(f"Initialised an empty gitlite repository in {dir}")

def init(cmd:str, dir = None):
    if dir and dir!="Empty":
        initRepo(dir)
    elif dir and dir=="Empty":
        initNewRepo()
    else:
        return throw_error(cmd, invalid= True)
    return None