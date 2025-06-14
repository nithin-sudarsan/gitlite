from error import throw_error

def clone_repo(link: str):
    # write logic to add files for staging
    # Throw error if link is invalid
    print(f"Cloned repo: {link}")

def clone(cmd:str, link = None):
    if link and link!="Empty":
        clone_repo(link)
    else:
        return throw_error(cmd, invalid= True)
    return None