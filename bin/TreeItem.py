from .FileType import FileType

class TreeItem:
    def __init__(self, filename, hash, filetype):
        self.filename: str = filename
        self.hash: str = hash
        self.filetype: FileType = filetype