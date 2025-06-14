from error import throw_error

def checkout_to(branch_name):
    # Write logic to checkout to existing branch
    print(f"Switched to: {branch_name}")

def create_branch(branch_name):
    # Write logic to checkout to a new branch
    # Throw error if branch already exisits
    print(f"Created new branch: {branch_name}")

def checkout(cmd: str, branch_name = None, new_branch = None):
    if branch_name=="Empty" and new_branch=="Empty": 
        return throw_error(cmd, False)
    elif branch_name and branch_name!="Empty":
        checkout_to(branch_name)
    elif new_branch and new_branch!="Empty":
        create_branch(new_branch)
    else:
        return throw_error(cmd, True)
    return None