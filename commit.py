from error import throw_error

def commit_staged(message: str):
    # write logic to add files for staging
    print(f"Commit message: {message}")

def commit(cmd:str, message = None):
    if message and message != "Empty" :
        commit_staged(message)
    elif message and message == "Empty":
        return throw_error(cmd, invalid= False)
    else:
        return throw_error(cmd, invalid= True)
    return None