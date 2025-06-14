def checkout(branch=None, new_branch = None):
    if branch and new_branch:
        print("Both branch and new branch cannot exist")
    elif branch:
        print(f"Checkedout to: {branch}")
    elif new_branch:
        print(f"Checkedout to new branch: {new_branch}")
    else:

        print("Invalid use of checkout command")
        