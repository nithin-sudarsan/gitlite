# GitLite
A lightweight implementation of Git-like version control system built from scratch in Python, designed to provide deeper understanding of Git's internal workings. Its core functionality revolves around staging and committing files, managing branches, and tracking file changes using SHA-1 hashes.

To read in detail about the internal working of a version control system, checkout [this blog](notnith.in/blogs/git-working). [⚠️ To be updated]

## Currently available features
- **`init`** : Initializes an empty gitlite repository
- **`status`** : Check staging status of files in working tree
- **`add`** : Adds files for staging
- **`commit`**: Creates a snapshot of the repository, storing metadata like timestamps, commit messages, and tree hashes.
    - **`-m`**: Commit message
    - **`-a` / `--amend`** : Amend to previous commit
- * **File Tracking:**  Uses SHA-1 hashes (`sha1`, `calculate_sha1`) to identify file changes and `TreeItem` objects to represent files within the file system tree.
- **`.gitignore` Support**: Implements `.gitignore` parsing to exclude specified files from tracking.

**Architecture:**

The system utilizes a tree-based structure to represent the file system, with `TreeItem` objects as nodes. `CommitObject` instances represent commits, linked to their parent commits and associated tree objects.  An index file tracks the staging area.  Utility functions provide core operations like SHA-1 hashing, file system traversal, and `.gitignore` handling.

**Technologies Used:**

* Python: The primary programming language.
* SHA-1: For file hashing.
* `enum` module: For type-safe file type representation (`FileType`).

**Purpose:**

The project aims to provide a simplified, educational implementation of core Git concepts, focusing on staging, committing, and branching.

