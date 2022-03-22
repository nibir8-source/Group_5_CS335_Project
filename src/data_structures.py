class Node:
    def __init__(self, name):
        self.code = []
        self.name = name
        self.ident_list = []
        self.type_list = []
        self.expr_list = []
        self.expr_type_list = []
        self.data = {}
        self.ast = []


class SymTable:
    def __init__(self):
        self.parent = None
        self.table = {}
        self.type_list = ['rune','bool','int','float','string']
        self.type_size_list = {'rune':1,'bool':4,'int':4,'float':4,'string':100, }

    def set_parent(self, parent):
        self.parent = parent

    def insert(self, ident, attr):
        if(not self.table.get(ident)):
            self.table[ident] = {}
            self.table[ident]["type"] = attr
    def search(self,ident):
        return self.table.get(ident)

    def update(self, ident, key, value):
        if self.table.get(ident):
            self.table[ident][key]=value

    def assign_parent(self, parent):
        self.parent = parent


class Errors:

    def __init__(self):
        self.errors = []
        self.n = 0

    def add_error(self, type, lineno, msg):
        error = {}
        error['type'] = type
        error['msg'] = msg
        error['lineno'] = lineno
        self.errors.append(error)
        print(error)
        self.n += 1

    def print_all(self):
        for error in self.errors:
            print_err = error['type'] + ': ' + error['msg'] + ' on line ' + str(error['lineno'])
            print(print_err)