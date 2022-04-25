import pickle as pkl
import pickle
import pprint
import sys
import ply.yacc as yacc
from ply.lex import TOKEN, line_number
import sys
import lexer
from lexer import *
from data_structures import SymTable
from data_structures import Node
from data_structures import Errors
from data_structures import check_functions
import csv


precedence = (
    ('left', 'IDENT'),
    ('left', 'DEFINE'),
    ('left', 'COMMA'),
    ('left', 'LEFT_BRACKET'),
    ('left', 'RIGHT_BRACKET'),
    ('left', 'PERIOD'),
    ('left', 'SEMICOLON'),
    ('left', 'COLON'),
    ('left', 'INT'),
    ('left', 'FLOAT'),
    ('left', 'STRING'),
    ('left', 'BREAK'),
    ('left', 'CONTINUE'),
    ('left', 'RETURN'),
    ('left', 'LEFT_PARENTHESIS'),
    ('left', 'RIGHT_PARENTHESIS'),
    ('right', 'ASSIGNMENT', 'NOT'),
    ('left', 'LOGICAL_OR'),
    ('left', 'LOGICAL_AND'),
    ('left', 'EQUAL', 'NOT_EQUAL', 'LESS_THAN',
     'LESS_THAN_EQUAL', 'GREATER_THAN', 'GREATER_THAN_EQUAL'),
    ('left', 'ADD', 'SUBTRACT', 'OR', 'XOR'),
    ('left', 'MULTIPLY', 'QUOTIENT', 'REMAINDER',
     'SHIFT_LEFT', 'SHIFT_RIGHT', 'AND', 'AND_NOT')
)

checker = check_functions()
curr_scope = 0
scope_number = 0
scope_list = [0]
scope_table = {}

scope_table[0] = SymTable()
open_for = 0
open_switch = 0
curr_func = 0
errors = Errors()
start_for = []
end_for = []
label_count = 0
curr_switch_type = 0
temp_count = 0
switch_expr = ""
curr_struct = 0
struct_offset = 0
curr_func_scope = 0
offset_list = [0]
struct_sym_list = []
basic_types_list = ["int", "float", "rune", "string", "bool", "imaginary"]


file1 = open("tree.txt", "w")  # write mode
#file1 = open(outputHtml,"a")
file1.write("digraph graphname {")
file1.write("\n")
counter = 0

Sf_node = Node("Sf_node")


def writeGraph(Ast_list):
    global counter
    local = counter
    counter += 1
    name = Ast_list[0]
    if(len(Ast_list) > 1):
        for node_list in Ast_list[1:]:
            if(len(node_list) > 0):
                file1.write(str(local))
                file1.write("[label=\"")
                file1.write(name)
                file1.write("\" ] ;")
                file1.write(str(counter))
                file1.write("[label=\"")
                if ((node_list[0][0]) == "\""):
                    node_list[0] = node_list[0][1:-1]
                file1.write(node_list[0])
                file1.write("\" ] ;")
                file1.write(str(local) + "->" + str(counter) + ";")
                file1.write("\n")
                writeGraph(node_list)


def open_scope():
    global curr_scope
    global scope_list
    global scope_number
    prev_scope = curr_scope
    scope_number += 1
    curr_scope = scope_number
    scope_list.append(curr_scope)
    offset_list.append(4)
    scope_table[curr_scope] = SymTable()
    scope_table[curr_scope].assign_parent(prev_scope)
    scope_table[curr_scope].type_list = scope_table[prev_scope].type_list
    scope_table[curr_scope].type_size_list = scope_table[prev_scope].type_size_list
    for x in scope_table[0].table:
        if(scope_table[0].table[x]["type"] == ["func"]):
            scope_table[curr_scope].insert(x, ["func"])
    for x in scope_table[prev_scope].table:
        if(scope_table[prev_scope].table[x]["type"] == ["struct"]):
            scope_table[curr_scope].table[x] = scope_table[prev_scope].table[x]


def close_scope():
    global curr_scope
    global scope_list
    curr_scope = scope_list[-2]
    scope_list.pop()


def create_label(p=None):
    global label_count
    label = "label_no_" + str(label_count)
    label_count += 1
    if ((not p is None) and (p == 1)):
        start_for.append(label)
    if not p is None and p == 2:
        end_for.append(label)
    return label


def create_temp(p=None):
    global temp_count
    if p is None:
        temp = "temp_no_" + str(temp_count)
        temp_count += 1
        scope_table[curr_scope].insert(temp, "temp")
    else:
        temp = "var_temp_no_" + str(temp_count)
        temp_count += 1
    return temp

# ----------------------------------------------------------------------------------------


def p_source_file(p):
    '''SourceFile  : PackageClause SEMICOLON ImportDeclStar TopLevelDeclStar'''
    global Sf_node
    p[0] = Node('SourceFile')
    p[0].code += p[1].code + p[3].code + p[4].code
    p[0].ast = ["SourceFile", p[1].ast, p[3].ast, p[4].ast]
    csv_file = "symbol_table.csv"
    with open(csv_file, 'w+') as csvfile:
        for x in range(0, scope_number+1):
            #           print("Table number",x)
            writer = csv.writer(csvfile)
            writer.writerow([])
            writer.writerow(["Table Number", x])
            writer.writerow([])
            writer.writerow(["Parent", x, "=", scope_table[x].parent])
            writer.writerow([])
            for key, value in scope_table[x].table.items():
                writer.writerow([key, value])
    f = open('code.txt', "w")
    for i in range(0, len(p[0].code)):
        y = ""
        for x in p[0].code[i]:
            y = y+" "+str(x)
        f.write(y+'\n')
    # print(p[0].ast)

    writeGraph(p[0].ast)
    file1.write("}")
    file1.close()
    Sf_node = p[0]


def p_open_scope(p):
    '''OpenScope : '''
    open_scope()


def p_close_scope(p):
    '''CloseScope : '''
    close_scope()


def p_open_for(p):
    '''OpenFor : '''
    global open_for
    open_for += 1
    create_label(1)
    create_label(2)


def p_close_for(p):
    '''CloseFor : '''
    global open_for
    open_for -= 1


def p_open_switch(p):
    '''OpenSwitch : '''
    global open_switch
    open_switch += 1
    create_label(1)
    create_label(2)


def p_close_switch(p):
    '''CloseSwitch : '''
    global open_switch
    open_switch -= 1


def p_open_struct(p):
    "OpenStruct : "
    struct_sym_list = []


def p_close_struct(p):
    "CloseStruct : "


def p_import_decl_star(p):
    '''ImportDeclStar : ImportDeclStar ImportDecl SEMICOLON 
    |'''
    p[0] = Node('ImportDeclStar')
    if(len(p) > 1):
        if(len(p[1].ast) > 0 and len(p[2].ast) > 0):
            p[0].ast = ['ImportDeclStar', p[1].ast, p[2].ast]
        elif(len(p[1].ast) > 0):
            p[0].ast = p[1].ast
        elif(len(p[2].ast) > 0):
            p[0].ast = p[2].ast
        else:
            p[0].ast = []
        p[0].code += p[1].code+p[2].code


def p_top_level_decl_star(p):
    '''TopLevelDeclStar : TopLevelDeclStar TopLevelDecl SEMICOLON 
    |'''
    p[0] = Node('TopLevelDeclStar')
    if(len(p) > 1):
        # if(len(p[1].ast))
        if(len(p[1].ast) > 0 and len(p[2].ast) > 0):
            p[0].ast = ['TopLevelDeclStar', p[1].ast, p[2].ast]
        elif(len(p[1].ast) > 0):
            p[0].ast = p[1].ast
        elif(len(p[2].ast) > 0):
            p[0].ast = p[2].ast
        else:
            p[0].ast = []
        p[0].code += p[1].code
        p[0].code += p[2].code


def p_top_level_decl(p):
    '''TopLevelDecl : Declaration 
    | FunctionDecl'''
    p[0] = Node("TopLevelDecl")
    p[0] = p[1]

    # print(p[1].ast)


def p_package_clause(p):
    '''PackageClause : PACKAGE IDENT'''

    p[0] = Node('PackageClause')
    p[0].ast = [p[2]]
    p[0].ident_list.append(p[2])


def p_import_decl(p):
    '''ImportDecl : IMPORT ImportSpec 
                    | IMPORT LEFT_PARENTHESIS ImportSpecSemicolonStar RIGHT_PARENTHESIS'''
    p[0] = Node('ImportDecl')

    if len(p) == 3:
        p[0].ast = p[2].ast

    else:

        p[0].ast = p[3].ast


def p_import_spec_semicolon_star(p):
    '''ImportSpecSemicolonStar : ImportSpecSemicolonStar ImportSpec SEMICOLON 
    |'''
    p[0] = Node('ImportSpecSemicolonStar')
    if len(p) > 1:

        if(len(p[1].ast) > 0 and len(p[2].ast) > 0):
            p[0].ast = ['ImportSpecSemicolonStar', p[1].ast, p[2].ast]
        elif(len(p[1].ast) > 0):
            p[0].ast = p[1].ast
        elif(len(p[2].ast) > 0):
            p[0].ast = p[2].ast
        else:
            p[0].ast = []


def p_import_spec(p):
    '''ImportSpec : PERIOD ImportPath
    | IDENT ImportPath
    | ImportPath'''
    p[0] = Node('ImportSpec')
    if(len(p) > 2):
        p[0] = p[2]

    else:
        p[0] = p[1]


def p_import_path(p):
    '''ImportPath : STRING'''
    p[0] = Node('ImportPath')
    p[0].ast = [p[1]]


# -----------------------------------------------------------------------------


def p_declaration(p):
    '''Declaration : ConstDecl 
    | StructDecl
    | VarDecl'''
    p[0] = Node("Declaration")
    p[0] = p[1]
    # print("hell", p[0].ast)


def p_struct_decl(p):
    """StructDecl : TYPE StructName StructType"""
    p[0] = Node('StructDecl')
    scope_table[curr_scope].type_list.append(curr_struct)
    scope_table[curr_scope].type_size_list[curr_struct] = struct_offset


def p_struct_name(p):
    """StructName : IDENT"""
    p[0] = Node('StructName')
    global curr_struct, struct_offset
    curr_struct = p[1]
    struct_offset = 0
    if p[1] in scope_table[curr_scope].type_list:
        errors.add_error('Redeclaration Error', line_number.get()+1,
                         "Redeclaration of type " + p[1])
    if p[1] in scope_table[curr_scope].table:
        errors.add_error('Redeclaration Error', line_number.get()+1,
                         "Redeclaration of variable " + p[1])
    scope_table[curr_scope].insert(p[1], ["struct"])


