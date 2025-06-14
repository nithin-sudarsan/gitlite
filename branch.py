from error import throw_error

def show_all_branches():
    # write logic to show all branches
    print("all branches")

def rename_branch(new_name):
    # Write logic to rename current branch
    print(f"Branch renamed to: {new_name}")

def delete_branch(branch_name):
    # Write logic to delete branch
    # throw error if trying to delete current branch
    print(f"Deleted branch: {branch_name}")


def branch(cmd: str, rename = None, delete = None):
    if rename=="Empty" and delete=="Empty": 
        show_all_branches()
    else:
        if rename and rename!="Empty":
            rename_branch(rename)
        elif delete and delete!="Empty":
            delete_branch(delete)
        else:
            return throw_error(cmd, True)
    return None