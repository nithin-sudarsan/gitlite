#!/usr/bin/env python3
import argparse
from gitlite.init import init
from gitlite.status import status
from gitlite.add import add
from gitlite.commit import commit
from gitlite.checkout import checkout
from gitlite.branch import branch
from gitlite.log import log
from gitlite.bin.utils import welcomeMessage

def main():
    parser = argparse.ArgumentParser(description = "A lite version of git")
    subparser = parser.add_subparsers(dest="command", help="Subcommand help")

    init_parser = subparser.add_parser("init", help = "Initializes an empty gitlite repository")
    init_parser.add_argument("dir", nargs="?",type=str, help="Create a new directory and intialize repository", default="Empty")

    status_parser = subparser.add_parser("status", help = "Check staging status of files in working tree.")

    add_parser = subparser.add_parser("add", help = "Adds files to staging")
    add_parser.add_argument("path", nargs="*", type=str, help="Mention file path(s)", default=[])

    commit_parser = subparser.add_parser("commit", help = "Commit staged files")
    commit_parser.add_argument("-m", nargs="?", type=str, help="Commit message", default="Empty")
    commit_parser.add_argument("-a", "--amend", nargs="?", type=str, help="Amend to previous commit", default="Empty")

    branch_parser = subparser.add_parser("branch", help = "See and modify branches")
    branch_parser.add_argument("branch", nargs="?", type=str, help="Create a new branch", default="Empty")
    branch_parser.add_argument("-m", nargs="*", type=str, help="Rename current branch", default="Empty")
    branch_parser.add_argument("-d", nargs="?", type=str, help="Delete branch", default="Empty")

    checkout_parser = subparser.add_parser("checkout", help = "Checkout to a branch")
    checkout_parser.add_argument("branch", nargs="?", type=str, help="Branch name to checkout to", default="Empty")
    checkout_parser.add_argument("-b", nargs="?", type=str, help="Checkout to a new branch", default="Empty")

    log_parser = subparser.add_parser("log", help = "Check branch logs")
    log_parser.add_argument("branch", nargs="?", type=str, help="Branch name to see logs", default="Empty")
   
    args = parser.parse_args()
    args_dict = args.__dict__

    cmd = args_dict["command"]

    match cmd:
        case "init":
            err = init(cmd, args_dict["dir"])
            if err != None:
                print(err)
        case "status":
            err = status()
            if err != None:
                print(err)
        case "add":
            err = add(cmd, args_dict["path"])
            if err != None:
                print(err)
        case "commit":
            err = commit(cmd, message=args_dict["m"], amend=args_dict["amend"])
            if err != None:
                print(err)
        case "branch":
            err = branch(cmd, new_branch=args_dict["branch"], rename=args_dict["m"], delete=args_dict["d"])
            if err != None:
                print(err)       
        case "checkout":
            err = checkout(cmd, branch_name=args_dict["branch"], new_branch=args_dict["b"])
            if err != None:
                print(err)
        case "log":
            err = log(branch_name=args_dict["branch"])
            if err != None:
                print(err)  
        case default:
            welcomeMessage()

if __name__ == "__main__":
    main()