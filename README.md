# GitLite
A lightweight implementation of Git-like local version control system built from scratch in Python, designed to provide deeper understanding of Git's internal workings. Its core functionality revolves around staging and committing files, managing branches, and tracking file changes using SHA-1 hashes.

For more in-depth details on internal working of a version control system, checkout <a href="https://notnith.in/blogs/gitlite-internal-working" target = "_blank">this blog</a>.

## Available features and Usage
### Install python package
```
$ pip install gitlite
```
OR
```
$ pip install gitlite==0.3.1
```
### `gitlite init`
Initializes an empty gitlite repository
```
$ gitlite init
```
### `gitlite add`
Add files for staging
```
$ gitlite add <file-name1> <file-name2>
```
### `gitlite status`
View status of the working directory, including `staged`, `modified`, and `untracked files`.
```
$ gitlite status
```
### `gitlite commit`
Creates a snapshot of the repository, storing metadata like timestamps, commit messages, and tree hashes.
- **`-m`**: Commit message
- **`-a` / `--amend`** : Amend to previous commit
```
$ gitlite commit -m <commit-message>
```
#### Amend to previous commit
```
$ gitlite commit -a <new-commit-message>
```
### `gitlite branch`
View, create and modify branches
- **`branch_name`**: Create new branch
- **`-m`**: Rename current branch
- **`-d`**: Delete a branch (other than current branch)
#### View all branches
```
$ gitlite branch
```
#### Create a branch
```
$ gitlite branch <branch-name>
```
#### Rename a branch
```
$ gitlite branch -m <new-branch-name>
```
OR
```
$ gitlite branch -m <old-branch-name> <new-branch-name>
```
#### Delete a branch (other than current branch)
```
$ gitlite branch -d <branch-name>
```
### `gitlite checkout`
Switch between branches
- **`branch_name`**: Checkout to a new branch
- **`-b`**: Create new branch and checkout to that branch
```
$ gitlite checkout <branch-name>
```
### Create a new branch and checkout
```
$ gitlite checkout -b <new-branch-name>
```
### `gitlite log`
View commit history of current branch
- **`branch_name`**: View commit history of a particular branch
```
$ gitlite log <branch-name>
```
#### Current branch logs
```
$ gitlite log
```
### `.gitignore` Support 
Implements `.gitignore` parsing to exclude specified files from tracking.
### Further help
```
$ gitlite --help
```

## Architecture:

The system utilizes a tree-based structure to represent the file system, with `TreeItem` objects as nodes. `CommitObject` instances represent commits, linked to their parent commits and associated tree objects.  An index file tracks the staging area.  Utility functions provide core operations like SHA-1 hashing, file system traversal, and `.gitignore` handling.

## Technologies Used:

* Python: The primary programming language.
* SHA-1: For file hashing and identifying changes in within the file system tree.
* `enum` module: For type-safe file type representation (`FileType`).

**Purpose:**

The project aims to provide a simplified, educational implementation of core Git concepts, focusing on staging, committing, and branching.

## Potential Improvements
### Support for following git commands:
- **`merge`**: Merge one branch to another
- **`rebase`**: Change the base of current branch
- **`clone`**: Clone a remote repository
- **`push`**: Push changes to a remote repository
- **`pull`**: Pull changes from a remote repository

### Remote Repository Support
Implement the ability to interact with remote repositories (e.g., fetching, pushing). This is a significant undertaking but would greatly enhance GitLite's functionality.

### Configuration Management
Implement a more robust configuration management system. This would allow users to customize GitLite's behavior, such as:
- **User Information**: Store user name and email address.
- **Core Settings**: Store core GitLite settings (e.g., editor, merge tool).
- **Repository-Specific Settings**: Store settings specific to a particular repository.