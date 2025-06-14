class Branch:
    def __init__(self, rename, delete):
        self.rename = rename
        self.delete = delete
        if (self.rename != None):
            print(f"Branch renamed to: {rename}")
        elif (self.delete != None):
            print(f"Deleted branch: {delete}")
        elif (self.delete == None or self.rename == None):
            Branch.show_all_branches()
        

    def show_all_branches():
        print("all branches")