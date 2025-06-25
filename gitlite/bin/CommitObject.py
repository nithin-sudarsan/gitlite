import datetime

class CommitObject:
    def __init__(self, message, treehash, parenthash):
        self.timestamp = datetime.datetime.now()
        self.message: str = message
        self.treehash: str = treehash
        self.parenthash: str = parenthash