def p_const_decl(p):
    '''ConstDecl : CONST ConstSpec
                | CONST LEFT_PARENTHESIS ConstSpecStar RIGHT_PARENTHESIS'''
    p[0] = Node("ConstDecl")
    # print(p[0].ast)
    if len(p) == 3:
        p[0] = p[2]
        p[0].ast = p[2].ast
    else:
        p[0] = p[3]
        p[0].ast = p[2].ast


def p_const_spec_star(p):
    '''ConstSpecStar : ConstSpecStar ConstSpec SEMICOLON
    |'''
    p[0] = Node("ConstSpecStar")
    if len(p) > 1:
        if(len(p[1].ast) > 0 and len(p[2].ast) > 0):
            p[0].ast = ['ConstSpecStar', p[1].ast, p[2].ast]
        elif(len(p[1].ast) > 0):
            p[0].ast = p[1].ast
        elif(len(p[2].ast) > 0):
            p[0].ast = p[2].ast
        else:
            p[0].ast = []
        # p[0].code += p[1].code
        p[0].code += p[2].code


def p_const_spec(p):
    '''ConstSpec : IdentifierList
                | IdentifierList ASSIGNMENT ExpressionList
                | IdentifierList IDENT ASSIGNMENT ExpressionList'''
    p[0] = Node("ConstSpec")
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 5:
        p[0].code = p[1].code+p[4].code
        p[0].ast = ["=", p[1].ast, [p[2]], p[4].ast]
        if len(p) == 5 and p[2] not in basic_types_list:
            errors.add_error("Type Error", line_number.get()+1,
                             "Invalid type for constant " + p[2])
        if len(p[1].ident_list) != len(p[4].expr_list):
            errors.add_error("Assignment Error", line_number.get(
            )+1, "Imbalaced assignment")
        for x in p[1].ident_list:
            if checker.check_ident(scope_table, curr_scope, scope_list, x, 'redeclaration') == True:
                errors.add_error("Redeclaration error", line_number.get(
                )+1, "Redeclaration of variable " + x)
            else:
                var1 = create_temp(1)
                scope_table[curr_scope].insert(x, [p[2]])
                scope_table[curr_scope].insert(var1, x)
                scope_table[curr_scope].update(x, "tmp", var1)
                scope_table[curr_scope].update(
                    x, "offset", offset_list[curr_func_scope])
                offset_list[curr_func_scope] += scope_table[curr_scope].type_size_list[p[2]]
                scope_table[curr_scope].update(x, 'constant', True)

        for i in range(0, len(p[1].ident_list)):
            if p[4].expr_type_list[i] != scope_table[curr_scope].table[p[1].ident_list[i]]["type"]:
                errors.add_error("Type Error", line_number.get() +
                                 1, "Type mismatch in assignment")

        for i in range(0, len(p[1].ident_list)):
            temp = [scope_table[curr_scope].table[p[1].ident_list[i]]["tmp"], "="]
            if(p[4].data["dereflist"][i] == 1):
                temp.append("*")
            temp.append(p[4].expr_list[i])
            p[0].code.append(temp)
    elif(len(p) == 4):
        p[0].code = p[1].code+p[3].code
        p[0].ast = ["=", p[1].ast, p[3].ast]
        if len(p[1].ident_list) != len(p[3].expr_list):
            errors.add_error("Imbalaced assignment", line_number.get(
            )+1, "Identifier and Expression list length is not equal")
        for i in range(0, len(p[1].ident_list)):
            if checker.check_ident(scope_table, curr_scope, scope_list, p[1].ident_list[i], 'redeclaration') == True:
                errors.add_error("Redeclaration error", line_number.get(
                )+1, "Redeclaration of variable " + p[1].ident_list)
            else:
                var1 = create_temp(1)
                scope_table[curr_scope].insert(
                    p[1].ident_list[i], p[3].expr_type_list[i])
                scope_table[curr_scope].insert(var1, p[1].ident_list[i])
                scope_table[curr_scope].update(p[1].ident_list[i], "tmp", var1)
                scope_table[curr_scope].update(
                    p[1].ident_list[i], "offset", offset_list[curr_func_scope])
                offset_list[curr_func_scope] += scope_table[curr_scope].type_size_list[p[3].expr_type_list[i][0]]
                scope_table[curr_scope].update(
                    p[1].ident_list[i], 'constant', True)
        for i in range(0, len(p[1].ident_list)):
            if p[3].expr_type_list[i] != scope_table[curr_scope].table[p[1].ident_list[i]]["type"]:
                errors.add_error("Type Error", line_number.get() +
                                 1, "Type mismatch in assignment")
        for i in range(0, len(p[1].ident_list)):
            temp = [scope_table[curr_scope].table[p[1].ident_list[i]]["tmp"], "="]
            if(p[3].data["dereflist"][i] == 1):
                temp.append("*")
            temp.append(p[3].expr_list[i])
            p[0].code.append(temp)


def p_identifier_list(p):
    '''IdentifierList : IDENT
    | IDENT COMMA IdentifierList'''
    p[0] = Node('IdentifierList')
    if(len(p) == 2):
        p[0].ast = [p[1]]
        p[0].ident_list.append(p[1])
    else:
        p[0].ast = ["IdentifierList", [p[1]], p[3].ast]
        p[0].ident_list.append(p[1])
        p[0].ident_list = p[0].ident_list + p[3].ident_list


def p_expression_list(p):
    '''ExpressionList : Expression
    | ExpressionList COMMA Expression
    | LEFT_BRACKET Expression RIGHT_BRACKET IDENT LEFT_BRACE ExpressionList RIGHT_BRACE'''
    p[0] = Node('ExpressionList')
    # print("hello")
    if len(p) == 2:
        p[0].expr_type_list += p[1].expr_type_list
        p[0].code = p[1].code
        p[0].ast = p[1].ast
        p[0].data["dereflist"] = []
        if p[1].data.get("deref") is None:
            p[0].expr_list += p[1].expr_list
            for i in range(0, len(p[1].expr_list)):
                p[0].data["dereflist"].append(0)
        else:
            p[0].expr_list += p[1].expr_list
            p[0].data["dereflist"] = [1]
        if p[1].data.get("memory"):
            p[0].data["memory"] = 1
        else:
            p[0].data["memory"] = 0
    elif (len(p) == 8):
        print("hello1")
        # p[0].expr_type_list=["array"]

    else:
        p[0].ast = ["ExpressionList", p[1].ast, p[3].ast]
        p[0].expr_type_list += p[1].expr_type_list
        p[0].expr_type_list += p[3].expr_type_list
        p[0].expr_list += p[1].expr_list
        p[0].data["dereflist"] = p[1].data["dereflist"]
        if p[3].data.get("deref") is None:
            p[0].expr_list += p[3].expr_list
            for i in range(0, len(p[3].expr_list)):
                p[0].data["dereflist"].append(0)
        else:
            p[0].expr_list += p[3].expr_list
            p[0].data["dereflist"].append(1)
        p[0].code = p[1].code + p[3].code
        if p[1].data["memory"] == 1 and p[3].data["memory"] == 1:
            p[0].data["memory"] = 1
        else:
            p[0].data["memory"] = 0


def p_var_decl(p):
    '''VarDecl : VARIABLE VarSpec
    | VARIABLE LEFT_PARENTHESIS VarSpecStar RIGHT_PARENTHESIS'''
    p[0] = Node("Vardecl")

    if len(p) == 3:
        p[0] = p[2]
        p[0].ast = p[2].ast
        # print(p[2].ast)
    else:
        p[0] = p[3]
        # print(p[2].ast)
    # print(p[0].ast)


def p_var_spec_star(p):
    '''VarSpecStar : VarSpec SEMICOLON VarSpecStar
    |'''
    p[0] = Node('VarSpecStar')
    if len(p) > 1:
        p[0].ast = ["Varspecstar", p[1].ast, p[3].ast]
        # print("Helloworld")
        # print(p[0].ast)
        p[0].code += p[1].code
        # p[0].code += p[3].code


