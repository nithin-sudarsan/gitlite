from error import throw_error

def add_path(path: str):
    # write logic to add files for staging
    print(f"Adding: {path}")

def add(cmd:str, path = None):
    if path and path!="Empty":
        add_path(path)
    else:
        return throw_error(cmd, invalid= True)
    return None