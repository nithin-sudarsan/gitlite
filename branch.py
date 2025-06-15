from error import throw_error

def show_all_branches():
    # write logic to show all branches
    print("all branches")

def create_branch(branch_name):
    # Write logic to checkout to a new branch
    # Throw error if branch already exisits
    print(f"Created new branch: {branch_name}")

def rename_branch(new_name):
    # Write logic to rename current branch
    print(f"Branch renamed to: {new_name}")

def delete_branch(branch_name):
    # Write logic to delete branch
    # throw error if trying to delete current branch
    print(f"Deleted branch: {branch_name}")


def branch(cmd: str, new_branch = None, rename = None, delete = None):
    if new_branch=="Empty" and rename=="Empty" and delete=="Empty": 
        show_all_branches()
    else:
        if rename and rename!="Empty":
            rename_branch(rename)
        elif delete and delete!="Empty":
            delete_branch(delete)
        elif new_branch and new_branch!="Empty":
            create_branch(new_branch)
        else:
            return throw_error(cmd, True)
    return None