def p_var_spec(p):
    '''VarSpec : IdentifierList Type 
                | IdentifierList Type ASSIGNMENT ExpressionList
                | IdentifierList IDENT ASSIGNMENT ExpressionList
                | IdentifierList IDENT
                | IdentifierList ASSIGNMENT ExpressionList'''
    p[0] = Node('VarSpec')
    if(len(p) == 3 and isinstance(p[2], str)):
        p[0].ast = ["VarSpec", p[1].ast, [p[2]]]
    elif (len(p) == 3):
        p[0].ast = ["VarSpec", p[1].ast, p[2].ast]
    elif (len(p) == 4):
        p[0].ast = ["VarSpec Assignment", p[1].ast, p[3].ast]
    elif (len(p) == 5 and isinstance(p[2], str)):

        p[0].ast = ["VarSpec Assignment", p[1].ast, [p[2]], p[4].ast]
    else:
        p[0].ast = ["VarSpec Assignment", p[1].ast, p[2].ast, p[4].ast]

    if len(p) == 5:
        for i in range(0, len(p[4].expr_type_list)):
            if(not (p[4].expr_type_list[i][0] in basic_types_list or p[4].expr_type_list[i][0] == "pointer")):
                errors.add_error('Type Error', line_number.get()+1,
                                 'Invalid Assignment')

    if(isinstance(p[2], str) and p[2] != "=" and not p[2] in scope_table[curr_scope].type_list):
        errors.add_error('Type Error', line_number.get() +
                         1, 'Invalid type of identifier')

    if len(p) == 5 or len(p) == 3:
        for x in p[1].ident_list:
            if checker.check_ident(scope_table, curr_scope, scope_list, x, 'redeclaration') == True and x != "_":
                errors.add_error('Redeclaration Error', line_number.get(
                )+1, 'Redeclaration of identifier:'+x)
            else:
                if(isinstance(p[2], str)):
                    var1 = create_temp(1)
                    scope_table[curr_scope].insert(x, [p[2]])
                    scope_table[curr_scope].insert(var1, x)
                    scope_table[curr_scope].update(x, "tmp", var1)
                    scope_table[curr_scope].update(
                        x, "offset", offset_list[curr_func_scope])
                    offset_list[curr_func_scope] += scope_table[curr_scope].type_size_list[p[2]]
                else:
                    var1 = create_temp(1)
                    scope_table[curr_scope].insert(x, p[2].type_list)
                    scope_table[curr_scope].insert(var1, x)
                    scope_table[curr_scope].update(x, "tmp", var1)
                    scope_table[curr_scope].update(
                        x, "offset", offset_list[curr_func_scope])
                    offset_list[curr_func_scope] += p[2].data["typesize"]

    if len(p) == 5:
        if len(p[1].ident_list) != len(p[4].expr_type_list):
            errors.add_error('Assignment Error', line_number.get()+1,
                             "Imbalanced assignment")
        for i in range(0, len(p[1].ident_list)):
            if(p[4].expr_type_list[i] != scope_table[curr_scope].table[p[1].ident_list[i]]["type"]):
                if not ((p[4].expr_type_list[i] == ['int'] and scope_table[curr_scope].table[p[1].ident_list[i]]["type"] == ["float"])):
                    # print(p[4].expr_type_list[i],
                    #       scope_table[curr_scope].table[p[1].ident_list[i]]["type"], p[4].expr_type_list[i] == 'int')
                    errors.add_error('Type Error', line_number.get(
                    )+1, "Mismatch of type for "+p[1].ident_list[i])
        p[0].code = p[1].code+p[4].code
        for i in range(0, len(p[1].ident_list)):
            temp = [scope_table[curr_scope].table[p[1].ident_list[i]]["tmp"], "="]
            if(p[4].data["dereflist"][i] == 1):
                temp.append("*")
            temp.append(p[4].expr_list[i])
            p[0].code.append(temp)

    if len(p) == 4:

        if(len(p[1].ident_list) != len(p[3].expr_type_list)):
            errors.add_error('Assignment Error', line_number.get()+1,
                             "Imbalanced Assignment")
        for i in range(0, len(p[1].ident_list)):
            if len(p[3].expr_type_list[i]) > 1:
                errors.add_error('Assignment Error', line_number.get(
                )+1, "Auto assignment of complex expressions not allowed")
            if not p[3].expr_type_list[i][0] in basic_types_list:
                errors.add_error('Assignment Error', line_number.get(
                )+1, "Auto assignment of only basic types allowed")
            if checker.check_ident(scope_table, curr_scope, scope_list, p[1].ident_list[i], 'redeclaration') is True and p[1].ident_list[i] != "_":
                errors.add_error('Redeclaration Error', line_number.get(
                )+1, 'Redeclaration of identifier: '+p[1].ident_list[i])
            var1 = create_temp(1)
            scope_table[curr_scope].insert(
                p[1].ident_list[i], p[3].expr_type_list[i])

            scope_table[curr_scope].insert(var1, p[1].ident_list[i])
            scope_table[curr_scope].update(p[1].ident_list[i], "tmp", var1)
            scope_table[curr_scope].update(
                p[1].ident_list[i], "offset", offset_list[curr_func_scope])
            offset_list[curr_func_scope] += scope_table[curr_scope].type_size_list[p[3].expr_type_list[i][0]]
            p[0].code = p[1].code+p[3].code
        for i in range(0, len(p[1].ident_list)):
            temp = [
                scope_table[curr_scope].table[p[1].ident_list[i]]["tmp"], "="]
            if(p[3].data["dereflist"][i] == 1):
                temp.append("*")
            temp.append(p[3].expr_list[i])
            p[0].code.append(temp)


def p_short_var_decl(p):
    '''ShortVarDecl : IdentifierList DEFINE ExpressionList'''

    if(len(p[1].ident_list) != len(p[3].expr_type_list)):
        errors.add_error('Assignment Error', line_number.get()+1,
                         "Imbalanced Assignment")
    for i in range(0, len(p[1].ident_list)):
        if len(p[3].expr_type_list[i]) > 1:
            errors.add_error('Assignment Error', line_number.get(
            )+1, "Auto assignment of complex expressions not allowed")
        if not p[3].expr_type_list[i][0] in basic_types_list:
            errors.add_error('Assignment Error', line_number.get(
            )+1, "Auto assignment of only basic types allowed")
        if checker.check_ident(scope_table, curr_scope, scope_list, p[1].ident_list[i], 'redeclaration') is True and p[1].ident_list[i] != "_":
            errors.add_error('Assignment Error', line_number.get(
            )+1, 'Redeclaration of identifier:'+p[1].ident_list[i])
        var1 = create_temp(1)
        scope_table[curr_scope].insert(
            p[1].ident_list[i], p[3].expr_type_list[i])
        scope_table[curr_scope].insert(var1, p[1].ident_list[i])
        scope_table[curr_scope].update(p[1].ident_list[i], "tmp", var1)
        scope_table[curr_scope].update(
            p[1].ident_list[i], "offset", offset_list[curr_func_scope])
        offset_list[curr_func_scope] += scope_table[curr_scope].type_size_list[p[3].expr_type_list[i][0]]
    p[0] = Node('ShortVarDecl')
    p[0].ast = [":=", p[1].ast, p[3].ast]
    p[0].code = p[3].code
    for i in range(0, len(p[1].ident_list)):
        temp = [scope_table[curr_scope].table[p[1].ident_list[i]]["tmp"], "="]
        if(p[3].data["dereflist"][i] == 1):
            temp.append("*")
        temp.append(p[3].expr_list[i])
        p[0].code.append(temp)
    p[0].expr_type_list = []


def p_open_base(p):
    '''OpenBase : '''
    global curr_func_scope, scope_number
    curr_func_scope = scope_number + 1


def p_close_base(p):
    '''CloseBase : '''
    scope_table[curr_scope].insert("total_size", offset_list[curr_func_scope])


def p_function_decl(p):
    '''FunctionDecl : FUNCTION OpenBase FunctionName OpenScope Signature Block CloseBase CloseScope 
                    | FUNCTION OpenBase FunctionName OpenScope Signature CloseBase CloseScope'''

    p[0] = Node('FunctionDecl')
    if(len(p) == 8):
        p[0].ast = ["FUNCTION", p[3].ast, p[5].ast]
    else:
        p[0].ast = ["FUNCTION", p[3].ast, p[5].ast, p[6].ast]
    p[0].code = p[3].code
    p[0].code += p[5].code
    if len(p) != 8:
        p[0].code += p[6].code
    p[0].code.append(["return"])


def p_function_name(p):
    """
    FunctionName : IDENT
    """
    p[0] = Node('FunctionName')
    p[0].ast = [p[1]]
    global curr_func
    if checker.check_ident(scope_table, curr_scope, scope_list, p[1], 'redeclaration') == True:
        errors.add_error("Redecleration error", line_number.get() +
                         1, p[1]+" is redeclared")
    scope_table[0].insert(p[1], ["func"])
    scope_table[0].update(p[1], "scope", curr_func_scope)
    p[0].code.append([p[1], ":"])
    curr_func = p[1]

# --------------------- TYPES -------------------------------------


def p_type(p):
    '''Type : LEFT_PARENTHESIS IDENT RIGHT_PARENTHESIS
    | TypeLit 
    | LEFT_PARENTHESIS Type RIGHT_PARENTHESIS'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if isinstance(p[2], str) and not p[2] in scope_table[curr_scope].type_list:
            errors.add_error('Type Error', line_number.get()+1,
                             "Invalid type of identifier "+p[2])
        if isinstance(p[2], str):
            p[0] = Node('Type')
            p[0].ast = [p[2]]
            p[0].type_list.append(p[2])
            p[0].data["typesize"] = scope_table[curr_scope].type_size_list[p[2]]
        else:
            p[0] = p[2]


def p_type_lit(p):
    '''TypeLit : ArrayType 
    | PointerType '''
    p[0] = p[1]


def p_array_type(p):
    '''ArrayType : LEFT_BRACKET INT RIGHT_BRACKET Type
                | LEFT_BRACKET INT RIGHT_BRACKET IDENT'''
    # | LEFT_BRACKET Expression RIGHT_BRACKET IDENT PERIOD IDENT'''
    if isinstance(p[4], str) and not p[4] in scope_table[curr_scope].type_list:
        errors.add_error('Type Error', line_number.get()+1,
                         "This type hasn't been declared yet "+p[4])
    temp = int(p[2])
    p[0] = Node('ArrayType')
    if isinstance(p[4], str):
        p[0].ast = ["ArrayType", [p[2]], [p[4]]]
        p[0].type_list.append("arr"+p[2])
        p[0].type_list.append(p[4])
        p[0].data["typesize"] = temp*scope_table[curr_scope].type_size_list[p[4]]
    else:
        p[0].ast = ["ArrayType", [p[2]], p[4].ast]
        p[0].type_list.append("arr"+p[2])
        p[0].type_list += p[4].type_list
        p[0].data["typesize"] = temp*p[4].data["typesize"]


def p_struct_type(p):
    '''StructType : STRUCT OpenStruct LEFT_BRACE FieldDeclStar RIGHT_BRACE CloseStruct'''
    p[0] = Node('StructType')
    p[0].code = p[4].code
    p[0].ast = ["STRUCT", p[4].ast]
# --------------------------------------------------------------------


def p_field_decl_star(p):
    '''FieldDeclStar : FieldDeclStar FieldDecl SEMICOLON
    |'''
    p[0] = Node('FieldDeclStar')
    if len(p) > 1:
        if(len(p[1].ast) > 0 and len(p[2].ast) > 0):
            p[0].ast = ['FieldDeclStar', p[1].ast, p[2].ast]
        elif(len(p[1].ast) > 0):
            p[0].ast = p[1].ast
        elif(len(p[2].ast) > 0):
            p[0].ast = p[2].ast
        else:
            p[0].ast = []
        p[0].code += p[1].code
        p[0].code += p[2].code


