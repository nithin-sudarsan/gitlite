from error import throw_error
from branch import create_branch

def switch_to(branch_name):
    # Write logic to checkout to existing branch
    print(f"Switched to: {branch_name}")

def checkout(cmd: str, branch_name = None, new_branch = None):
    if branch_name=="Empty" and new_branch=="Empty": 
        return throw_error(cmd, False)
    elif branch_name and branch_name!="Empty":
        switch_to(branch_name)
    elif new_branch and new_branch!="Empty":
        create_branch(new_branch)
    else:
        return throw_error(cmd, True)
    return None