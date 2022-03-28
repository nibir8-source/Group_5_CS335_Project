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
        self.type_list = ['rune', 'bool', 'int',
                          'float', 'string', 'imaginary']
        self.type_size_list = {'rune': 1, 'bool': 4, 'int': 4,
                               'float': 4, 'string': 100, 'imaginary': 20}

    def set_parent(self, parent):
        self.parent = parent

    def insert(self, ident, attr):
        if(not self.table.get(ident)):
            self.table[ident] = {}
            self.table[ident]["type"] = attr

    def search(self, ident):
        return self.table.get(ident)

    def update(self, ident, key, value):
        if self.table.get(ident):
            self.table[ident][key] = value

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
            print_err = error['type'] + ': ' + \
                error['msg'] + ' on line ' + str(error['lineno'])
            print(print_err)


class LineCount:
    def __init__(self):
        self.lineno = 0

    def add(self, count):
        self.lineno += count

    def get(self):
        return self.lineno


class check_functions:
    def check_ident(self, scope_table, curr_scope, scope_list, ident, purpose):
        if purpose == "redeclaration":
            if scope_table[curr_scope].search(ident) != None:
                return True
            else:
                return False

        if purpose == 'check_declaration':
            for x in scope_list[::-1]:
                if(scope_table[x].search(ident) != None):
                    return x + 1
            return False

    def check_unary_operation(self, unop, exp1):
        unop = unop[0]
        if unop == "+" or unop == "-":
            if(len(exp1) > 1):
                return None
            exp1 = exp1[0]
            if exp1 == "int" or exp1 == "float" or exp1 == "rune" or exp1 == "imaginary":
                return [exp1]
            else:
                return None
        if unop == "!":
            if len(exp1) > 1:
                return None
            if exp1 == ["bool"]:
                return exp1
            else:
                return None
        if unop == "^":
            if len(exp1) > 1 or exp1[0] != "int":
                return None
            else:
                return exp1
        if unop == "*":
            if exp1[0] != "pointer":
                return None
            exp1 = exp1[1:]
            return exp1
        if unop == "&":
            exp2 = ["pointer"]
            exp1 = exp2+exp1
            return exp1

    def check_operation(self, expr_1, op, expr_2):
        if len(expr_1) > 1 or len(expr_2) > 1:
            return None
        if len(op) == 1:
            op = op[0]
        expr_1 = expr_1[0]
        expr_2 = expr_2[0]
        if expr_1 != expr_2:
            if (expr_1 == "int" and expr_2 == "float") or (expr_1 == "float" and expr_2 == "int"):
                if op == ">" or op == "<" or op == "==" or op == ">=" or op == "<=" or op == "!=":
                    return ["bool"]
                if op == "|" or op == "^" or op == "<<" or op == ">>" or op == "%" or op == "&" or op == "&^":
                    return None
                return ["float"]
            if (expr_1 == "imaginary" and expr_2 == "int") or (expr_1 == "imaginary" and expr_2 == "float") or (expr_1 == "int" and expr_2 == "imaginary") or (expr_1 == "float" and expr_2 == "imaginary"):
                if op == ">" or op == "<" or op == ">=" or op == "<=" or op == "|" or op == "^" or op == "<<" or op == ">>" or op == "%" or op == "&" or op == "&^":
                    return None
                if op == "==" or op == "!=":
                    return ["bool"]
                return ["imaginary"]

            return None
        if op == "||" or op == "&&":
            if(expr_1 == "bool"):
                # print(expr_1,op,expr_2)
                return [expr_1]
            else:
                return None
        if expr_1 == "int" or expr_1 == "rune":
            if op == ">" or op == "<" or op == "==" or op == ">=" or op == "<=" or op == "!=":
                return ["bool"]
            return [expr_1]
        if expr_1 == "float":
            if op == ">" or op == "<" or op == "==" or op == ">=" or op == "<=" or op == "==" or op == "!=":
                return ["bool"]
            if op == "|" or op == "^" or op == "<<" or op == ">>" or op == "%" or op == "&" or op == "&^":
                return None
            else:
                return [expr_1]
        if expr_1 == "string":
            if op == "+":
                return [expr_1]
            else:
                return None

        if expr_1 == "imaginary":
            if op == "+" or op == "-" or op == "*" or op == "/":
                return [expr_1]
            elif op == "!=" or op == "==":
                return ["bool"]
            else:
                return None