def p_field_decl(p):
    """FieldDecl : IDENT COMMA IdentifierList Type
              | IDENT COMMA IdentifierList IDENT
              | IDENT Type
              | IDENT IDENT
              | IDENT STRUCT MULTIPLY IDENT
              | IDENT COMMA IdentifierList STRUCT MULTIPLY IDENT"""
    p[0] = Node('FieldDecl')
    global struct_offset
    if len(p) == 3:
        if(isinstance(p[2], str)):
            p[0].ast = ["FieldDecl", [p[1]], [p[2]]]
            if(p[1] in struct_sym_list):
                errors.add_error('Redeclaration Error', line_number.get(
                )+1, "This identifier is already declared in this list")
            struct_sym_list.append(p[1])
            scope_table[curr_scope].update(curr_struct, p[1], [p[2]])
            scope_table[curr_scope].update(
                curr_struct, "offset "+p[1], struct_offset)
            struct_offset += scope_table[curr_scope].type_size_list[p[2]]
        else:
            p[0].ast = ["FieldDecl", [p[1]], p[2].ast]
            if(p[1] in struct_sym_list):
                errors.add_error('Redeclaration Error', line_number.get(
                )+1, "This identifier is already declared in this list")
            struct_sym_list.append(p[1])
            scope_table[curr_scope].update(curr_struct, p[1], p[2].type_list)
            scope_table[curr_scope].update(
                curr_struct, "offset "+p[1], struct_offset)
            struct_offset += p[2].data["typesize"]
    elif len(p) == 5 and not isinstance(p[3], str):
        if isinstance(p[4], str):
            p[0].ast = ["FieldDecl", [p[1]], p[3].ast, [p[4]]]
            if p[1] in struct_sym_list:
                errors.add_error('Redeclaration Error', line_number.get(
                )+1, "This identifier is already declared in this list")
            struct_sym_list.append(p[1])
            scope_table[curr_scope].update(curr_struct, p[1], [p[4]])
            scope_table[curr_scope].update(
                curr_struct, "offset "+p[1], struct_offset)
            struct_offset += scope_table[curr_scope].type_size_list[p[4]]
            for x in p[3].ident_list:
                if(x in struct_sym_list):
                    errors.add_error('Redeclaration Error', line_number.get(
                    )+1, "This identifier is already declared in this list")
                struct_sym_list.append(x)
                scope_table[curr_scope].update(curr_struct, x, [p[4]])
                scope_table[curr_scope].update(
                    curr_struct, "offset "+x, struct_offset)
                struct_offset += scope_table[curr_scope].type_size_list[p[4]]
        else:
            p[0].ast = ["FieldDecl", [p[1]], p[3].ast, p[4].ast]
            if(p[1] in struct_sym_list):
                errors.add_error('Redeclaration Error', line_number.get(
                )+1, "This identifier is already declared in this list")
            struct_sym_list.append(p[1])
            scope_table[curr_scope].update(curr_struct, p[1], p[4].type_list)
            scope_table[curr_scope].update(
                curr_struct, "offset "+p[1], structOff)
            struct_offset += p[4].data["typesize"]
            for x in p[3].ident_list:
                if x in struct_sym_list:
                    errors.add_error('Redeclaration Error', line_number.get(
                    )+1, "This identifier is already declared in this list")
                struct_sym_list.append(x)
                scope_table[curr_scope].update(curr_struct, x, p[4].type_list)
                scope_table[curr_scope].update(
                    curr_struct, "offset "+x, struct_offset)
                structOff += p[4].data["typesize"]
    elif len(p) == 5:
        p[0].ast = ["FieldDecl", [p[1]], "STRUCT", [p[3]], [p[4]]]
        if(p[4] != curr_struct):
            errors.add_error('Struct Error', line_number.get(
            )+1, "The identifier should be the current struct")
        struct_sym_list.append(p[1])
        scope_table[curr_scope].update(
            curr_struct, p[1], ["pointer", curr_struct])
        scope_table[curr_scope].update(
            curr_struct, "offset "+p[1], struct_offset)
        struct_offset += 4
    else:
        p[0].ast = ["FieldDecl", [p[1]], p[3].ast, "STRUCT", [p[5]], [p[6]]]
        if p[6] != curr_struct:
            errors.add_error('Struct Error', line_number.get(
            )+1, "The identifier should be the current struct")
        struct_sym_list.append(p[1])
        scope_table[curr_scope].update(
            curr_struct, p[1], ["pointer", curr_struct])
        for x in p[3].ident_list:
            if(x in struct_sym_list):
                errors.add_error('Redeclaration Error', line_number.get(
                )+1, "This identifier is already declared in this list")
            struct_sym_list.append(x)
            scope_table[curr_scope].update(
                curr_struct, x, ["pointer", curr_struct])
            scope_table[curr_scope].update(
                curr_struct, "offset "+x, struct_offset)
            struct_offset += 4


def p_pointer_type(p):
    '''PointerType : MULTIPLY Type
        | MULTIPLY IDENT'''
    if isinstance(p[2], str) and not p[2] in scope_table[curr_scope].type_list:
        errors.add_error('Type Error', line_number.get()+1,
                         "Invalid type of identifier "+p[2])
    p[0] = Node('PointerType')

    p[0].type_list.append("pointer")
    if isinstance(p[2], str):
        p[0].ast = ["*", [p[2]]]
        p[0].type_list.append(p[2])
        p[0].data["typesize"] = 4
    else:
        p[0].ast = ["*", p[2].ast]
        p[0].type_list += p[2].type_list
        p[0].data["typesize"] = 4


def p_signature(p):
    '''Signature : Parameters Result'''
    p[0] = Node('Signature')
    p[0].ast = ["Parameters", p[1].ast, p[2].ast]


def p_result(p):
    '''Result : LEFT_PARENTHESIS TypeList RIGHT_PARENTHESIS 
    |'''
    p[0] = Node('Result')
    if len(p) == 1:

        scope_table[0].update(curr_func, 'return_type', [["void"]])
        scope_table[0].update(curr_func, 'total_return_size', 0)
        scope_table[0].update(curr_func, 'return_size_list', [])
    else:
        p[0].ast = ["Result", p[2].ast]
        scope_table[0].update(curr_func, 'return_type', p[2].ident_list)
        total_sum = -8 - scope_table[0].table[curr_func]["total_param_size"]
        return_list = []
        return_sum = 0
        for i in range(0, len(p[2].ident_list)):
            return_list.append(total_sum)
            total_sum -= p[2].expr_list[i]
            return_sum += p[2].expr_list[i]
        scope_table[0].update(curr_func, "total_return_size", return_sum)
        scope_table[0].update(curr_func, "return_size_list", return_list)


def p_TypeList(p):
    """TypeList : TypeList COMMA IDENT
    | TypeList COMMA Type 
    | IDENT
    | Type"""
    if(isinstance(p[1], str) and not p[1] in scope_table[curr_scope].type_list):
        errors.add_error("Return Error",line_number.get()+1, "Invalid return type")
    if len(p) == 4 and isinstance(p[3], str) and not p[3] in scope_table[curr_scope].type_list:
        errors.add_error("Return Error",line_number.get()+1, "Invalid return type")
    p[0] = Node('TypeList')
    if(len(p) == 2):
        if(isinstance(p[1], str)):
            p[0].ast = [p[1]]
            p[0].ident_list.append([p[1]])
            p[0].expr_list.append(scope_table[curr_scope].type_size_list[p[1]])
        else:
            p[0].ast = p[1].ast
            p[0].ident_list.append(p[1].type_list)
            p[0].expr_list.append(p[1].data["typesize"])
    else:
        if(isinstance(p[3], str)):
            p[0].ast = ["TypeList", p[1].ast, [p[3]]]
            p[0].ident_list = p[1].ident_list
            p[0].expr_list = p[1].expr_list
            p[0].ident_list.append([p[3]])
            p[0].expr_list.append(scope_table[curr_scope].type_size_list[p[3]])
        else:
            p[0].ast = ["TypeList", p[1].ast, p[3].ast]
            p[0].ident_lList = p[1].ident_list
            p[0].expr_list = p[1].expr_list
            p[0].ident_list.append(p[3].type_list)
            p[0].expr_list.append(p[3].data["typesize"])


def p_parameters(p):
    '''Parameters : LEFT_PARENTHESIS RIGHT_PARENTHESIS
                | LEFT_PARENTHESIS ParameterList RIGHT_PARENTHESIS
                | LEFT_PARENTHESIS ParameterList COMMA RIGHT_PARENTHESIS'''
    p[0] = Node('Paramters')
    if(len(p) == 3):
        scope_table[0].update(curr_func, "accepts", [["void"]])
        scope_table[0].update(curr_func, "total_param_size", 0)
    else:
        p[0].ast = p[2].ast
        scope_table[0].update(curr_func, "accepts", p[2].expr_type_list)
        arg_offset = -8
        param_sum = 0
        param_list = []
        n = len(p[2].ident_list)
        for i in range(0, n):
            scope_table[curr_scope].update(
                p[2].ident_list[n-i-1], "offset", arg_offset)
            param_list.append(p[2].expr_list[i])
            arg_offset -= p[2].expr_list[n-i-1]
            param_sum += p[2].expr_list[i]
        scope_table[0].update(curr_func, "total_param_size", param_sum)
        scope_table[0].update(curr_func, "param_size_list", param_list)


def p_parameter_list(p):
    '''ParameterList : ParameterDecl 
    | ParameterList COMMA ParameterDecl'''
    p[0] = Node('ParameterList')
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0].ast = ["ParameterList", p[1].ast, p[3].ast]
        p[0].ident_list = p[1].ident_list
        p[0].ident_list += (p[3].ident_list)
        p[0].expr_type_list = p[1].expr_type_list
        p[0].expr_type_list += (p[3].expr_type_list)
        p[0].expr_list = p[1].expr_list
        p[0].expr_list += (p[3].expr_list)


def p_ParameterDecl(p):
    """ParameterDecl : ParaIdentList Type
    | ParaIdentList IDENT
    | IDENT IDENT
    | IDENT Type"""
    if isinstance(p[2], str) and not p[2] in scope_table[curr_scope].type_list:
        errors.add_error("Type Error", line_number.get()+1,
                         "Invalid type of identifier "+p[2])

    p[0] = Node('ParameterDecl')
    flag = 0
    if not isinstance(p[1], str):
        p[0].ident_list = p[1].ident_list
        for x in p[1].ident_list:
            if checker.check_ident(scope_table, curr_scope, scope_list, x, 'redeclaration') == True and x != "_":
                errors.add_error("Redeclaration Error", line_number.get()+1,"Redeclaration of identifier "+x)
            else:
                if(isinstance(p[2], str)):
                    p[0].ast = ["ParameterDecl", p[1].ast, [p[2]]]
                    var1 = create_temp(1)
                    scope_table[curr_scope].insert(x, [p[2]])
                    scope_table[curr_scope].insert(var1, x)
                    scope_table[curr_scope].update(x, "tmp", var1)
                    p[0].expr_type_list.append([p[2]])
                    p[0].expr_list.append(
                        scope_table[curr_scope].type_size_list[p[2]])
                else:
                    p[0].ast = ["ParameterDecl", p[1].ast, p[2].ast]
                    var1 = create_temp(1)
                    scope_table[curr_scope].insert(x, p[2].type_list)
                    scope_table[curr_scope].insert(var1, x)
                    scope_table[curr_scope].update(x, "tmp", var1)
                    p[0].expr_type_list.append(p[2].type_list)
                    p[0].expr_list.append(p[2].data["typesize"])
    else:
        if checker.check_ident(scope_table, curr_scope, scope_list, p[1], 'redeclaration') == True and p[1] != "_":
            errors.add_error("Redeclaration Error", line_number.get()+1,
                             "Redeclaration of identifier "+p[1])
        else:
            p[0].ident_list = [p[1]]
            if(isinstance(p[2], str)):
                p[0].ast = ["ParameterDecl", [p[1]], [p[2]]]
                var1 = create_temp(1)
                scope_table[curr_scope].insert(p[1], [p[2]])
                scope_table[curr_scope].insert(var1, p[1])
                scope_table[curr_scope].update(p[1], "tmp", var1)
                p[0].expr_type_list.append([p[2]])
                p[0].expr_list.append(
                    scope_table[curr_scope].type_size_list[p[2]])
            else:
                p[0].ast = ["ParameterDecl", [p[1]], p[2].ast]
                var1 = create_temp(1)
                scope_table[curr_scope].insert(p[1], p[2].type_list)
                scope_table[curr_scope].insert(var1, p[1])
                scope_table[curr_scope].update(p[1], "tmp", var1)
                p[0].expr_type_list.append(p[2].type_list)
                p[0].expr_list.append(p[2].data["typesize"])


