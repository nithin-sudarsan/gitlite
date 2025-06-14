import argparse
from init import initRepo
from add import add
from commit import commit
from checkout import checkout
from branch import Branch
from clone import clone

def displayHelp():
    print("GitLite by Nithin!")
    print("Available commands:")
    print("\tinit: Initializes an empty gitlite repository ")
    print("\tadd: Adds files to staging")
    print("\tcommit: Commit staged files")
    print("\tbranch: Creates a new branch")
    print("\tcheckout: Checkout to branch")
    print("\tclone: Clones a remote repository")
    print("\thelp: Display this help message")

def main():
    parser = argparse.ArgumentParser(description = "A lite version of git")
    subparser = parser.add_subparsers(dest="command", help="Subcommand help")

    init_parser = subparser.add_parser("init", help = "initialize git")

    add_parser = subparser.add_parser("add", help = "Stage files to commit")
    add_parser.add_argument("path", nargs="?",type=str, help="Mention file path", default=None)

    commit_parser = subparser.add_parser("commit", help = "Commit staged files")
    commit_parser.add_argument("-m", type=str, help="Commit message", default="")

    branch_parser = subparser.add_parser("branch", help = "See and modify branches")
    branch_parser.add_argument("-m", type=str, help="Rename current branch", default=None)
    branch_parser.add_argument("-d", type=str, help="Delete branch", default=None)

    checkout_parser = subparser.add_parser("checkout", help = "Checkout to a different branch")
    checkout_parser.add_argument("branch", nargs="?", type=str, help="Branch name to checkout to", default=None)
    checkout_parser.add_argument("-b", type=str, help="Checkout to a new branch", default=None)

    clone_parser = subparser.add_parser("clone", help = "Clone a git repository")
    clone_parser.add_argument("hyperlink", nargs="?",type=str, help="HTTPS reference to clone repository", default=None)
   
    args = parser.parse_args()
    args_dict = args.__dict__

    cmd = args_dict["command"]

    match cmd:
        case "init":
            err = initRepo()
            if err != None:
                print(err)
        case "clone":
            err = clone(args_dict["hyperlink"])
            if err != None:
                print(err)
        case "add":
            err = add(args_dict["path"])
            if err != None:
                print(err)
        case "commit":
            commit(args_dict["m"])
        case "checkout":
            checkout(branch=args_dict["branch"], new_branch=args_dict["b"])
        case "branch":
            Branch(rename=args_dict["m"], delete=args_dict["d"])
        case default:
            displayHelp()

    """ 
    Three differnt approaches to handle cases in the swtich statement above
        1. return the error or execute the function
            err = initRepo()
            if err != None:
                print(err)
        2. Create classes instead of functions like how its done for case "branch"
        3. if-else conditions inside case:
            if args_dict["path"]:
                add(args_dict["path"])
            else:
                print("Invalid commad :( ")
                print("For help with gitlite add, try")
                print("\tmain.py add -h")
                print("\tmain.py add --help")
    """


if __name__ == "__main__":
    main()