from error import throw_error

def commit_staged(message: str):
    # write logic to add files for staging
    print(f"Commit message: {message}")

def commit_amend():
    # write logic to amend to previous commit
    print(f"Amended to previous commit")

def commit(cmd:str, message = None, amend = None):
    if message and message != "Empty" :
        commit_staged(message)
    elif not amend:
        commit_amend()
    elif amend:
        return throw_error(cmd, invalid= True)
    elif message and message == "Empty":
        return throw_error(cmd, invalid= False)
    else:
        return throw_error(cmd, invalid= True)
    return None