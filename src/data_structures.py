class Node:
    def __init__(self):
        self.code = []
        self.ident_list = []
        self.type_list = []
        self.data = {}


class SymTable:
    def __init__(self):
        self.parent = None
        self.table = {}

    def set_parent(self, parent):
        self.parent = parent

