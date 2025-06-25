from enum import Enum

# Making FileType an enum by inheriting from Enum
class FileType(Enum):
    BLOB = "blob"
    TREE = "tree"