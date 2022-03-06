class Node:
    def __init__(self, name):
        self.code = []
        self.name = name
        self.ident_list = []
        self.type_list = []
        self.expr_list = []
        self.data = {}


class SymTable:
    def __init__(self):
        self.parent = None
        self.table = {}

    def set_parent(self, parent):
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
        self.n += 1

    def print_all(self):
        for error in self.errors:
            print_err = error['type'] + ': ' + error['msg'] + ' on line ' + str(error['lineno'])
            print(print_err)