def p_ParaIdentList(p):
    """
    ParaIdentList : IDENT COMMA IDENT
               | ParaIdentList COMMA IDENT
    """
    p[0] = Node('ParaIdentList')

    if(isinstance(p[1], str)):
        p[0].ast = ["ParaIdentList", [p[1]], [p[3]]]
        p[0].ident_list.append(p[1])
        p[0].ident_list.append(p[3])
    else:
        p[0].ast = ["ParaIdentList", p[1].ast, [p[3]]]
        p[0].ident_list = p[1].ident_list
        p[0].ident_list.append(p[3])

# --------------------------------------------------------------------


def p_block(p):
    '''Block : LEFT_BRACE StatementList RIGHT_BRACE'''
    p[0] = p[2]


def p_statement_list(p):
    '''StatementList : StatementList Statement SEMICOLON
    |'''
    p[0] = Node('StatementList')
    if len(p) > 1:
        if(len(p[1].ast) > 0 and len(p[2].ast) > 0):
            p[0].ast = ['StatementList', p[1].ast, p[2].ast]
        elif(len(p[1].ast) > 0):
            p[0].ast = p[1].ast
        elif(len(p[2].ast) > 0):
            p[0].ast = p[2].ast
        else:
            p[0].ast = []
        p[0].code = p[1].code + p[2].code
        if(p[1].data.get("hasReturnStmt") != None or p[2].data.get("hasReturnStmt") != None):
            p[0].data["hasReturnStmt"] = 1
#############################


def p_expression(p):
    '''Expression : UnaryExpr 
    | Expression LOGICAL_OR Expression
    | Expression LOGICAL_AND Expression
    | Expression EQUAL Expression
    | Expression NOT_EQUAL Expression
    | Expression LESS_THAN Expression
    | Expression LESS_THAN_EQUAL Expression
    | Expression GREATER_THAN Expression
    | Expression GREATER_THAN_EQUAL Expression
    | Expression ADD Expression
    | Expression SUBTRACT Expression
    | Expression OR Expression
    | Expression XOR Expression
    | Expression MULTIPLY Expression
    | Expression QUOTIENT Expression
    | Expression REMAINDER Expression
    | Expression SHIFT_LEFT Expression
    | Expression SHIFT_RIGHT Expression
    | Expression AND Expression
    | Expression AND_NOT Expression'''
    if len(p) == 2:
        p[0] = Node('Expression')
        p[0] = p[1]
    else:
        p[0] = Node('Expression')
        p[0].ast = [p[2], p[1].ast, p[3].ast]
        if len(p[1].expr_type_list) > 1 or len(p[3].expr_type_list) > 1:
            errors.add_error("Operation Error", line_number.get(
            )+1, "Can't apply binary operators to multiple values")
        if checker.check_operation(p[1].expr_type_list[0], p[2], p[3].expr_type_list[0]) is None:
            errors.add_error("Operation Error", line_number.get()+1,
                             "Invalid types for operator")
        p[0].code = p[1].code+p[3].code
        # print(p[1].code)
        if p[1].data.get("deref") is not None:
            var1 = create_temp()
            scope_table[curr_scope].table[var1]["offset"] = offset_list[curr_func_scope]
            offset_list[curr_func_scope] += 4
            # print('A')
            p[0].code.append([var1, "=", "*", p[1].expr_list[0]])
        else:
            var1 = p[1].expr_list[0]
        if p[3].data.get("deref") is not None:
            var2 = create_temp()
            scope_table[curr_scope].table[var2]["offset"] = offset_list[curr_func_scope]
            offset_list[curr_func_scope] += 4
            # print('B')
            p[0].code.append([var2, "=", "*", p[3].expr_list[0]])
        else:
            var2 = p[3].expr_list[0]
        p[0].expr_type_list.append(checker.check_operation(
            p[1].expr_type_list[0], [p[2]], p[3].expr_type_list[0]))
        p[0].data["memory"] = 0
        var3 = create_temp()
        scope_table[curr_scope].table[var3]["offset"] = offset_list[curr_func_scope]
        offset_list[curr_func_scope] += 4
        # print('C')
        p[0].expr_list = [var3]
        p[0].code.append(
            [var3, "=", var1, p[2]+p[3].expr_type_list[0][0], var2])


