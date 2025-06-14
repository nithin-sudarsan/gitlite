import argparse
from init import init
from add import add
from commit import commit
from checkout import checkout
from branch import branch
from clone import clone

def welcomeMessage():
    print("GitLite by Nithin!")
    print("Available commands:")
    print("\tinit: Initializes an empty gitlite repository")
    print("\tadd: Adds files to staging")
    print("\tcommit: Commit staged files")
    print("\tbranch: Creates a new branch")
    print("\tcheckout: Checkout to branch")
    print("\tclone: Clones a remote repository")
    print("\thelp: Display this help message")

def main():
    parser = argparse.ArgumentParser(description = "A lite version of git")
    subparser = parser.add_subparsers(dest="command", help="Subcommand help")

    init_parser = subparser.add_parser("init", help = "Initializes an empty gitlite repository")

    add_parser = subparser.add_parser("add", help = "Adds files to staging")
    add_parser.add_argument("path", nargs="?",type=str, help="Mention file path", default="Empty")

    commit_parser = subparser.add_parser("commit", help = "Commit staged files")
    commit_parser.add_argument("-m", nargs="?", type=str, help="Commit message", default="Empty")

    branch_parser = subparser.add_parser("branch", help = "See and modify branches")
    branch_parser.add_argument("-m", nargs="?", type=str, help="Rename current branch", default="Empty")
    branch_parser.add_argument("-d", nargs="?", type=str, help="Delete branch", default="Empty")

    checkout_parser = subparser.add_parser("checkout", help = "Checkout to a branch")
    checkout_parser.add_argument("branch", nargs="?", type=str, help="Branch name to checkout to", default="Empty")
    checkout_parser.add_argument("-b", nargs="?", type=str, help="Checkout to a new branch", default="Empty")

    clone_parser = subparser.add_parser("clone", help = "Clone a remote repository")
    clone_parser.add_argument("hyperlink", nargs="?",type=str, help="HTTPS reference to clone repository", default=None)
   
    args = parser.parse_args()
    args_dict = args.__dict__

    cmd = args_dict["command"]

    match cmd:
        case "init":
            err = init(cmd)
            if err != None:
                print(err)
        case "add":
            err = add(cmd, args_dict["path"])
            if err != None:
                print(err)
        case "commit":
            err = commit(cmd, message=args_dict["m"])
            if err != None:
                print(err)
        case "branch":
            err = branch(cmd, rename=args_dict["m"], delete=args_dict["d"])
            if err != None:
                print(err)       
        case "checkout":
            err = checkout(cmd, branch_name=args_dict["branch"], new_branch=args_dict["b"])
            if err != None:
                print(err)
        case "clone":
            err = clone(cmd, args_dict["hyperlink"])
            if err != None:
                print(err)    
        case default:
            welcomeMessage()

if __name__ == "__main__":
    main()