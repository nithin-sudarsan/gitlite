# GitLite
A lightweight implementation of Git-like local version control system built from scratch in Python, designed to provide deeper understanding of Git's internal workings. Its core functionality revolves around staging and committing files, managing branches, and tracking file changes using SHA-1 hashes.

To read in detail about the internal working of a version control system, checkout [this blog](notnith.in/blogs/gitlite-internal-working). [⚠️ To be updated]

## Available features
- **`init`** : Initializes an empty gitlite repository
- **`status`** : Showing the status of the working directory, including `staged`, `modified`, and `untracked files`.
- **`add`** : Adds files for staging
- **`commit`**: Creates a snapshot of the repository, storing metadata like timestamps, commit messages, and tree hashes.
    - **`-m`**: Commit message
    - **`-a` / `--amend`** : Amend to previous commit
- **`branch`**: See, create and modify branches
    - **`branch_name`**: Create new branch
    - **`-m`**: Rename current branch
    - **`-d`**: Delete a branch (other than current branch)
- **`checkout`**: Switch between branches
    - **`branch_name`**: Checkout to a new branch
    - **`-b`**: Create new branch and checkout to that branch
- **`log`**: View commit history of current branch
    - **`branch_name`**: View commit history of a particular branch
- **`.gitignore` Support**: Implements `.gitignore` parsing to exclude specified files from tracking.

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