def p_unary_expr(p):
    '''UnaryExpr : PrimaryExpr 
    | unary_op UnaryExpr'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node('UnaryExp')
        p[0].ast = [p[1].ast, p[2].ast]
        if len(p[1].expr_type_list) > 1:
            errors.add_error("Operation Error", line_number.get(
            )+1, "Can't apply binary operators to multiple values")
        if checker.check_unary_operation(p[1].expr_type_list[0], p[2].expr_type_list[0]) is None:
            errors.add_error("Operation Error", line_number.get()+1,
                             "Invalid types for operator")
        p[0].expr_type_list.append(checker.check_unary_operation(
            p[1].expr_type_list[0], p[2].expr_type_list[0]))

        p[0].code = p[2].code
        if p[1].expr_type_list[0][0] == "*":
            p[0].data["memory"] = 1
            p[0].data["deref"] = 1
            # var1 = create_temp()
            # p[0].code.append([var1, "=", "*", p[2].expr_list[0]])
            p[0].expr_list = [p[2].expr_list[0]]
        elif p[1].expr_type_list[0][0] == "&":
            p[0].data["memory"] = 0
            if p[2].data.get("deref") is None:
                if p[2].data["memory"] == 0:
                    errors.add_error(
                        'Address Error', line_number.get()+1, "Can't get address")
                var1 = create_temp()
                scope_table[curr_scope].table[var1]["offset"] = offset_list[curr_func_scope]
                offset_list[curr_func_scope] += 4
                p[0].code.append([var1, "=", "&", p[2].expr_list[0]])
                p[0].expr_list = [var1]
            else:
                p[0].expr_list = p[2].expr_list
        else:
            p[0].data["memory"] = 0
            var1 = create_temp()
            scope_table[curr_scope].table[var1]["offset"] = offset_list[curr_func_scope]
            offset_list[curr_func_scope] += 4
            p[0].expr_list = [var1]
            if p[1].expr_type_list[0][0] == '+' or p[1].expr_type_list[0][0] == '-':
                p[0].code.append([var1, "=", p[1].expr_type_list[0]
                                 [0]+p[2].expr_type_list[0][0], p[2].expr_list[0]])
            else:
                p[0].code.append(
                    [var1, "=", p[1].expr_type_list[0][0], p[2].expr_list[0]])


def p_unary_op(p):
    '''unary_op : ADD 
    | SUBTRACT 
    | NOT 
    | XOR 
    | MULTIPLY 
    | AND 
    | ARROW'''
    p[0] = Node('UnaryOp')
    p[0].expr_type_list.append([p[1]])
    p[0].ast = p[1]


def p_primary_expr(p):
    '''PrimaryExpr : IDENT
    | LEFT_PARENTHESIS Expression RIGHT_PARENTHESIS
    | Literal
    | PrimaryExpr Index
    | PrimaryExpr PERIOD IDENT 
    | PrimaryExpr Arguments'''
    if len(p) == 2 and not isinstance(p[1], str):
        p[0] = p[1]
        p[0].data["memory"] = 0
        p[0].expr_list = p[1].expr_list

    elif len(p) == 2:
        if checker.check_ident(scope_table, curr_scope, scope_list, p[1], "check_declaration") == False:
            errors.add_error("Undeclared Error", line_number.get() +
                             1, "Variable "+p[1]+" is not declared")
        p[0] = Node('PrimaryExpr')
        p[0].ast = [p[1]]
        p[0].expr_type_list.append(scope_table[checker.check_ident(
            scope_table, curr_scope, scope_list, p[1], "check_declaration") - 1].table[p[1]]["type"])
        p[0].data["memory"] = 1
        p[0].data["isID"] = p[1]
        x = checker.check_ident(scope_table, curr_scope,
                                scope_list, p[1], 'check_declaration') - 1
        temp1 = scope_table[x].table[p[1]]["type"]
        if(temp1 != ["func"]):
            p[0].expr_list = [scope_table[checker.check_ident(
                scope_table, curr_scope, scope_list, p[1], 'check_declaration') - 1].table[p[1]]["tmp"]]
        else:
            p[0].expr_list = ["func"]
        if scope_table[x].table.get(temp1[0]) != None:
            if(scope_table[x].table[temp1[0]]["type"] == ["struct"]):
                var1 = create_temp()
                scope_table[curr_scope].table[var1]["offset"] = offset_list[curr_func_scope]
                offset_list[curr_func_scope] += 4
                p[0].code.append([var1, "=", "&", scope_table[checker.check_ident(scope_table, curr_scope, scope_list,
                                                                                  p[1], 'check_declaration')].table[p[1]]["tmp"]])
                p[0].data["deref"] = 1
                p[0].expr_list = [var1]
        elif temp1[0][0:3] == "arr" or temp1[0] == "pointer":
            p[0].data["deref"] = 1

    elif(len(p) == 4 and p[2] == '.'):

        temp = p[1].expr_type_list[0][0]
        if(scope_table[curr_scope].table.get(temp) != None and scope_table[curr_scope].table[temp]["type"] == ["struct"]):
            if(scope_table[curr_scope].table[temp].get(p[3]) == None):
                errors.add_error("Struct Error", line_number.get(
                )+1, "No such attribute of given struct")
            p[0] = Node('PrimaryExpr')
            p[0].ast = [p[2], p[1].ast, [p[3]]]
            p[0].expr_type_list.append(
                scope_table[curr_scope].table[temp][p[3]])
            p[0].data["memory"] = 1
            p[0].code = p[1].code
            var1 = create_temp()
            scope_table[curr_scope].table[var1]["offset"] = offset_list[curr_func_scope]
            offset_list[curr_func_scope] += 4
            off = scope_table[curr_scope].table[p[1].expr_type_list[0]
                                                [0]]["offset "+p[3]]
            p[0].code.append([var1, "=", p[1].expr_list[0], '+int', off])
            p[0].data["deref"] = 1
            p[0].expr_list.append(var1)
        else:
            errors.add_error("Error", line_number.get()+1,
                             "The identifier is not declared or isn't a struct")

    elif(len(p) == 4):
        p[0] = p[2]

    elif p[2].data.get("index") is not None:
        if p[1].expr_type_list[0][0][0:3] != "arr":
            errors.add_error("Type Error", line_number.get()+1,
                             "The type of this expression is not an array")
        p[0] = p[1]
        p[0].ast = ["PrimaryExpr", p[1].ast, p[2].ast]
        p[0].code += p[2].code
        p[0].expr_type_list[0] = p[0].expr_type_list[0][1:]
        p[0].data["memory"] = 1
        p[0].data["deref"] = 1
        var1 = create_temp()
        scope_table[curr_scope].table[var1]["offset"] = offset_list[curr_func_scope]
        offset_list[curr_func_scope] += 4
        p[0].code.append([var1, "=", p[2].expr_list[0]])
        for i in range(0, len(p[0].expr_type_list[0])):
            if p[0].expr_type_list[0][i][0:3] == "arr":
                temp1 = int(p[0].expr_type_list[0][i][3:])
                p[0].code.append([var1, "=", var1, "*int", temp1])
            else:
                width = 0
                if p[0].expr_type_list[0][i] == "pointer":
                    width = 4
                else:
                    width = scope_table[curr_scope].type_size_list[p[0].expr_type_list[0][i]]
                p[0].code.append([var1, "=", var1, "*int", width])
                p[0].code.append([var1, "=", p[0].expr_list[0], '-arr_int', var1])
                break
        p[0].expr_list = [var1]

    elif p[2].data.get("arguments") is not None:
        if p[1].expr_type_list[0][0] != "func" or p[1].data.get("isID") is None:
            errors.add_error("Error", line_number.get()+1,
                             "The primary expression is not a function")
        if(p[2].expr_type_list != scope_table[0].table[p[1].data["isID"]]["accepts"]):
            errors.add_error("Error", line_number.get(
            )+1, "The arguments passed are not of the same type as the function")
        p[0] = Node('PrimaryExpr')
        p[0].ast = ['PrimaryExpr', p[1].ast, p[2].ast]
        p[0].expr_type_list = scope_table[0].table[p[1].data["isID"]]['return_type']
        if(p[0].expr_type_list[0][0] == "void"):
            p[0].expr_list = []
        else:
            for i in range(0, len(p[0].expr_type_list)):
                var1 = create_temp()
                scope_table[curr_scope].table[var1]["offset"] = offset_list[curr_func_scope]
                offset_list[curr_func_scope] += 4
                p[0].expr_list.append(var1)
        p[0].data["multi_return"] = 1
        p[0].data["memory"] = 0
        p[0].code = p[2].code
        # p[0].code.append(["startf", p[1].data["isID"]])
        for i in range(0, len(p[2].expr_list)):
            if(p[2].data["dereflist"][i] == 1):
                # var1 = create_temp()
                # p[0].code.append([var1, "=", "*", p[2].expr_list[i]])
                # p[0].code.append(["param", var1])
                p[0].code.append(
                    ["param", p[2].expr_list[i], scope_table[0].table[p[1].data["isID"]]["param_size_list"][i]])
            else:
                p[0].code.append(["param", p[2].expr_list[i]])
        p[0].code.append(["call", p[1].data["isID"]])
        # p[0].code.append(["endf", p[1].data["isID"]])
        for i in range(0, len(p[2].expr_list)):
            p[0].code.append(["pop"])
        for i in range(0, len(p[0].expr_list)):
            p[0].code.append([p[0].expr_list[i], "=", "retval_"+str(i+1)])


def p_index(p):
    '''Index : LEFT_BRACKET Expression RIGHT_BRACKET'''
    if p[2].expr_type_list != [["int"]]:
        errors.add_error("Type Error", line_number.get()+1,
                         "The index expression is not of type int")
    # print("hello")
    p[0] = Node("Index")
    p[0] = p[2]
    p[0].ast = ["Index", p[2].ast]
    p[0].data["index"] = 1


def p_Arguments(p):
    """Arguments : LEFT_PARENTHESIS RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS ExpressionList RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS ExpressionList COMMA RIGHT_PARENTHESIS"""
    if len(p) == 3:
        p[0] = Node("Arguments")
        p[0].data["arguments"] = 1
        p[0].expr_type_list.append(["void"])
        p[0].ast = []
    else:
        # print("hello")
        p[0] = p[2]
        p[0].data["arguments"] = 1
        p[0].expr_type_list = p[2].expr_type_list
        p[0].ast = p[2].ast


def p_literal(p):
    '''Literal : BasicLit '''
    # | CompositeLit
    # | FunctionLit'''
    p[0] = p[1]


def p_basic_lit(p):
    '''BasicLit : IntLit 
    | FloatLit
    | RuneLit
    | StringLit
    | TrueFalseLit
    | ImaginaryLit'''
    p[0] = p[1]


def p_imaginary_lit(p):
    '''ImaginaryLit : IMAGINARY'''
    p[0] = Node('ImaginaryLit')
    p[0].expr_type_list.append(["imaginary"])
    p[0].expr_list.append(p[1])
    p[0].ast = [p[1]]


def p_true_false_lit(p):
    '''TrueFalseLit : TRUE
    | FALSE'''
    p[0] = Node('TrueFalseLit')
    p[0].expr_type_list.append(["bool"])
    p[0].expr_list.append(p[1])
    p[0].ast = [p[1]]


def p_int_lit(p):
    '''IntLit : INT'''
    p[0] = Node('IntLit')
    p[0].expr_type_list.append(["int"])
    p[0].expr_list.append(p[1])
    p[0].ast = [p[1]]


def p_float_lit(p):
    '''FloatLit : FLOAT'''
    p[0] = Node('FloatLit')
    p[0].expr_type_list.append(["float"])
    p[0].expr_list.append(p[1])
    p[0].ast = [p[1]]


def p_rune_lit(p):
    '''RuneLit : RUNE'''
    p[0] = Node('RuneLit')
    p[0].expr_type_list.append(["rune"])
    p[0].expr_list.append(p[1])
    p[0].ast = [p[1]]


def p_string_lit(p):
    '''StringLit : STRING'''
    p[0] = Node('StringLit')
    p[0].expr_type_list.append(["string"])
    p[0].expr_list.append(p[1])
    p[0].ast = [p[1]]

# ----------------------------------------------------------


def p_statement(p):
    '''Statement : Declaration 
    | SimpleStmt 
    | ReturnStmt 
    | BreakStmt 
    | ContinueStmt 
    | OpenScope Block CloseScope 
    | IfStmt 
    | SwitchStmt 
    | ForStmt
    | PrintStmt
    | ScanStmt  '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_simple_stmt(p):
    '''SimpleStmt : Expression
    | IncDecStmt 
    | Assignment 
    | ShortVarDecl 
    |'''
    if len(p) > 1:
        p[0] = p[1]
    else:
        p[0] = Node('SimpleStmt')


def p_inc_dec_stmt(p):
    '''IncDecStmt : Expression INCREMENT
                    | Expression DECREMENT'''
    p[0] = p[1]
    if(p[2] == "++"):
        p[0].ast = ["++", p[1].ast]
    else:
        p[0].ast = ["--", p[1].ast]
    if p[0].expr_type_list != [["int"]]:
        errors.add_error("Type Error",
            line_number.get()+1, "Type Mismatch: Cannot increment/decrement non-integer value")
    if p[1].data["memory"] == 0:
        errors.add_error("Error",
            line_number.get()+1, "Cannot increment/decrement non-addressable value")
    if p[1].data.get("deref") == None:
        if p[2] == "++":
            p[0].code.append(
                [p[1].expr_list[0], "=", p[1].expr_list[0], '+int', 1])
        if p[2] == "--":
            p[0].code.append(
                [p[1].expr_list[0], "=", p[1].expr_list[0], '-int', 1])
    else:
        if p[2] == "++":
            var1 = create_temp()
            scope_table[curr_scope].table[var1]["offset"] = offset_list[curr_func_scope]
            offset_list[curr_func_scope] += 4
            p[0].code.append([var1, "=", "*", p[1].expr_list[0]])
            p[0].code.append([var1, "=", var1, '+int', 1])
            p[0].code.append(["*", p[1].expr_list[0], "=", var1])
        if(p[2] == "--"):
            var1 = create_temp()
            scope_table[curr_scope].table[var1]["offset"] = offset_list[curr_func_scope]
            offset_list[curr_func_scope] += 4
            p[0].code.append([var1, "=", "*", p[1].expr_list[0]])
            p[0].code.append([var1, "=", var1, '-int', 1])
            p[0].code.append(["*", p[1].expr_list[0], "=", var1])
    p[0].expr_type_list = []


def p_assignment(p):
    '''Assignment : ExpressionList assign_op ExpressionList'''
    p[0] = Node('Assignment')
    p[0].ast = [p[2].ast[0], p[1].ast, p[3].ast]
    for i in range(0, len(p[3].expr_type_list)):
        if(p[2].data["op"] == "="):
            if not (p[1].expr_type_list[i][0] in basic_types_list or p[1].expr_type_list[i][0] == "pointer"):
                errors.add_error('TypeError', line_number.get(
                )+1, "Type Mismatch: Cannot assign non-addressable value to addressable value")
        else:
            if(p[1].expr_type_list[i][0] not in basic_types_list):
                errors.add_error('TypeError', line_number.get()+1,
                                 "Invalid Assignment")
    if p[1].data["memory"] == 0:
        errors.add_error('Type Error', line_number.get()+1,
                         'Assignment not allowed for this expression list')
    if len(p[1].expr_type_list) != len(p[3].expr_type_list):
        errors.add_error('Assignment Error', line_number.get() +
                         1, 'Imbalanced assignment')

    for i in range(0, len(p[1].expr_type_list)):
        if p[1].expr_type_list[i] != p[3].expr_type_list[i]:
            if not (p[1].expr_type_list[i] == ["float"] and p[3].expr_type_list[i] == ["int"]):
                errors.add_error('Type Error', line_number.get()+1, "Mismatch of type for " +
                                 str(p[1].expr_type_list[i])+" and " + str(p[3].expr_type_list[i]))
    p[0].code += p[1].code + p[3].code
    for i in range(0, len(p[1].expr_type_list)):
        temp = None
        if p[2].expr_type_list[0][0] != "=":
            temp = checker.check_operation(p[1].expr_type_list[i], [
                p[2].expr_type_list[0][0][0:-1]], p[3].expr_type_list[i])
            if(temp == None):
                errors.add_error('Type Error', line_number.get()+1,
                                 "Invalid operation")
        if temp != None:
            p[2].expr_type_list[0] = [p[2].expr_type_list[0][0]+temp[0]]
        if p[1].data["dereflist"][i] == 1:
            if p[3].data["dereflist"][i] == 1:
                var1 = create_temp()
                scope_table[curr_scope].table[var1]["offset"] = offset_list[curr_func_scope]
                offset_list[curr_func_scope] += 4
                p[0].code.append([var1, "=", "*", p[3].expr_list[i]])
                p[0].code.append(
                    ["*", p[1].expr_list[i], p[2].expr_type_list[0][0], var1])
            else:
                p[0].code.append(["*", p[1].expr_list[i],
                                 p[2].expr_type_list[0][0], p[3].expr_list[i]])
        else:
            if(p[3].data["dereflist"][i] == 1):
                var1 = create_temp()
                scope_table[curr_scope].table[var1]["offset"] = offset_list[curr_func_scope]
                offset_list[curr_func_scope] += 4
                p[0].code.append([var1, "=", "*", p[3].expr_list[i]])
                p[0].code.append(
                    [p[1].expr_list[i], p[2].expr_type_list[0][0], var1])
            else:
                p[0].code.append(
                    [p[1].expr_list[i], p[2].expr_type_list[0][0], p[3].expr_list[i]])
    p[0].expr_type_list = []


def p_assign_op(p):
    '''assign_op : ADD_ASSIGNMENT
                | SUB_ASSIGNMENT
                | MUL_ASSIGNMENT
                | QUO_ASSIGNMENT
                | REM_ASSIGNMENT
                | AND_ASSIGNMENT
                | AND_NOT_ASSIGNMENT
                | OR_ASSIGNMENT
                | XOR_ASSIGNMENT
                | SHIFT_LEFT_ASSIGNMENT
                | SHIFT_RIGHT_ASSIGNMENT
                | ASSIGNMENT'''
    p[0] = Node('AssignOp')
    p[0].expr_type_list.append([p[1]])
    p[0].data["op"] = p[1]
    p[0].ast = [p[1]]


def p_if_stmt(p):
    '''IfStmt : IF OpenScope Expression Block CloseScope
    | IF OpenScope SimpleStmt SEMICOLON Expression Block CloseScope
    | IF OpenScope Expression Block CloseScope ELSE OpenScope IfStmt CloseScope
    | IF OpenScope Expression Block CloseScope ELSE OpenScope Block CloseScope
    | IF OpenScope SimpleStmt SEMICOLON Expression Block CloseScope ELSE OpenScope IfStmt CloseScope
    | IF OpenScope SimpleStmt SEMICOLON Expression Block CloseScope ELSE OpenScope Block CloseScope'''

    if len(p) == 6:
        if (p[3].expr_type_list[0][0] != "bool" and p[3].expr_type_list[0][0] != "int" and p[3].expr_type_list[0][0] != "float") or len(p[3].expr_type_list) > 1:
            errors.add_error('Type Error', line_number.get(
            )+1, "The type of expression in if is not (boolean/int/float)")
        p[0] = Node('IfStmt')
        p[0].ast = ["IF", p[3].ast, p[4].ast]
        p[0].code += p[3].code
        label = create_label()
        p[0].code.append(['ifnot', p[3].expr_list[0], 'goto', label])
        p[0].code += p[4].code
        p[0].code.append([label, ': '])

    elif len(p) == 8:
        if p[5].expr_type_list[0][0] != "bool" or len(p[5].expr_type_list) > 1:
            errors.add_error('Type Error', line_number.get()+1,
                             "The type of expression in if is not boolean")
        p[0] = Node('IfStmt')
        p[0].ast = ["IF", p[3].ast, p[5].ast, p[6].ast]
        p[0].code += p[3].code
        p[0].code += p[5].code
        label = create_label()
        p[0].code.append(['ifnot', p[5].expr_list[0], 'goto', label])
        p[0].code += p[6].code
        p[0].code.append([label, ': '])

    elif len(p) == 10:

        if p[3].expr_type_list[0][0] != "bool" or len(p[3].expr_type_list) > 1:
            errors.add_error('Type Error', line_number.get()+1,
                             "The type of expression in if is not boolean")
        p[0] = Node('IfStmt')
        p[0].ast = ["IF", p[3].ast, p[4].ast, p[8].ast]
        p[0].code += p[3].code
        label1 = create_label()
        label2 = create_label()
        p[0].code.append(['ifnot', p[3].expr_list[0], 'goto', label1])
        p[0].code += p[4].code
        p[0].code.append(['goto', label2])
        p[0].code.append([label1, ': '])
        p[0].code += p[8].code
        p[0].code.append([label2, ': '])

    else:
        if p[5].expr_type_list[0][0] != "bool" or len(p[5].expr_type_list) > 1:
            errors.add_error('Type Error', line_number.get()+1,
                             "The type of expression in if is not boolean")
        p[0] = Node('IfStmt')
        p[0].ast = ["IF", p[3].ast, p[5].ast, p[6].ast, p[9].ast]
        p[0].code += p[3].code
        p[0].code += p[5].code
        label1 = create_label()
        label2 = create_label()
        p[0].code.append(['ifnot', p[5].expr_list[0], 'goto', label1])
        p[0].code += p[6].code
        p[0].code.append(['goto', label2])
        p[0].code.append([label1, ': '])
        p[0].code += p[10].code
        p[0].code.append([label2, ': '])


def p_expr_switch_stmt(p):
    '''SwitchStmt : SWITCH LEFT_BRACE OpenSwitch ExprCaseClauseStar CloseSwitch RIGHT_BRACE
    | SWITCH SimpleStmt SEMICOLON LEFT_BRACE OpenSwitch ExprCaseClauseStar CloseSwitch RIGHT_BRACE
    | SWITCH SimpleStmt SEMICOLON ExpressionName LEFT_BRACE OpenSwitch ExprCaseClauseStar CloseSwitch RIGHT_BRACE
    | SWITCH ExpressionName LEFT_BRACE OpenSwitch ExprCaseClauseStar CloseSwitch RIGHT_BRACE'''
    p[0] = Node('ExprSwitchStmt')
    global curr_switch_type, end_for
    old_label = end_for[-1]
    label = create_label(2)
    print(end_for)
    if len(p) == 7:
        p[0].ast = ["SWITCH", p[4].ast]
        p[0].code += p[4].code
        p[0].code.append([old_label, ': '])
        if(p[4].data.get("hasReturnStmt") != None):
            p[0].data["hasRStmt"] = 1
    elif len(p) == 8:
        p[0].ast = ["SWITCH", p[2].ast, p[5].ast]
        p[0].code += p[2].code
        p[0].code += p[5].code
        p[0].code.append([old_label, ': '])
        if(p[5].data.get("hasReturnStmt") != None):
            p[0].data["hasRStmt"] = 1

    elif len(p) == 10:
        p[0].ast = ["SWITCH", p[2].ast, p[4].ast, p[7].ast]
        p[0].code += p[2].code
        p[0].code += p[4].code
        p[0].code += p[7].code
        p[0].code.append([old_label, ': '])
        if(p[7].data.get("hasReturnStmt") != None):
            p[0].data["hasRStmt"] = 1
    else:
        p[0].code += p[2].code
        p[0].code += p[6].code
        p[0].ast = ["SWITCH", p[2].ast, p[6].ast]
        p[0].code.append([old_label, ': '])
        if(p[6].data.get("hasReturnStmt") != None):
            p[0].data["hasRStmt"] = 1
    end_for = end_for[0: -1]


def p_ExpressionName(p):
    """ExpressionName : Expression"""
    p[0] = p[1]
    global switch_expr, curr_switch_type
    if len(p[1].expr_type_list) > 1:
        errors.add_error('Type Error', line_number.get()+1,
                         "The type of expression in switch is not a single type")
    if p[1].expr_type_list[0][0] != "int" and p[1].expr_type_list[0][0] != "rune" and p[1].expr_type_list[0][0] != "bool":
        errors.add_error('Type Error', line_number.get(
        )+1, "The type of expression in switch is not an integer, rune or boolean")
    curr_switch_type = p[1].expr_type_list[0][0]
    switch_expr = p[0].expr_list[0]
    label1 = create_label(2)


def p_expr_case_clause_star(p):
    '''ExprCaseClauseStar : ExprCaseClauseStar ExprCaseClause 
    | ExprCaseClause'''
    if len(p) > 2:
        p[0] = p[1]
        if(len(p[1].ast) > 0 and len(p[2].ast) > 0):
            p[0].ast = ['ExprCaseClauseStar', p[1].ast, p[2].ast]
        elif(len(p[1].ast) > 0):
            p[0].ast = p[1].ast
        elif(len(p[2].ast) > 0):
            p[0].ast = p[2].ast
        else:
            p[0].ast = []
        p[0].code += p[2].code
    else:
        p[0] = p[1]


def p_expr_case_clause(p):
    '''ExprCaseClause : OpenScope CASE Expression COLON StatementList CloseScope
    | DEFAULT COLON OpenScope StatementList CloseScope'''
    global switch_expr
    if len(p) == 6:
        p[0] = Node('DefClause')
        p[0].ast = ["DEFAULT", p[4].ast]
        p[0].code += p[4].code
    else:
        p[0] = Node('ExprCaseClause')
        p[0].ast = ["CASE", p[3].ast, p[5].ast]

        if p[3].expr_type_list[0][0] != "int" and p[3].expr_type_list[0][0] != "rune":
            errors.add_error('Type Error', line_number.get(
            )+1, "The type of expression in switch is not an integer or rune")
        if curr_switch_type is not None and curr_switch_type != p[3].expr_type_list[0][0]:
            errors.add_error('Type Error', line_number.get(
            )+1, "The type of expression in case does not match type of expression in switch")
        var = create_temp()
        scope_table[curr_scope].table[var]["offset"] = offset_list[curr_func_scope]
        offset_list[curr_func_scope] += 4
        label = create_label()
        p[0].code = p[3].code
        typ = 'big'
        for _, value in scope_table[curr_scope].table.items():
            if 'tmp' in value.keys() and value['tmp'] == switch_expr:
                typ = value['type'][0]
        p[0].code.append([var, '=', switch_expr, '=='+str(typ), p[3].expr_list[0]])
        p[0].code.append(['ifnot', var, 'goto', label])
        p[0].code += p[5].code
        p[0].code.append(['goto', end_for[-1]])
        p[0].code.append([label, ': '])


def p_print(p):
    '''PrintStmt : PRINT LEFT_PARENTHESIS ExpressionList RIGHT_PARENTHESIS'''
    p[0] = Node("Print")
    p[0] = p[3]
    for i in range(0, len(p[3].expr_list)):
        print(p[3].expr_list[i])
        p[0].code.append(
            ["print_" + str(p[3].expr_type_list[i][0]), p[3].expr_list[i]])


def p_scan(p):
    '''ScanStmt : SCAN LEFT_PARENTHESIS ExpressionList RIGHT_PARENTHESIS'''
    p[0] = Node("Scan")
    p[0] = p[3]
    for i in range(0, len(p[3].expr_list)):

        p[0].code.append(
            ["scan_" + str(p[3].expr_type_list[i][0]), p[3].expr_list[i]])
    # print(p[3].expr_list)
    # print(p[3].expr_type_list)


def p_for_stmt(p):
    '''ForStmt : FOR OpenScope OpenFor ForClause Block CloseFor CloseScope
    | FOR OpenScope OpenFor Expression Block CloseFor CloseScope
    | FOR OpenScope OpenFor Block CloseFor CloseScope'''

    global start_for, end_for
    p[0] = Node("ForStmt")
    p[0].code.append([start_for[-1], ': '])
    if len(p) == 8 and p[4].data.get("forclause") is not None:
        p[0].ast = ["FOR", p[4].ast, p[5].ast]
        p[0].code = p[4].code
        p[0].code += p[5].code
        p[0].code += p[4].data["for_label_pass"]
        if(p[5].data.get("hasReturnStmt") != None):
            p[0].data["hasReturnStmt"] = 1

    elif len(p) == 8:
        p[0].ast = ["FOR", p[4].ast, p[5].ast]
        if len(p[4].expr_type_list) > 1 or p[4].expr_type_list[0][0] != "bool":
            errors.add_error('Type Error', line_number.get(
            )+1, "The type of expression in for loop is not a boolean")
        label1 = create_label()
        label2 = create_label()
        p[0].code += p[4].code
        p[0].code.append([label2, ": "])
        p[0].code.append(["ifnot", p[4].expr_list[0], "goto", label1])
        p[0].code += p[5].code
        p[0].code.append(["goto", label2])
        p[0].code.append([label1, ":"])
        if(p[5].data.get("hasReturnStmt") != None):
            p[0].data["hasReturnStmt"] = 1

    else:
        p[0].ast = ["FOR", p[4].ast, ]
        # label1 = create_label()
        # p[0].code.append([label1, ":"])
        p[0].code += p[4].code
        # p[0].code.append(["goto", label1])
        p[0].code.append(["goto", start_for[-1]])
        if(p[4].data.get("hasReturnStmt") != None):
            p[0].data["hasReturnStmt"] = 1
    p[0].code.append([end_for[-1], ":"])
    start_for = start_for[0:-1]
    end_for = end_for[0:-1]


def p_for_clause(p):
    '''ForClause : SimpleStmt SEMICOLON Expression SEMICOLON SimpleStmt
    | SimpleStmt SEMICOLON SEMICOLON SimpleStmt'''

    p[0] = Node('ForClause')
    p[0].data["forclause"] = 1
    if len(p) == 6 and (len(p[3].expr_type_list) > 1 or p[3].expr_type_list[0][0] != "bool"):
        errors.add_error('Type Error', line_number.get()+1,
                         "The type of expression in for loop is not a boolean")
    p[0].code = p[1].code
    p[0].code.append([start_for[-1], ":"])
    label1 = create_label()
    p[0].code.append([label1, ":"])
    if len(p) == 6:
        p[0].ast = ["ForClause", p[1].ast, p[3].ast, p[5].ast]
        label2 = create_label()
        p[0].code += p[3].code
        p[0].code.append(["ifnot", p[3].expr_list[0], "goto", label2])
        p[0].data["for_label_pass"] = []
        p[0].data["for_label_pass"] += p[5].code
        p[0].data["for_label_pass"].append(["goto", label1])
        p[0].data["for_label_pass"].append([label2, ":"])
    else:
        p[0].ast = ["ForClause", p[1].ast, p[4].ast]
        p[0].data["for_label_pass"] = []
        p[0].data["for_label_pass"] += p[4].code
        p[0].data["for_label_pass"].append(["goto", label1])


def p_returnstmt(p):
    '''ReturnStmt : RETURN ExpressionList
    | RETURN'''
    # print(curr_scope)
    # print(curr_func)
    # print(scope_table[0])
    if len(p) == 2 and scope_table[0].table[curr_func]['return_type'] != [["void"]]:
        errors.add_error('Type Error', line_number.get()+1,
                         "Return statement without return value")
    elif len(p) == 3 and scope_table[0].table[curr_func]['return_type'] != p[2].expr_type_list:
        errors.add_error('Type Error', line_number.get()+1,
                         "Return statement with wrong return value")
    elif curr_scope == 0:
        errors.add_error('Scope Error', line_number.get()+1,
                         "Return statement is not inside a function")
    p[0] = Node('ReturnStmt')

    if len(p) == 2:
        p[0].code = [["return"]]
        p[0].ast = ["return"]
        p[0].data["hasReturnStmt"] = 1
    else:
        p[0].ast = ["return", p[2].ast]
        p[0].data["hasReturnStmt"] = 1
        p[0].code = p[2].code
        for i in range(0, len(p[2].expr_list)):
            if(p[2].data["dereflist"][i] == 1):
                var1 = create_temp()
                scope_table[curr_scope].table[var1]["offset"] = offset_list[curr_func_scope]
                offset_list[curr_func_scope] += 4
                p[0].code.append([var1, "=", "*", p[2].expr_list[i]])
                p[0].code.append(["return", var1])
            else:
                p[0].code.append(["return", p[2].expr_list[i]])
        # p[0].code.append(["return"])


# ---------------------------------
def p_break_stmt(p):
    '''BreakStmt : BREAK IDENT
                | BREAK'''
    if open_for == 0 and open_switch == 0:
        errors.add_error('Scope Error', line_number.get()+1,
                         "Break statement can only exist inside a loop")
    p[0] = Node('BreakStmt')
    p[0].code.append(['goto', end_for[-1]])
    if len(p) == 2:
        p[0].ast = ["Break"]
    else:
        p[0].ast = ["Break", [p[2]]]
# -------------------------------------


def p_continue_stmt(p):
    '''ContinueStmt : CONTINUE IDENT
                | CONTINUE'''
    if open_for == 0 and open_switch == 0:
        errors.add_error('Scope Error', line_number.get()+1,
                         "Continue statement can only exist inside a loop")
    p[0] = Node('ContinueStmt')
    p[0].code.append(['goto', start_for[-1]])
    if len(p) == 2:
        p[0].ast = ["Continue"]
    else:
        p[0].ast = ["Continue", [p[2]]]


def p_error(p):
    if p:
        print("Syntax error at line no:", line_number.get()+1, "at position", p.lexpos,
              "in the code.   " "TOKEN VALUE=", p.value,  "TOKEN TYPE=", p.type)
        parser.errok()
    else:
        print("Syntax error at EOF")


def preprocessing(f):
    lines = f.readlines()
    All_imports = []
    processed_file = open("our_new_file.go", "w")

    # print(len(lines))
    count_import_line = 0
    for line in lines:

        if "import" in line:
            count_import_line += 1
            All_imports.append(line.split()[1])

    for line in lines:
        processed_file.write(line)
        if "import" in line:

            count_import_line -= 1
            if(count_import_line == 0):
                for i in All_imports:
                    if(i == "\"math\""):
                        mat_lib = open("math.go", 'r')
                        processed_file.write(mat_lib.read())
                    if(i == "\"string\""):
                        string_lib = open("string.go", 'r')
                        processed_file.write(string_lib.read())
    processed_file.close()
    mat_lib.close()
    string_lib.close()


tokens = lexer.tokens
lexer = lex.lex()
# -------------------------------------------------------------------------------------
file = open(sys.argv[1], 'r')
# preprocessing(file)
# file.close()
# file = open("our_new_file.go", 'r')
data = file.read()
parser = yacc.yacc(debug=True)
res = parser.parse(data, lexer=lexer)
# pprint.pprint(res)
# with open('scopeTabDump', 'wb') as handle:
#     pickle.dump(scope_table, handle, protocol=pickle.HIGHEST_PROTOCOL)

pkl.dump(Sf_node, open('Sf_node.p', 'wb'))
# print((scope_table[0].table))
# print(Sf_node.code)
# print(temp_count)
# l = []

# for i in range(scope_table.keys()):
#     print(i)
# print(scope_table.keys())
# print(offset_list)
# for i in range(1, len(scope_table.keys())):
#     # print(scope_table[i].table.keys())
#     for key in scope_table[i].table:
#         if "temp_no" in key and key[0] == "t":
#             scope_table[i].table[key]["offset"] = offset_list[i]
#             offset_list[i] += 4
#     scope_table[i].table["total_size"]["type"] = offset_list[i]

# for i in range(1, len(scope_table.keys())):
#     print(scope_table[i].table)

with open('scopeTabDump', 'wb') as handle:
    pickle.dump(scope_table, handle, protocol=pickle.HIGHEST_PROTOCOL)

csv_file = "symbol_table2.csv"
with open(csv_file, 'w+') as csvfile:
    for x in range(0, scope_number+1):
        #           print("Table number",x)
        writer = csv.writer(csvfile)
        writer.writerow([])
        writer.writerow(["Table Number", x])
        writer.writerow([])
        writer.writerow(["Parent", x, "=", scope_table[x].parent])
        writer.writerow([])
        for key, value in scope_table[x].table.items():
            writer.writerow([key, value])
