import sys
import ply.yacc as yacc
from ply.lex import TOKEN
import sys
import lexer
from lexer import * 
from data_structures import SymTable
from data_structures import Node
from data_structures import Errors
import csv

precedence = (
    ('left','IDENT'),
    ('left','DEFINE'),
    ('left','COMMA'),
    ('left','LEFT_BRACKET'),
    ('left','RIGHT_BRACKET'),
    ('left','PERIOD'),
    ('left','SEMICOLON'),
    ('left','COLON'),
    ('left','INT'),
    ('left','FLOAT'),
    ('left','STRING'),
    ('left','BREAK'),
    ('left','CONTINUE'),
    ('left','RETURN'),
    ('left','LEFT_PARENTHESIS'),
    ('left','RIGHT_PARENTHESIS'),
    ('right', 'ASSIGNMENT', 'NOT'),
    ('left', 'LOGICAL_OR'),
    ('left', 'LOGICAL_AND'),
    ('left', 'EQUAL', 'NOT_EQUAL', 'LESS_THAN', 'LESS_THAN_EQUAL', 'GREATER_THAN', 'GREATER_THAN_EQUAL'),
    ('left', 'ADD', 'SUBTRACT', 'OR', 'XOR'),
    ('left', 'MULTIPLY', 'QUOTIENT', 'REMAINDER', 'SHIFT_LEFT', 'SHIFT_RIGHT', 'AND', 'AND_NOT')
)

curr_scope = 0
scope_number=0
scope_list = [0]
scope_table= {}
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
struct_off = 0
curr_func_scope = 0
offset_list = [0]
struct_sym_list = []
basic_types_list=["int","float","rune","string","bool"]

def open_scope():
    global curr_scope
    global scope_list
    global scope_number
    prev_scope=curr_scope
    scope_number += 1
    curr_scope = scope_number
    scope_list.append(curr_scope)
    offset_list.append(4)
    scope_table[curr_scope] = SymTable()
    scope_table[curr_scope].assign_parent(prev_scope)
    scope_table[curr_scope].type_list=scope_table[prev_scope].type_list
    scope_table[curr_scope].type_size_list=scope_table[prev_scope].type_size_list
    for x in scope_table[0].table:
        if(scope_table[0].table[x]["type"]==["func"]):
            scope_table[curr_scope].insert(x,["func"])
    for x in scope_table[prev_scope].table:
        if(scope_table[prev_scope].table[x]["type"]==["struct"]):
            scope_table[curr_scope].table[x]=scope_table[prev_scope].table[x]


def close_scope():
    global curr_scope
    global scope_list
    curr_scope = scope_list[-2] 
    scope_list.pop()

def presence_of_identifier(ident,purpose):
    if purpose=="Isredeclared":
        if scope_table[curr_scope].search(ident)!=None:
            return True
        else :
            return False
    
    if (purpose=='declared_anywhere'):
        for x in scope_list[::-1]:
            if(scope_table[x].search(ident)!=None):
                return x
        return False 

def create_label(p = None):
    global label_count
    label = "label_no#" + str(label_count)
    label_count += 1
    # print("helno")
    if ((not p is None) and (p == 1)):
        # print("in all")
        start_for.append(label)
    if not p is None and p == 2:
        end_for.append(label) 
    return label

def create_temp(p = None):
    global temp_count
    if p is None:
        temp = "temp_no#" + str(temp_count)
        temp_count += 1
        scope_table[curr_scope].insert(temp,"temp")
    else:
        temp = "var_temp_no#" + str(temp_count)
        temp_count += 1
    return temp

def check_operation(expr_1, op, expr_2):
    if len(expr_1)>1 or len(expr_2)>1:
        return None
    if len(op) == 1:
        op = op[0]
    expr_1 = expr_1[0]
    expr_2 = expr_2[0]
    if expr_1 != expr_2:
        if(expr_1=="int" and expr_2=="float" ) or (expr_1=="float" and expr_2=="int"):
            if op == ">" or op =="<" or op=="==" or op==">=" or op=="<="or op=="!=":
                return ["bool"]
            if op == "|" or op == "^" or op == "<<" or op == ">>" or op == "%" or op == "&" or op=="&^":
                return None
            return ["float"]

        
        return None
    if op=="||" or op=="&&":
        if(expr_1=="bool"):
            # print(expr_1,op,expr_2)
            return [expr_1]
        else:
            return None
    if expr_1 == "int" or expr_1 == "rune":
        if op == ">" or op =="<" or op=="==" or op==">=" or op=="<="or op=="!=":
            return ["bool"]
        return [expr_1]
    if expr_1=="float":
        if op == ">" or op =="<" or op=="==" or op==">=" or op=="<=" or op=="==" or op=="!=":
            return ["bool"]
        if op == "|" or op == "^" or op == "<<" or op == ">>" or op == "%" or op == "&" or op=="&^":
            return None
        else:
            return [expr_1]
    if expr_1 == "string":
        if op=="+":
            return [expr_1]
        else:
            return None

def check_unary_operation(unop, exp1):
    unop=unop[0]
    if unop=="+" or unop=="-":
        if(len(exp1)>1):
            return None
        exp1 = exp1[0]
        if exp1=="int" or exp1=="float" or exp1=="rune":
            return [exp1]
        else:
            return None
    if unop == "!":
        if len(exp1)>1:
            return None
        if exp1==["bool"]:
            return exp1
        else:
            return None
    if unop=="^":
        if len(exp1) >1 or exp1[0]!="int":
            return None
        else:
            return exp1
    if unop=="*":
        if exp1[0]!="pointer":
            return None
        exp1 = exp1[1:]
        return exp1
    if unop=="&":
        exp2 = ["pointer"]
        exp1= exp2+exp1
        return exp1

#----------------------------------------------------------------------------------------
def p_source_file(p):
    '''SourceFile  : PackageClause SEMICOLON ImportDeclStar TopLevelDeclStar'''
    p[0]=Node('SourceFile')
    p[0].code += p[1].code + p[3].code + p[4].code
    csv_file="symbol_table.csv"
    with open(csv_file, 'w+') as csvfile:
        for x in range(0,scope_number+1):
#           print("Table number",x)
            writer=csv.writer(csvfile)
            writer.writerow([])
            writer.writerow(["Table Number",x])
            writer.writerow([])
            writer.writerow(["Parent",x,"=",scope_table[x].parent])
            writer.writerow([])
            for key,value in scope_table[x].table.items():
                writer.writerow([key,value])
#           pprint.pprint(scope_table[x].table)
#           print("-----------------------------------------------------------------------")
#   print("#############################################################################")
    f=open('code.txt',"w")
    for i in range(0,len(p[0].code)):
        y=""
        for x in p[0].code[i]:
            y=y+" "+str(x)
        f.write(y+'\n')
    print(p[0].code)


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
    if(len(p)>1):
        p[0].code+=p[1].code+p[2].code

def p_top_level_decl_star(p):
    '''TopLevelDeclStar : TopLevelDeclStar TopLevelDecl SEMICOLON 
    |'''
    p[0] = Node('TopLevelDeclStar')
    if(len(p)>1):
        p[0].code += p[1].code
        p[0].code += p[2].code

def p_top_level_decl(p):
    '''TopLevelDecl : Declaration 
    | FunctionDecl'''
    p[0] = p[1]

def p_package_clause(p):
    '''PackageClause : PACKAGE IDENT'''
    p[0]=Node('PackageClause')
    p[0].ident_list.append(p[2])

def p_import_decl(p):
    '''ImportDecl : IMPORT ImportSpec 
                    | IMPORT LEFT_PARENTHESIS ImportSpecSemicolonStar RIGHT_PARENTHESIS'''
    p[0]=Node('ImportDecl')

    if len(p)==3:
        p[0].code+=p[2].code
    else:
        p[0].code+=p[3].code

def p_import_spec_semicolon_star(p):
    '''ImportSpecSemicolonStar : ImportSpecSemicolonStar ImportSpec SEMICOLON 
    |'''
    p[0]=Node('ImportSpecSemicolonStar')
    # if len(p)>1:
    #     p[0].code+=p[1].code+p[2].code

def p_import_spec(p):
    '''ImportSpec : PERIOD ImportPath
                    | IDENT ImportPath
                    | ImportPath'''
    p[0]=Node('ImportSpec')
    if(len(p)>2):
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_import_path(p):
    '''ImportPath : STRING'''
    p[0]=Node('ImportPath')
    p[0].code.append(p[1])

#-----------------------------------------------------------------------------
def p_declaration(p):
    '''Declaration : ConstDecl 
    | StructDecl
    | VarDecl'''
    p[0] = p[1]

def p_StructDecl(p):
    """StructDecl : TYPE StructName StructType"""
    p[0] = Node('StructDecl')
    scope_table[curr_scope].type_list.append(curr_struct)
    scope_table[curr_scope].type_size_list[curr_struct]=struct_off

def p_StructName(p):
    """StructName : IDENT"""
    p[0] = Node('StructName')
    global curr_struct,struct_off
    curr_struct = p[1]
    struct_off=0
    if p[1] in scope_table[curr_scope].type_list:
        errors.add_error('Redeclaration Error', p.lineno(1), "Redeclaration of type " + p[1])
    if p[1] in scope_table[curr_scope].table:
        errors.add_error('Redeclaration Error', p.lineno(1), "Redeclaration of variable " + p[1])
    scope_table[curr_scope].insert(p[1],["struct"])

def p_const_decl(p):
    '''ConstDecl : CONST ConstSpec
                | CONST LEFT_PARENTHESIS ConstSpecStar RIGHT_PARENTHESIS'''
    if len(p)==3:
        p[0] = p[2]
    else:
        p[0] = p[3]
def p_const_spec_star(p):
    '''ConstSpecStar : ConstSpecStar ConstSpec SEMICOLON
    |'''
    p[0] = Node("ConstSpecStar")
    if len(p) > 1:
        p[0].code += p[1].code
        p[0].code += p[2].code

def p_const_spec(p):
    '''ConstSpec : IdentifierList
                | IdentifierList ASSIGNMENT ExpressionList
                | IdentifierList IDENT ASSIGNMENT ExpressionList'''
    p[0]=Node("ConstSpec")
    if len(p)==2:
        p[0]=p[1]
    elif len(p)==5:
        if len(p) == 5 and p[2] not in basic_types_list:
            errors.add_error("Type Error",p.lineno(2), "Invalid type for constant " + p[2])
        if len(p[1].ident_list) != len(p[4].expr_list):
            errors.add_error("Imbalaced assignment",p.lineno(1),"Identifier and Expression list length is not equal")
        for x in p[1].ident_list:
            if presence_of_identifier(x,'Isredeclared')==True:
                errors.add_error("Redeclaration error",p.lineno(1), "Redeclaration of variable " + x)
            else:
                var1 = create_temp(1)
                scope_table[curr_scope].insert(x,[p[2]])
                scope_table[curr_scope].insert(var1,x)
                scope_table[curr_scope].update(x,"tmp",var1)
                scope_table[curr_scope].update(x,"offset",offset_list[curr_func_scope])
                offset_list[curr_func_scope] += scope_table[curr_scope].type_size_list[p[2]]
                scope_table[curr_scope].update(x,'constant',True)

        for i in range(0,len(p[1].ident_list)):
            if p[4].expr_type_list[i] != scope_table[curr_scope].table[p[1].ident_list[i]]["type"]:
                errors.add_error("Type Error",p.lineno(1), "Type mismatch in assignment")

        for i in range(0,len(p[1].ident_list)):
            temp = [scope_table[curr_scope].table[p[1].ident_list[i]]["tmp"],"="]
            if(p[4].data["dereflist"][i]==1):
                temp.append("*")
            temp.append(p[4].expr_list[i])
            p[0].code.append(temp)
    elif(len(p)==4) :
        if len(p[1].ident_list) != len(p[3].expr_list):
            errors.add_error("Imbalaced assignment",p.lineno(1),"Identifier and Expression list length is not equal")
        for i in range(0,len(p[1].ident_list)):
            if presence_of_identifier(p[1].ident_list[i],'Isredeclared')==True:
                errors.add_error("Redeclaration error",p.lineno(1), "Redeclaration of variable " + p[1].ident_list)
            else:
                    var1 = create_temp(1)
                    scope_table[curr_scope].insert(p[1].ident_list[i],p[3].expr_type_list[i])
                    scope_table[curr_scope].insert(var1,p[1].ident_list[i])
                    scope_table[curr_scope].update(p[1].ident_list[i],"tmp",var1)
                    scope_table[curr_scope].update(p[1].ident_list[i],"offset",offset_list[curr_func_scope])
                    offset_list[curr_func_scope] += scope_table[curr_scope].type_size_list[p[3].expr_type_list[i][0]]
                    scope_table[curr_scope].update(p[1].ident_list[i],'constant',True)
        for i in range(0,len(p[1].ident_list)):
            if p[3].expr_type_list[i] != scope_table[curr_scope].table[p[1].ident_list[i]]["type"]:
                errors.add_error("Type Error",p.lineno(1), "Type mismatch in assignment")
        for i in range(0,len(p[1].ident_list)):
            temp = [scope_table[curr_scope].table[p[1].ident_list[i]]["tmp"],"="]
            if(p[3].data["dereflist"][i]==1):
                temp.append("*")
            temp.append(p[3].expr_list[i])
            p[0].code.append(temp)
        


        

def p_identifier_list(p):
    '''IdentifierList : IDENT
    | IDENT COMMA IdentifierList'''
    p[0]=Node('IdentifierList')
    if(len(p)==2):
        p[0].ident_list.append(p[1])
    else:
        p[0].ident_list.append(p[1])
        p[0].ident_list=p[0].ident_list + p[3].ident_list

def p_expression_list(p):
    '''ExpressionList : Expression
    | ExpressionList COMMA Expression'''
    p[0] = Node('ExpressionList')
    if len(p)==2:
        p[0].expr_type_list += p[1].expr_type_list
        p[0].code = p[1].code
        p[0].data["dereflist"]=[]
        if p[1].data.get("deref") is None:
            p[0].expr_list += p[1].expr_list
            for i in range(0,len(p[1].expr_list)):
                p[0].data["dereflist"].append(0)
        else:
            p[0].expr_list += p[1].expr_list
            p[0].data["dereflist"]=[1]
        if p[1].data.get("memory"):
            p[0].data["memory"]=1
        else:
            p[0].data["memory"]=0
    else:
        p[0].expr_type_list += p[1].expr_type_list
        p[0].expr_type_list+=p[3].expr_type_list
        p[0].expr_list += p[1].expr_list
        p[0].data["dereflist"] = p[1].data["dereflist"]
        if p[3].data.get("deref") is None:
            p[0].expr_list += p[3].expr_list
            for i in range(0,len(p[3].expr_list)):
                p[0].data["dereflist"].append(0)
        else:
            p[0].expr_list+=p[3].expr_list
            p[0].data["dereflist"].append(1)
        p[0].code = p[1].code + p[3].code
        if p[1].data["memory"]==1 and p[3].data["memory"]==1:
            p[0].data["memory"]=1
        else:
            p[0].data["memory"]=0

# def p_type_decl(p):
#     '''TypeDecl : TYPE TypeDef
#                 | TYPE LEFT_PARENTHESIS TypeDefStar RIGHT_PARENTHESIS'''
#     if len(p)==3:
#         p[0]=['TypeDecl', [p[1]], p[2]]
#     else:
#         p[0]=['TypeDecl', [p[1]], p[3]]
        
# def p_type_spec_star(p):
#     '''TypeDefStar : TypeDef SEMICOLON TypeDefStar
#     |'''
#     if len(p) == 1:
#         p[0] = []
#     else:
#         p[0] = ['TypeDefStar', p[1], p[2]]
# def p_type_def(p):
#     '''TypeDef : IDENT Type
#     | IDENT IDENT PERIOD IDENT
#     | IDENT IDENT'''
#     if len(p)==5:
#         p[0] = ['TypeDef', [p[1]], [p[2]], [p[3]], [p[4]]]
#     elif isinstance(p[2], str):
#         p[0] = ['TypeDef', [p[1]], [p[2]]]
#     else:
#         p[0] = ['TypeDef', [p[1]], p[2]]
    
def p_var_decl(p):
    '''VarDecl : VARIABLE VarSpec
    | VARIABLE LEFT_PARENTHESIS VarSpecStar RIGHT_PARENTHESIS'''   
    if len(p)==3:
        p[0] = p[2]
    else:
        p[0] = p[3]
def p_var_spec_star(p):
    '''VarSpecStar : VarSpec SEMICOLON VarSpecStar
    |'''
    p[0] = Node('VarSpecStar')
    if len(p)>1:
        p[0].code += p[1].code
        p[0].code += p[3].code
def p_var_spec(p):
    '''VarSpec : IdentifierList Type 
                | IdentifierList Type ASSIGNMENT Expression
                | IdentifierList IDENT ASSIGNMENT ExpressionList
                | IdentifierList IDENT
                | IdentifierList ASSIGNMENT ExpressionList'''
    p[0] = Node('VarSpec')
    if (len(p)==5):
        for i in range(0,len(p[4].expr_type_list)):
            if(not (p[4].expr_type_list[i][0] in basic_types_list or p[4].expr_type_list[i][0]=="pointer")):
                errors.add_error('Type Error', p.lineno(1), 'Invalid Assignemnt')

    if(isinstance(p[2],str) and p[2]!="=" and not p[2] in scope_table[curr_scope].type_list):
        errors.add_error('Type Error', p.lineno(1), 'Invalid type of identifier')

    if len(p)==5 or len(p)==3:
        for x in p[1].ident_list:
            if presence_of_identifier(x,'Isredeclared')==True and x != "_":
                errors.add_error('Redeclaration Error', p.lineno(1), 'Redeclaration of identifier:'+x)
            else:
                if(isinstance(p[2],str)):
                    var1 = create_temp(1)
                    scope_table[curr_scope].insert(x,[p[2]])
                    scope_table[curr_scope].insert(var1,x)
                    scope_table[curr_scope].update(x,"tmp",var1)
                    scope_table[curr_scope].update(x,"offset",offset_list[curr_func_scope])
                    offset_list[curr_func_scope]+=scope_table[curr_scope].type_size_list[p[2]]
                else:
                    var1 = create_temp(1)
                    scope_table[curr_scope].insert(x,p[2].type_list)
                    scope_table[curr_scope].insert(var1,x)
                    scope_table[curr_scope].update(x,"tmp",var1)
                    scope_table[curr_scope].update(x,"offset",offset_list[curr_func_scope])
                    offset_list[curr_func_scope]+=p[2].data["typesize"]

    if len(p)==5:
        if len(p[1].ident_list) != len(p[4].expr_type_list):
            errors.add_error('Assignment Error', p.lineno(1), "Imbalanced assignment")
        for i in range(0,len(p[1].ident_list)):
            if(p[4].expr_type_list[i] != scope_table[curr_scope].table[p[1].ident_list[i]]["type"]):
                errors.add_error('Type Error', p.lineno(1), "Mismatch of type for "+p[1].ident_list[i])
        p[0] = Node('VarSpec')
        p[0].code=p[1].code+p[4].code
        for i in range(0,len(p[1].ident_list)):
            temp=[scope_table[curr_scope].table[p[1].ident_list[i]]["tmp"],"="]
            if(p[4].data["dereflist"][i]==1):
                temp.append("*")
            temp.append(p[4].expr_list[i])
            p[0].code.append(temp)

    if len(p)==4:
        if(len(p[1].ident_list) != len(p[3].expr_type_list)):
            errors.add_error('Assignment Error', p.lineno(1), "Imbalanced Assignment")
        for i in range(0,len(p[1].ident_list)):
            if len(p[3].expr_type_list[i])>1:
                errors.add_error('Assignment Error', p.lineno(1), "Auto assignment of complex expressions not allowed")
            if not p[3].expr_type_list[i][0] in basic_types_list:
                errors.add_error('Assignment Error', p.lineno(1), "Auto assignment of only basic types allowed")
            if presence_of_identifier(p[1].ident_list[i],'Isredeclared') is True and p[1].ident_list[i] != "_":
                errors.add_error('Redeclaration Error', p.lineno(1), 'Redeclaration of identifier: '+p[1].ident_list[i])
            var1 = create_temp(1)
            scope_table[curr_scope].insert(p[1].ident_list[i],p[3].expr_type_list[i])
            scope_table[curr_scope].insert(var1,p[1].ident_list[i])
            scope_table[curr_scope].update(p[1].ident_list[i],"tmp",var1)
            scope_table[curr_scope].update(p[1].ident_list[i],"offset",offset_list[curr_func_scope])
            offset_list[curr_func_scope]+=scope_table[curr_scope].type_size_list[p[3].expr_type_list[i][0]]
            p[0] = Node('VarSpec')
            p[0].code=p[1].code+p[3].code
            for i in range(0,len(p[1].ident_list)):
                temp=[scope_table[curr_scope].table[p[1].ident_list[i]]["tmp"],"="]
                if(p[3].data["dereflist"][i]==1):
                    temp.append("*")
                temp.append(p[3].expr_list[i])
                p[0].code.append(temp)

def p_short_var_decl(p):
    '''ShortVarDecl : IdentifierList DEFINE ExpressionList'''
    if(len(p[1].ident_list) != len(p[3].expr_type_list)):
        errors.add_error('Assignment Error', p.lineno(1), "Imbalanced Assignment")
    for i in range(0,len(p[1].ident_list)):
        if len(p[3].expr_type_list[i])>1:
            errors.add_error('Assignment Error', p.lineno(1), "Auto assignment of complex expressions not allowed")
        if not p[3].expr_type_list[i][0] in basic_types_list:
            errors.add_error('Assignemnt Error', p.lineno(1), "Auto assignment of only basic types allowed")
        if presence_of_identifier(p[1].ident_list[i],'Isredeclared') is True and p[1].ident_list[i] != "_":
            errors.add_error('Assignment Error', p.lineno(1), 'Redeclaration of identifier:'+p[1].ident_list[i])
        var1 = create_temp(1)
        scope_table[curr_scope].insert(p[1].ident_list[i],p[3].expr_type_list[i])
        scope_table[curr_scope].insert(var1,p[1].ident_list[i])
        scope_table[curr_scope].update(p[1].ident_list[i],"tmp",var1)
        scope_table[curr_scope].update(p[1].ident_list[i],"offset",offset_list[curr_func_scope])
        offset_list[curr_func_scope]+=scope_table[curr_scope].type_size_list[p[3].expr_type_list[i][0]]
    p[0] = Node('ShortVarDecl')
    p[0].code=p[3].code
    for i in range(0,len(p[1].ident_list)):
        temp=[scope_table[curr_scope].table[p[1].ident_list[i]]["tmp"],"="]
        if(p[3].data["dereflist"][i]==1):
            temp.append("*")
        temp.append(p[3].expr_list[i])
        p[0].code.append(temp)
    p[0].expr_type_list=[]


def p_function_decl(p):
    '''FunctionDecl : FUNCTION FunctionName OpenScope Signature Block CloseScope
                    | FUNCTION FunctionName OpenScope Signature CloseScope'''

    p[0] = Node('FunctionDecl')
    p[0].code = p[2].code
    p[0].code += p[4].code
    if len(p) != 6:
        p[0].code += p[5].code
    p[0].code.append(["return"])

def p_function_name(p):
    """
    FunctionName : IDENT
    """
    p[0] = Node('FunctionName')
    global curr_func
    if presence_of_identifier(p[1],'Isredeclared')==True:
        errors.add_error("Redecleration",p.lineno(1),p[1]+" is redeclared")
    scope_table[0].insert(p[1],["func"])
    scope_table[0].update(p[1], "scope", curr_func_scope)
    p[0].code.append([p[1],":"])
    curr_func = p[1]

# --------------------- TYPES -------------------------------------
# Removed IDENT PERIOD IDENT
def p_type(p):
    '''Type : LEFT_PARENTHESIS IDENT RIGHT_PARENTHESIS
    | TypeLit 
    | LEFT_PARENTHESIS Type RIGHT_PARENTHESIS'''
    if len(p)==2:
        p[0]=p[1]
    else:
        if isinstance(p[2],str) and not p[2] in scope_table[curr_scope].type_list:
            errors.add_error('Type Error', p.lineno(1), "Invalid type of identifier "+p[2])
        if isinstance(p[2],str):
            p[0] = Node('Type')
            p[0].type_list.append(p[2])
            p[0].data["typesize"] = scope_table[curr_scope].type_size_list[p[2]]
        else:
            p[0]=p[2]

def p_type_lit(p):
    '''TypeLit : ArrayType 
    | PointerType '''
    # | StructType 
    # | FunctionType 
    # | SliceType 
    # | MapType
    p[0] = p[1]

def p_array_type(p):
    '''ArrayType : LEFT_BRACKET INT RIGHT_BRACKET Type
                | LEFT_BRACKET INT RIGHT_BRACKET IDENT'''
                # | LEFT_BRACKET Expression RIGHT_BRACKET IDENT PERIOD IDENT'''    
    if isinstance(p[4],str) and not p[4] in scope_table[curr_scope].type_list:
        errors.add_error('Type Error', p.lineno(1), "This type hasn't been declared yet "+p[4])
    temp = int(p[2])
    p[0] = Node('ArrayType')
    if isinstance(p[4],str):
        p[0].type_list.append("arr"+p[2])
        p[0].type_list.append(p[4])
        p[0].data["typesize"]=temp*scope_table[curr_scope].type_size_list[p[4]]
    else:
        p[0].type_list.append("arr"+p[2])
        p[0].type_list += p[4].type_list
        p[0].data["typesize"]=temp*p[4].data["typesize"]


# def p_slice_type(p):
#     '''SliceType : LEFT_BRACKET RIGHT_BRACKET Type
#     | LEFT_BRACKET RIGHT_BRACKET IDENT PERIOD IDENT
#     | LEFT_BRACKET RIGHT_BRACKET IDENT'''
#     p[0] = ['SliceType']
#     for idx in range(1,len(p)):
#         if p[idx] == '[' or p[idx] == ']':
#             continue
#         if isinstance(p[idx],str):
#             p[0].append([p[idx]])
#         else:
#             p[0].append(p[idx])

def p_struct_type(p):
    '''StructType : STRUCT OpenStruct LEFT_BRACE FieldDeclStar RIGHT_BRACE CloseStruct'''
    p[0] = Node('StructType')
    p[0].code = p[4].code
# --------------------------------------------------------------------
def p_field_decl_star(p):
    '''FieldDeclStar : FieldDeclStar FieldDecl SEMICOLON
    |'''
    p[0] = Node('FieldDeclStar')
    if len(p) > 1:
        p[0].code += p[1].code
        p[0].code += p[2].code

# def p_field_decl(p):
#     '''FieldDecl : IdentifierList Type Tag
#     | IdentifierList IDENT Tag
#     | IdentifierList IDENT PERIOD IDENT Tag
#     | IdentifierList Type 
#     | IdentifierList IDENT
#     | IdentifierList IDENT PERIOD IDENT
#     | EmbeddedField Tag
#     | EmbeddedField'''
#     p[0] = ['FieldDecl']
#     for idx in range(1,len(p)):
#         if isinstance(p[idx],str):
#             p[0].append([p[idx]])
#         else:
#             p[0].append(p[idx])

def p_field_decl(p):
    """FieldDecl : IDENT COMMA IdentifierList Type
              | IDENT COMMA IdentifierList IDENT
              | IDENT Type
              | IDENT IDENT
              | IDENT STRUCT MULTIPLY IDENT
              | IDENT COMMA IdentifierList STRUCT MULTIPLY IDENT"""
    p[0] = Node('FieldDecl')
    global struct_off
    if len(p)==3:
        if(isinstance(p[2],str)):
            if(p[1] in struct_sym_list):
                errors.add_error('Redeclaration Error', p.lineno(1), "This identifier is already declared in this list")
            struct_sym_list.append(p[1])
            scope_table[curr_scope].update(curr_struct,p[1],[p[2]])
            scope_table[curr_scope].update(curr_struct,"offset "+p[1],struct_off)
            struct_off += scope_table[curr_scope].type_size_list[p[2]]
        else:
            if(p[1] in struct_sym_list):
                errors.add_error('Redeclaration Error', p.lineno(1), "This identifier is already declared in this list")
            struct_sym_list.append(p[1])
            scope_table[curr_scope].update(curr_struct,p[1],p[2].type_list)
            scope_table[curr_scope].update(curr_struct,"offset "+p[1],struct_off)
            struct_off += p[2].data["typesize"]
    elif len(p)==5 and not isinstance(p[3],str):
        if isinstance(p[4],str):
            if p[1] in struct_sym_list:
                errors.add_error('Redeclaration Error', p.lineno(1), "This identifier is already declared in this list")
            struct_sym_list.append(p[1])
            scope_table[curr_scope].update(curr_struct,p[1],[p[4]])
            scope_table[curr_scope].update(curr_struct,"offset "+p[1],struct_off)
            struct_off += scope_table[curr_scope].type_size_list[p[4]]
            for x in p[3].ident_list:
                if(x in struct_sym_list):
                    errors.add_error('Redeclaration Error', p.lineno(1), "This identifier is already declared in this list")
                struct_sym_list.append(x)
                scope_table[curr_scope].update(curr_struct,x,[p[4]])
                scope_table[curr_scope].update(curr_struct,"offset "+x,struct_off)
                struct_off += scope_table[curr_scope].type_size_list[p[4]]
        else:
            if(p[1] in struct_sym_list):
                errors.add_error('Redeclaration Error', p.lineno(1), "This identifier is already declared in this list")
            struct_sym_list.append(p[1])
            scope_table[curr_scope].update(curr_struct,p[1],p[4].type_list)
            scope_table[curr_scope].update(curr_struct,"offset "+p[1],structOff)
            struct_off += p[4].data["typesize"]
            for x in p[3].ident_list:
                if x in struct_sym_list:
                    errors.add_error('Redeclaration Error', p.lineno(1), "This identifier is already declared in this list")
                struct_sym_list.append(x)
                scope_table[curr_scope].update(curr_struct,x,p[4].type_list)
                scope_table[curr_scope].update(curr_struct,"offset "+x,struct_off)
                structOff += p[4].data["typesize"]
    elif len(p)==5:
        if(p[4] != curr_struct):
            errors.add_error('Struct Error', p.lineno(1), "The identifier should be the current struct")
        struct_sym_list.append(p[1])
        scope_table[curr_scope].update(curr_struct, p[1], ["pointer",curr_struct])
        scope_table[curr_scope].update(curr_struct,"offset "+p[1],struct_off)
        struct_off += 4
    else:
        if p[6] != curr_struct:
            errors.add_error('Struct Error', p.lineno(1), "The identifier should be the current struct")
        struct_sym_list.append(p[1])
        scope_table[curr_scope].update(curr_struct, p[1], ["pointer",curr_struct])
        for x in p[3].ident_list:
            if(x in struct_sym_list):
                errors.add_error('Redeclaration Error', p.lineno(1), "This identifier is already declared in this list")
            struct_sym_list.append(x)
            scope_table[curr_scope].update(curr_struct,x,["pointer",curr_struct])
            scope_table[curr_scope].update(curr_struct,"offset "+x, struct_off)
            struct_off += 4

# def p_embedded_field(p):
#     '''EmbeddedField : MULTIPLY IDENT 
#     | MULTIPLY IDENT PERIOD IDENT 
#     | IDENT
#     | IDENT PERIOD IDENT'''
#     if len(p) == 2:
#         p[0] = [p[1]]
#     else:
#         p[0] = ['EmbeddedField']
#         for index in range(1,len(p)):
#             p[0].append([p[index]])
# def p_tag(p):
#     '''Tag : STRING'''
#     p[0] = [p[1]]

def p_pointer_type(p):
    '''PointerType : MULTIPLY Type
        | MULTIPLY IDENT'''
        # | MULTIPLY IDENT PERIOD IDENT'''
    if isinstance(p[2],str) and not p[2] in scope_table[curr_scope].type_list:
        errors.add_error('Type Error', p.lineno(1), "Invalid type of identifier "+p[2])
    p[0] = Node('PointerType')
    p[0].type_list.append("pointer")
    if isinstance(p[2],str):
        p[0].type_list.append(p[2])
        p[0].data["typesize"]=4
    else:
        p[0].type_list += p[2].type_list
        p[0].data["typesize"]=4
# def p_function_type(p):
#     '''FunctionType : FUNCTION Signature'''
#     p[0] = ['FunctionType', [p[0]], p[1]]

def p_signature(p):
    '''Signature : Parameters Result'''
    p[0] = Node('Signature')

def p_result(p):
    '''Result : LEFT_PARENTHESIS TypeList RIGHT_PARENTHESIS 
    |'''
    p[0] = Node('Result')
    if len(p)==1:
        scope_table[0].update(curr_func,'return_type',[["void"]])
        scope_table[0].update(curr_func,'total_return_size',0)
        scope_table[0].update(curr_func,'return_size_list',[])
    else:
        scope_table[0].update(curr_func,'return_type',p[2].ident_list)
        total_sum = -8- scope_table[0].table[curr_func]["total_param_size"]
        return_list = []
        return_sum = 0
        for i in range(0,len(p[2].ident_list)):
            return_list.append(total_sum)
            total_sum -= p[2].expr_list[i]
            return_sum += p[2].expr_list[i]
        scope_table[0].update(curr_func,"total_return_size", return_sum)
        scope_table[0].update(curr_func,"return_size_list", return_list)

def p_TypeList(p):
    """TypeList : TypeList COMMA IDENT
    | TypeList COMMA Type 
    | IDENT
    | Type"""
    if(isinstance(p[1],str) and not p[1] in scope_table[curr_scope].type_list):
        errors.add_error(p.lineno(1), "Invalid return type")
    if len(p)==4 and isinstance(p[3],str) and not p[3] in scope_table[curr_scope].type_list:
        errors.add_error(p.lineno(3), "Invalid return type")
    p[0] = Node('TypeList')
    if(len(p)==2):
        if(isinstance(p[1],str)):
            p[0].ident_list.append([p[1]])
            p[0].expr_list.append(scope_table[curr_scope].type_size_list[p[1]]) 
        else:
            p[0].ident_list.append(p[1].type_list)
            p[0].expr_list.append(p[1].data["typesize"])
    else:
        if(isinstance(p[3],str)):
            p[0].ident_list=p[1].ident_list
            p[0].expr_list=p[1].expr_list
            p[0].ident_list.append([p[3]])
            p[0].expr_list.append(scope_table[curr_scope].type_size_list[p[3]])
        else:
            p[0].ident_lList=p[1].ident_list
            p[0].expr_list=p[1].expr_list
            p[0].ident_list.append(p[3].type_list)
            p[0].expr_list.append(p[3].data["typesize"])


def p_parameters(p):
    '''Parameters : LEFT_PARENTHESIS RIGHT_PARENTHESIS
                | LEFT_PARENTHESIS ParameterList RIGHT_PARENTHESIS
                | LEFT_PARENTHESIS ParameterList COMMA RIGHT_PARENTHESIS'''
    p[0] = Node('Paramters')
    if(len(p)==3):
        scope_table[0].update(curr_func,"takes",[["void"]])
        scope_table[0].update(curr_func,"total_param_size",0)
    else:
        scope_table[0].update(curr_func,"takes",p[2].expr_type_list)
        arg_offset = -8
        param_sum = 0
        param_list = []
        n = len(p[2].ident_list)
        for i in range(0, n):
            scope_table[curr_scope].update(p[2].ident_list[n-i-1], "offset", arg_offset)
            param_list.append(p[2].expr_list[i])
            arg_offset -= p[2].expr_list[n-i-1]
            param_sum += p[2].expr_list[i]
        scope_table[0].update(curr_func,"total_param_size",param_sum)
        scope_table[0].update(curr_func,"param_size_list",param_list)


def p_parameter_list(p):
    '''ParameterList : ParameterDecl 
    | ParameterList COMMA ParameterDecl'''
    p[0] = Node('ParameterList')
    if len(p)==2:
        p[0] = p[1]
    else:
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
    if isinstance(p[2],str) and not p[2] in scope_table[curr_scope].type_list:
        errors.add_error(p.lineno(2), "Invalid type of identifier "+p[2])

    p[0] = Node('ParameterDecl')
    flag = 0
    if not isinstance(p[1],str):
        p[0].ident_list = p[1].ident_list
        for x in p[1].ident_list:
            if presence_of_identifier(x,'Isredeclared')==True and x != "_":
                errors.add_error(p.lineno(1), "Redeclaration of identifier "+x)
            else:
                if(isinstance(p[2],str)):
                    var1 = create_temp(1)
                    scope_table[curr_scope].insert(x,[p[2]])
                    scope_table[curr_scope].insert(var1,x)
                    scope_table[curr_scope].update(x,"tmp",var1)
                    p[0].expr_type_list.append([p[2]])
                    p[0].expr_list.append(scope_table[curr_scope].type_size_list[p[2]])
                else:
                    var1 = create_temp(1)
                    scope_table[curr_scope].insert(x,p[2].type_list)
                    scope_table[curr_scope].insert(var1,x)
                    scope_table[curr_scope].update(x,"tmp",var1)
                    p[0].expr_type_list.append(p[2].type_list)
                    p[0].expr_list.append(p[2].data["typesize"])
    else:
        if presence_of_identifier(p[1],'Isredeclared')==True and p[1] != "_":
            errors.add_error(p.lineno(1), "Redeclaration of identifier "+p[1])
        else:
            p[0].ident_list = [p[1]]
            if(isinstance(p[2],str)):
                var1 = create_temp(1)
                scope_table[curr_scope].insert(p[1], [p[2]])
                scope_table[curr_scope].insert(var1,p[1])
                scope_table[curr_scope].update(p[1],"tmp",var1)
                p[0].expr_type_list.append([p[2]])
                p[0].expr_list.append(scope_table[curr_scope].type_size_list[p[2]])
            else:
                var1 = create_temp(1)
                scope_table[curr_scope].insert(p[1], p[2].type_list)
                scope_table[curr_scope].insert(var1,p[1])
                scope_table[curr_scope].update(p[1],"tmp",var1)
                p[0].expr_type_list.append(p[2].type_list)
                p[0].expr_list.append(p[2].data["typesize"])

def p_ParaIdentList(p):
    """
    ParaIdentList : IDENT COMMA IDENT
               | ParaIdentList COMMA IDENT
    """
    p[0] = Node('ParaIdentList')
    if(isinstance(p[1],str)):
        p[0].ident_list.append(p[1])
        p[0].ident_list.append(p[3])
    else:
        p[0].ident_list = p[1].ident_list
        p[0].ident_list.append(p[3])

#--------------------------------------------------------------------
# def p_MapType(p):
#     '''MapType : MAP LEFT_BRACKET Type RIGHT_BRACKET Type
#     | MAP LEFT_BRACKET Type RIGHT_BRACKET IDENT
#     | MAP LEFT_BRACKET Type RIGHT_BRACKET IDENT PERIOD IDENT
#     | MAP LEFT_BRACKET IDENT RIGHT_BRACKET Type
#     | MAP LEFT_BRACKET IDENT RIGHT_BRACKET IDENT
#     | MAP LEFT_BRACKET IDENT RIGHT_BRACKET IDENT PERIOD IDENT
#     | MAP LEFT_BRACKET IDENT PERIOD IDENT RIGHT_BRACKET Type
#     | MAP LEFT_BRACKET IDENT PERIOD IDENT RIGHT_BRACKET IDENT
#     | MAP LEFT_BRACKET IDENT PERIOD IDENT RIGHT_BRACKET IDENT PERIOD IDENT'''
#     p[0]=['MapType']
#     for index in range(1,len(p)):
#       if(isinstance(p[index],str) and p[index]!="[" and p[index]!="]" and p[index]!="map"):
#         p[0].append([p[index]])
#       elif(p[index]!="[" and p[index]!="]" and p[index]!="map"):
#         p[0].append(p[index])
def p_block(p):
    '''Block : LEFT_BRACE StatementList RIGHT_BRACE'''
    p[0] = p[2]
def p_statement_list(p):
    '''StatementList : StatementList Statement SEMICOLON
    |'''
    p[0] = Node('StatementList')
    if len(p)>1:
        p[0].code = p[1].code + p[2].code
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
        p[0] = p[1]
    else:
        p[0] = Node('Expression')
        if len(p[1].expr_type_list)>1 or len(p[3].expr_type_list)>1:
            errors.add_error("Operation Error", p.lineno(1), "Can't apply binary operators to multiple values")
        if check_operation(p[1].expr_type_list[0], p[2], p[3].expr_type_list[0]) is None:
            # print(check_operation(p[1].expr_type_list[0], p[2], p[3].expr_type_list[0]))
            # print(p[1].expr_type_list[0], p[2], p[3].expr_type_list[0])
            errors.add_error("Operation Error", p.lineno(1), "Invalid types for operator")
        p[0].code = p[1].code+p[3].code
        if p[1].data.get("deref") is None:
            var1 = create_temp()
            p[0].code.append([var1,"=","*",p[1].expr_list[0]])
        else:
            var1 = p[1].expr_list[0]
        if p[3].data.get("deref") is None:
            var2 = create_temp()
            p[0].code.append([var2,"=","*",p[3].expr_list[0]])
        else:
            var2=p[3].expr_list[0]
        p[0].expr_type_list.append(check_operation(p[1].expr_type_list[0] , [p[2]], p[3].expr_type_list[0] ))
        p[0].data["memory"]=0
        var3 = create_temp()
        p[0].expr_list = [var3]
        p[0].code.append([var3,"=",var1,p[2]+p[3].expr_type_list[0][0],var2])
def p_unary_expr(p):
    '''UnaryExpr : PrimaryExpr 
    | unary_op UnaryExpr'''
    if len(p)==2:
        p[0] = p[1]
    else:
        p[0] = Node('UnaryExp')
        if len(p[1].expr_type_list)>1:
            errors.add_error("Operation Error", p.lineno(1), "Can't apply binary operators to multiple values")
        if check_unary_operation(p[1].expr_type_list[0], p[2].expr_type_list[0]) is None:
            print(2)
            errors.add_error("Operation Error", p.lineno(1), "Invalid types for operator")
        p[0].expr_type_list.append(check_unary_operation(p[1].expr_type_list[0], p[2].expr_type_list[0]))
        p[0].code = p[2].code
        if p[1].expr_type_list[0][0]=="*":
            p[0].data["memory"] = 1
            p[0].data["deref"] = 1
            var1 = create_temp()
            p[0].code.append([var1,"=","*",p[2].expr_list[0]])
            p[0].expr_list=[var1]
        elif p[1].expr_type_list[0][0]=="&":
            p[0].data["memory"]=0
            if p[2].data.get("deref") is None:
                if p[2].data["memory"] == 0:
                    errors.add_error('Address Error', p.lineno(1), "Can't get address")
                var1 = create_temp()
                p[0].code.append([var1,"=","&",p[2].expr_list[0]])
                p[0].expr_list = [var1]
            else:
                p[0].expr_list = p[2].expr_list
        else:
            p[0].data["memory"]=0
            var1 = create_temp()
            p[0].expr_list = [var1]
            if p[1].expr_type_list[0][0]=='+' or p[1].expr_type_list[0][0]=='-':
                p[0].code.append([var1,"=",p[1].expr_type_list[0][0]+p[2].expr_type_list[0][0],p[2].expr_list[0]])
            else:
                p[0].code.append([var1,"=",p[1].expr_type_list[0][0],p[2].expr_list[0]])
   
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
  


def p_primary_expr(p):
    '''PrimaryExpr : IDENT
    | LEFT_PARENTHESIS Expression RIGHT_PARENTHESIS
    | Literal
    | PrimaryExpr Index
    | PrimaryExpr PERIOD IDENT 
    | PrimaryExpr Arguments'''
    # | PrimaryExpr Slice 
    # | PrimaryExpr Selector 
    # | IDENT PERIOD IDENT
    if len(p)==2 and not isinstance(p[1],str):
        p[0] = p[1]
        p[0].data["memory"] = 0
        p[0].expr_list = p[1].expr_list
    elif len(p)==2:
        if(presence_of_identifier(p[1],"declared_anywhere")==False):
            errors.add_error("Undeclared Error", p.lineno(1), "Variable "+p[1]+" is not declared")
        p[0]=Node('PrimaryExpr')
        p[0].expr_type_list.append(scope_table[presence_of_identifier(p[1],"declared_anywhere")].table[p[1]]["type"])
        p[0].data["memory"] = 1
        p[0].data["isID"] = p[1]
        x=presence_of_identifier(p[1],'declared_anywhere')
        temp1=scope_table[x].table[p[1]]["type"]
        if(temp1!=["func"]):
            p[0].expr_list=[scope_table[presence_of_identifier(p[1],'declared_anywhere')].table[p[1]]["tmp"]]
        else:
            p[0].expr_list=["func"]
        if scope_table[x].table.get(temp1[0])!=None:
            if(scope_table[x].table[temp1[0]]["type"]==["struct"]):
                var1=create_temp()
                p[0].code.append([var1,"=", "&",scope_table[presence_of_identifier(p[1],'declared_anywhere')].table[p[1]]["tmp"]])
                p[0].data["deref"]=1
                p[0].expr_list=[var1]
        elif temp1[0][0:3]=="arr" or temp1[0]=="pointer":
            p[0].data["deref"]=1

    elif(len(p)==4 and p[2]=='.'):
        temp=p[1].expr_type_list[0][0]
        if(scope_table[curr_scope].table.get(temp)!=None and scope_table[curr_scope].table[temp]["type"]==["struct"]):
            if(scope_table[curr_scope].table[temp].get(p[3])==None):
                errors.add_error("Struct Error", p.lineno(1), "No such attribute of given struct")
            p[0]=Node('PrimaryExpr')
            p[0].expr_type_list.append(scope_table[curr_scope].table[temp][p[3]])
            p[0].data["memory"]=1
            p[0].code=p[1].code
            var1=create_temp()
            off=scope_table[curr_scope].table[p[1].expr_type_list[0][0]]["offset "+p[3]]
            p[0].code.append([var1, "=", p[1].expr_list[0], '+int', off])
            p[0].data["deref"]=1
            p[0].expr_list.append(var1)
        else:
            errors.add_error("Error", p.lineno(1), "The identifier is not declared or isn't a struct")

    elif(len(p)==4):
        p[0]=p[2]

    elif p[2].data.get("index") is not None:
        if p[1].expr_type_list[0][0][0:3]!="arr":
            errors.add_error("Type Error", p.lineno(1), "The type of this expression is not an array")
        p[0] = p[1]
        p[0].code+=p[2].code
        p[0].expr_type_list[0] = p[0].expr_type_list[0][1:]
        p[0].data["memory"] = 1
        p[0].data["deref"] = 1
        var1 = create_temp()
        p[0].code.append([var1,"=",p[2].expr_list[0]])
        for i in range(0,len(p[0].expr_type_list[0])):
            if p[0].expr_type_list[0][i][0:3]=="arr":
                temp1 = int(p[0].expr_type_list[0][i][3:])
                p[0].code.append([var1,"=",var1,"*int",temp1])
            else:
                width = 0
                if p[0].expr_type_list[0][i]=="pointer":
                    width = 4
                else:
                    width = scope_table[curr_scope].type_size_list[p[0].expr_type_list[0][i]]
                p[0].code.append([var1,"=",var1,"*int",width])
                p[0].code.append([var1,"=",var1,'+int',p[0].expr_list[0]])
                break
        p[0].expr_list=[var1]

    elif p[2].data.get("arguments") is not None:
        if p[1].expr_type_list[0][0]!="func" or p[1].data.get("isID") is None:
            errors.add_error("Error", p.lineno(1), "The primary expression is not a function")
        if(p[2].expr_type_list != scope_table[0].table[p[1].data["isID"]]["takes"]):
            errors.add_error("Error", p.lineno(1), "The arguments passed are not of the same type as the function")
        p[0]=Node('PrimaryExpr')
        p[0].expr_type_list=scope_table[0].table[p[1].data["isID"]]['return_type']
        if(p[0].expr_type_list[0][0]=="void"):
            p[0].expr_list=[]
        else:
            for i in range(0,len(p[0].expr_type_list)):
                var1=create_temp()
                p[0].expr_list.append(var1)
        p[0].data["multi_return"] = 1
        p[0].data["memory"]=0
        p[0].code=p[2].code
        p[0].code.append(["startf",p[1].data["isID"]])
        for i in range(0,len(p[2].expr_list)):
            if(p[2].data["dereflist"][i]==1):
                # var1=create_temp()
                # p[0].code.append([var1,"=","*",p[2].expr_list[i]])
                # p[0].code.append(["param",var1])
                p[0].code.append(["param",p[2].expr_list[i],scope_table[0].table[p[1].data["isID"]]["param_size_list"][i]  ])
            else:
                p[0].code.append(["param",p[2].expr_list[i]])
        p[0].code.append(["call",p[1].data["isID"]])
        p[0].code.append(["endf",p[1].data["isID"]])
        for i in range(0,len(p[0].expr_list)):
            p[0].code.append([p[0].expr_list[i],"=","retval_"+str(i+1)])

# def p_selector(p):
#     '''Selector : PERIOD IDENT'''
#     p[0] = ['Selector', [p[1]], [p[2]]]

def p_index(p):
    '''Index : LEFT_BRACKET Expression RIGHT_BRACKET'''
    if p[2].expr_type_list!=[["int"]]:
        errors.add_error("Type Error", p.lineno(1), "The index expression is not of type int")
    p[0] = p[2]
    p[0].data["index"]=1
# def p_slice(p):
#     '''Slice : LEFT_BRACKET Expression COLON Expression RIGHT_BRACKET
#     | LEFT_BRACKET Expression COLON RIGHT_BRACKET
#     | LEFT_BRACKET COLON Expression RIGHT_BRACKET
#     | LEFT_BRACKET COLON RIGHT_BRACKET 
#     | LEFT_BRACKET Expression COLON Expression COLON Expression RIGHT_BRACKET
#     | LEFT_BRACKET COLON Expression COLON Expression RIGHT_BRACKET'''
#     p[0] = ['Slice']
#     for idx in range(1,len(p)):
#         if p[idx] == '[' or p[idx] == ']' or p[idx] == ':':
#             continue
#         if isinstance(p[idx],str):
#             p[0].append([p[idx]])
#         else:
#             p[0].append(p[idx])
# def p_arguments(p):
#     '''Arguments : LEFT_PARENTHESIS RIGHT_PARENTHESIS
#               | LEFT_PARENTHESIS ExpressionList RIGHT_PARENTHESIS
#               | LEFT_PARENTHESIS ExpressionList COMMA RIGHT_PARENTHESIS
#               | LEFT_PARENTHESIS Type RIGHT_PARENTHESIS
#               | LEFT_PARENTHESIS Type COMMA RIGHT_PARENTHESIS
#               | LEFT_PARENTHESIS Type COMMA ExpressionList RIGHT_PARENTHESIS
#               | LEFT_PARENTHESIS Type COMMA ExpressionList COMMA RIGHT_PARENTHESIS
#               | LEFT_PARENTHESIS IDENT RIGHT_PARENTHESIS
#               | LEFT_PARENTHESIS IDENT COMMA RIGHT_PARENTHESIS
#               | LEFT_PARENTHESIS IDENT COMMA ExpressionList RIGHT_PARENTHESIS
#               | LEFT_PARENTHESIS IDENT COMMA ExpressionList COMMA RIGHT_PARENTHESIS
#               | LEFT_PARENTHESIS IDENT PERIOD IDENT RIGHT_PARENTHESIS
#               | LEFT_PARENTHESIS IDENT PERIOD IDENT COMMA RIGHT_PARENTHESIS
#               | LEFT_PARENTHESIS IDENT PERIOD IDENT COMMA ExpressionList RIGHT_PARENTHESIS
#               | LEFT_PARENTHESIS IDENT PERIOD IDENT COMMA ExpressionList COMMA RIGHT_PARENTHESIS'''
#     p[0] = ['Arguments']
#     for idx in range(1,len(p)):
#         if isinstance(p[idx],str) and p[idx]!="(" and p[idx]!=")" and p[idx] != ",":
#             p[0].append([p[idx]])
#         elif p[idx]!="(" and p[idx]!=")" and p[idx] != ",":
#             p[0].append(p[idx])

def p_Arguments(p):
    """Arguments : LEFT_PARENTHESIS RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS ExpressionList RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS ExpressionList COMMA RIGHT_PARENTHESIS"""
    if len(p)==3:
        p[0] = Node()
        p[0].data["arguments"] = 1
        p[0].expr_type_list.append(["void"])
    else:
        p[0] = p[2]
        p[0].data["arguments"] = 1
        p[0].expr_type_list=p[2].expr_type_list


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
    | TrueFalseLit'''
    # | IMAGINARY 
    p[0] = p[1]

def p_true_false_lit(p):
    '''TrueFalseLit : TRUE
    | FALSE'''
    p[0] = Node('TrueFalseLit')
    p[0].expr_type_list.append(["bool"])
    p[0].expr_list.append(p[1])

def p_int_lit(p):
    '''IntLit : INT'''
    p[0] = Node('IntLit')
    p[0].expr_type_list.append(["int"])
    p[0].expr_list.append(p[1])

def p_float_lit(p):
    '''FloatLit : FLOAT'''
    p[0] = Node('FloatLit')
    p[0].expr_type_list.append(["float"])
    p[0].expr_list.append(p[1])

def p_rune_lit(p):
    '''RuneLit : RUNE'''
    p[0] = Node('RuneLit')
    p[0].expr_type_list.append(["rune"])
    p[0].expr_list.append(p[1])

def p_string_lit(p):
    '''StringLit : STRING'''
    p[0] = Node('StringLit')
    p[0].expr_type_list.append(["string"])
    p[0].expr_list.append(p[1])


# def p_composite_lit(p):
#     '''CompositeLit : StructType LiteralValue
#                 | ArrayType LiteralValue
#                 | SliceType LiteralValue
#                 | MapType LiteralValue
#                 | IDENT LiteralValue
#                 | IDENT PERIOD IDENT LiteralValue'''
#     p[0] = ['CompositeLit']
#     for idx in range(1,len(p)):
#         if isinstance(p[idx],str) and p[idx]!="[" and p[idx]!="]" and p[idx]!=",":
#             p[0].append([p[idx]])
#         elif p[idx]!="[" and p[idx]!="]" and p[idx]!=",":
#             p[0].append(p[idx])
# def p_literal_value(p):
#     '''LiteralValue : LEFT_BRACE RIGHT_BRACE
#                     | LEFT_BRACE ElementList RIGHT_BRACE
#                     | LEFT_BRACE ElementList COMMA RIGHT_BRACE'''
#     if len(p) == 3:
#         p[0] = []
#     else:
#         p[0] = p[2]
# def p_element_list(p):
#     '''ElementList : KeyedElement 
#     | ElementList COMMA KeyedElement'''
#     if len(p) == 2:
#         p[0] = p[1]
#     else:
#         p[0] = ['ElementList', p[1], p[3]]
# def p_keyed_element(p):
#     '''KeyedElement : Element
#                     | IDENT COLON Element
#                     | Expression COLON Element
#                     | LiteralValue COLON Element'''
#     if len(p) == 2:
#         p[0] = p[1]
#     else:
#         p[0] = ['KeyedElement']
#         for idx in range(1,len(p)):
#             if(isinstance(p[idx],str)):
#                 p[0].append([p[idx]])
#             else:
#                 p[0].append(p[idx])
# def p_element(p):
#     '''Element : Expression 
#     | LiteralValue'''
#     p[0] = p[1]
# def p_function_lit(p):
#     '''FunctionLit : FUNCTION Signature Block'''
#     p[0] = ['FunctionLit', p[2], p[3]]

#----------------------------------------------------------
def p_statement(p):
    '''Statement : Declaration 
    | SimpleStmt 
    | ReturnStmt 
    | BreakStmt 
    | ContinueStmt 
    | OpenScope Block CloseScope 
    | IfStmt 
    | SwitchStmt 
    | ForStmt  '''
    if len(p)==2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_simple_stmt(p):
    '''SimpleStmt : Expression
    | IncDecStmt 
    | Assignment 
    | ShortVarDecl 
    |'''
    if len(p)>1:
        p[0] = p[1]
    else:
        p[0] = Node('SimpleStmt')

# def p_labeled_stmt(p):
#     '''LabeledStmt : IDENT COLON Statement '''
#     p[0] = ['LabeledStmt', [p[1]], [p[2]], p[3]]

def p_inc_dec_stmt(p):
    '''IncDecStmt : Expression INCREMENT
                    | Expression DECREMENT'''
    p[0] = p[1]
    if p[0].expr_type_list != [["int"]]:
        errors.add_error(p.lineno(1), "Type Mismatch: Cannot increment/decrement non-integer value")
    if p[1].data["memory"] == 0:
        errors.add_error(p.lineno(1), "Cannot increment/decrement non-addressable value")
    if p[1].data.get("deref") == None:
        if p[2]=="++":
            p[0].code.append([p[1].expr_list[0],"=",p[1].expr_list[0],'+int',1])
        if p[2]=="--":
            p[0].code.append([p[1].expr_list[0],"=",p[1].expr_list[0],'-int',1])
    else:
        if p[2]=="++":
            var1 = create_temp()
            p[0].code.append([var1,"=","*",p[1].expr_list[0]])
            p[0].code.append([var1,"=",var1,'+int',1])
            p[0].code.append(["*",p[1].expr_list[0],"=",var1])
        if(p[2]=="--"):
            var1 = create_temp()
            p[0].code.append([var1,"=","*",p[1].expr_list[0]])
            p[0].code.append([var1,"=",var1,'-int',1])
            p[0].code.append(["*",p[1].expr_list[0],"=",var1])
    p[0].expr_type_list=[]

def p_assignment(p):
    '''Assignment : ExpressionList assign_op ExpressionList'''
    p[0] = Node('Assignment')
    for i in range(0,len(p[3].expr_type_list)):
        if(p[2].data["op"] == "="):
            if  not ( p[1].expr_type_list[i][0] in basic_types_list or p[1].expr_type_list[i][0] == "pointer"):
                errors.add_error('TypeError', p.lineno(1), "Type Mismatch: Cannot assign non-addressable value to addressable value")
        else:
            if(p[1].expr_type_list[i][0] not in basic_types_list):
                errors.add_error('TypeError', p.lineno(1), "Invalid Assignment")
    if p[1].data["memory"] == 0:
        errors.add_error('Type Error', p.lineno(1), 'Assignment not allowed for this expression list')
    if len(p[1].expr_type_list) != len(p[3].expr_type_list):
        errors.add_error('Type Error', p.lineno(1), 'Imbalanced assignment')

    for i in range(0,len(p[1].expr_type_list)):
        if p[1].expr_type_list[i] != p[3].expr_type_list[i]:
            errors.add_error('Type Error', p.lineno(1), "Mismatch of type for "+str(p[1].expr_type_list[i])+" and " +str(p[3].expr_type_list[i]))
    p[0].code += p[1].code + p[3].code
    for i in range (0,len(p[1].expr_type_list)):
        temp = None
        if p[2].expr_type_list[0][0]!="=":
            temp = check_operation(p[1].expr_type_list[i], [p[2].expr_type_list[0][0][0:-1]],p[3].expr_type_list[i])
            if(temp == None):
                errors.add_error('Type Error', p.lineno(1), "Invalid operation")
        if temp != None:
            p[2].expr_type_list[0] = [p[2].expr_type_list[0][0]+temp[0]]
        if p[1].data["dereflist"][i]==1:
            if p[3].data["dereflist"][i]==1:
                var1 = create_temp()
                p[0].code.append([var1,"=","*",p[3].expr_list[i]])
                p[0].code.append(["*",p[1].expr_list[i],p[2].expr_type_list[0][0],var1])
            else:
                p[0].code.append(["*",p[1].expr_type_list[i],p[2].expr_type_list[0][0],p[3].expr_list[i]])
        else:
            if(p[3].data["dereflist"][i]==1):
                var1 = create_temp()
                p[0].code.append([var1,"=","*",p[3].expr_list[i]])
                p[0].code.append([p[1].expr_list[i],p[2].expr_type_list[0][0],var1])
            else:
                p[0].code.append([p[1].expr_list[i],p[2].expr_type_list[0][0],p[3].expr_list[i]])
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

def p_if_stmt(p):
    '''IfStmt : IF OpenScope Expression Block CloseScope
    | IF OpenScope SimpleStmt SEMICOLON Expression Block CloseScope
    | IF OpenScope Expression Block CloseScope ELSE OpenScope IfStmt CloseScope
    | IF OpenScope Expression Block CloseScope ELSE OpenScope Block CloseScope
    | IF OpenScope SimpleStmt SEMICOLON Expression Block CloseScope ELSE OpenScope IfStmt CloseScope
    | IF OpenScope SimpleStmt SEMICOLON Expression Block CloseScope ELSE OpenScope Block CloseScope'''
    
    if len(p) == 6:
        if p[3].expr_type_list[0][0] != "bool" or len(p[3].expr_type_list)>1:
            errors.add_error('Type Error', p.lineno(1), "The type of expression in if is not boolean")
        p[0] = Node('IfStmt')
        p[0].code += p[3].code
        label = create_label()
        p[0].code.append(['ifnot', p[3].expr_list[0], 'goto', label])
        p[0].code += p[4].code
        p[0].code.append([label, ': '])

    elif len(p) == 8:
        if p[5].expr_type_list[0][0] != "bool" or len(p[5].expr_type_list)>1:
            errors.add_error('Type Error', p.lineno(1), "The type of expression in if is not boolean")
        p[0] = Node('IfStmt')
        p[0].code += p[3].code
        p[0].code += p[5].code
        label = create_label()
        p[0].code.append(['ifnot', p[5].expr_list[0], 'goto', label])
        p[0].code += p[6].code
        p[0].code.append([label, ': '])

    elif len(p) == 10:
        if p[3].expr_type_list[0][0] != "bool" or len(p[3].expr_type_list)>1:
            errors.add_error('Type Error', p.lineno(1), "The type of expression in if is not boolean")
        p[0] = Node('IfStmt')
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
        if p[5].expr_type_list[0][0] != "bool" or len(p[5].expr_type_list)>1:
            errors.add_error('Type Error', p.lineno(1), "The type of expression in if is not boolean")
        p[0] = Node('IfStmt')
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


# def p_switch_stmt(p):
#     '''SwitchStmt : ExprSwitchStmt''' 
#     # ''' | TypeSwitchStmt'''
#     p[0] = p[1]

def p_expr_switch_stmt(p):
    '''SwitchStmt : SWITCH LEFT_BRACE OpenSwitch ExprCaseClauseStar CloseSwitch RIGHT_BRACE
    | SWITCH SimpleStmt SEMICOLON LEFT_BRACE OpenSwitch ExprCaseClauseStar CloseSwitch RIGHT_BRACE
    | SWITCH SimpleStmt SEMICOLON ExpressionName LEFT_BRACE OpenSwitch ExprCaseClauseStar CloseSwitch RIGHT_BRACE
    | SWITCH ExpressionName LEFT_BRACE OpenSwitch ExprCaseClauseStar CloseSwitch RIGHT_BRACE'''
    p[0] = Node('ExprSwitchStmt')
    label = create_label(2)
    global curr_switch_type, end_for
    if len(p) == 7:
        p[0].code += p[4].code
    elif len(p) == 8:
        p[0].code += p[2].code
        p[0].code += p[5].code

    elif len(p) == 10:
        p[0].code += p[2].code
        p[0].code += p[4].code
        p[0].code += p[7].code
    else:
        p[0].code += p[2].code
        p[0].code += p[6].code
    p[0].code.append([end_for[-1], ': '])
    end_for = end_for[0: -1]

def p_ExpressionName(p):
    """ExpressionName : Expression"""
    p[0] = p[1]
    global switch_exp, curr_switch_type
    if len(p[1].expr_type_list)>1:
        errors.add_error('Type Error', p.lineno(1), "The type of expression in switch is not a single type")
    if p[1].expr_type_list[0][0]!="int" and p[1].expr_type_list[0][0]!="rune" and p[1].expr_type_list[0][0]!="bool":
        errors.add_error('Type Error', p.lineno(1), "The type of expression in switch is not an integer, rune or boolean")
    curr_switch_type = p[1].expr_type_list[0][0]
    switch_expr = p[0].expr_list[0]
    label1 = create_label(2)


def p_expr_case_clause_star(p):
    '''ExprCaseClauseStar : ExprCaseClauseStar ExprCaseClause 
    | ExprCaseClause'''
    if len(p) > 2:
        p[0] = p[1]
        p[0].code += p[2].code
    else:
        p[0] = p[1]

#Changed grammar after parser
def p_expr_case_clause(p):
    '''ExprCaseClause : OpenScope CASE ExpressionList COLON StatementList CloseScope
    | DEFAULT COLON OpenScope StatementList CloseScope'''
    if len(p) == 6:
        p[0] = Node('DefClause')
        p[0].code += p[4].code
    else:
        p[0] = Node('ExprCaseClause')
        for i in range(0,len(p[3].expr_type_list)):
            if p[3].expr_type_list[i][0]!="int" and p[3].expr_type_list[i][0]!="rune":
                errors.add_error('Type Error', p.lineno(1), "The type of expression in switch is not an integer or rune")
            if curr_switch_type is not None and curr_switch_type != p[3].expr_type_list[i][0]:
                errors.add_error('Type Error', p.lineno(1), "The type of expression in case does not match type of expression in switch")
            var = create_temp()
            label = create_label()
            p[0].code.append([var, '=', switch_expr, '==', p[3].expr_list[i]])
            p[0].code.append(['ifnot', var, 'goto', label])
            p[0].code += p[5].code
            p[0].code.append(['goto', end_for[-1]])
            p[0].code.append([label, ': '])
        p[0].code.append(['goto', end_for[-1]])

def p_for_stmt(p):
    '''ForStmt : FOR OpenScope OpenFor ForClause Block CloseFor CloseScope
    | FOR OpenScope OpenFor Expression Block CloseFor CloseScope
    | FOR OpenScope OpenFor Block CloseFor CloseScope'''
    # | FOR OpenScope OpenFor RangeClause Block CloseFor CloseScope'''
    
    global start_for,end_for
    p[0] = Node("ForStmt")
    p[0].code.append([start_for[-1], ': '])
    if len(p)==8 and p[4].data.get("forclause") is not None:
        p[0].code = p[4].code
        p[0].code += p[5].code
        p[0].code += p[4].data["for_label_pass"]

    # elif len(p) == 8 and p[4].data.get("rangeclause") is not None:
    #     p[0].code = p[4].code
    #     p[0].code += p[5].code
    #     p[0].code += p[4].data["for_label_pass"] 

    elif len(p)==8:
        if len(p[4].expr_type_list)>1 or p[4].expr_type_list[0][0]!="bool":
            errors.add_error('Type Error', p.lineno(1), "The type of expression in for loop is not a boolean")
        label1 = create_label()
        # print("hello")
        label2 = create_label()
        p[0].code += p[4].code
        p[0].code.append([label2,": "])
        p[0].code.append(["ifnot", p[4].expr_list[0], "goto", label1])
        p[0].code += p[5].code
        p[0].code.append(["goto",label2])
        p[0].code.append([label1,":"])

    else:
        label1 = create_label()
        p[0].code.append([label1,":"])
        p[0].code += p[4].code
        p[0].code.append(["goto",label1])

    p[0].code.append([end_for[-1],":"])
    start_for=start_for[0:-1]
    end_for=end_for[0:-1]

def p_for_clause(p):
    '''ForClause : SimpleStmt SEMICOLON Expression SEMICOLON SimpleStmt
    | SimpleStmt SEMICOLON SEMICOLON SimpleStmt'''
    
    p[0] = Node('ForClause')
    p[0].data["forclause"] = 1
    if len(p) == 6 and len(p[3].expr_type_list) > 1 or p[3].expr_type_list[0][0] != "bool":
        errors.add_error('Type Error', p.lineno(1), "The type of expression in for loop is not a boolean")
    p[0].code = p[1].code
    p[0].code.append([start_for[-1],":"])
    label1 = create_label()
    p[0].code.append([label1,":"])
    if len(p)==6:
        label2=create_label()
        p[0].code += p[3].code
        p[0].code.append(["ifnot", p[3].expr_list[0],"goto",label2])
        p[0].data["for_label_pass"] = []
        p[0].data["for_label_pass"] += p[5].code
        p[0].data["for_label_pass"].append(["goto",label1])
        p[0].data["for_label_pass"].append([label2,":"])
    else:
        p[0].data["for_label_pass"] = []
        p[0].data["for_label_pass"] += p[4].code
        p[0].data["for_label_pass"].append(["goto",label1])

# def p_range_clause(p):
#     '''RangeClause : RANGE Expression
#     | IdentifierList DEFINE RANGE Expression
#     | ExpressionList ASSIGNMENT RANGE Expression'''
#     p[0] = ['RangeClause']
#     for idx in range(1,len(p)):
#         if isinstance(p[idx],str) and p[idx]!=";":
#             p[0].append([p[idx]])
#         elif p[idx]!=";":
#             p[0].append(p[idx])
 
def p_returnstmt(p):
    '''ReturnStmt : RETURN ExpressionList
    | RETURN'''
    # print(curr_scope)
    # print(curr_func)
    # print(scope_table[0])
    if len(p) == 2 and scope_table[0].table[curr_func]['return_type'] != [["void"]]:
        errors.add_error('Type Error',p.lineno(1), "Return statement without return value")
    elif len(p) == 3 and scope_table[0].table[curr_func]['return_type'] != p[2].expr_type_list:
        errors.add_error('Type Error', p.lineno(1), "Return statement with wrong return value")
    elif curr_scope == 0:
        errors.add_error('Scope Error', p.lineno(1), "Return statement is not inside a function")
    p[0] = Node('ReturnStmt')

    if len(p) == 2:
        p[0].code = [["return"]]
    else:
        p[0].code = p[2].code +  [["return"]]
        

    

#---------------------------------
def p_break_stmt(p):
    '''BreakStmt : BREAK IDENT
                | BREAK'''
    if open_for == 0 and open_switch == 0:
        errors.add_error('Scope Error', p.lineno(1), "Break statement can only exist inside a loop")
    p[0] = Node('BreakStmt')
    p[0].code.append(['goto', end_for[-1]])
#-------------------------------------
def p_continue_stmt(p):
    '''ContinueStmt : CONTINUE IDENT
                | CONTINUE'''
    if open_for == 0 and open_switch == 0:
        errors.add_error('Scope Error', p.lineno(1), "Continue statement can only exist inside a loop")
    p[0] = Node('ContinueStmt')
    p[0].code.append(['goto', start_for[-1]])

# def p_goto_stmt(p):
#     '''GotoStmt : GOTO IDENT'''
#     p[0] = ['GotoStmt', [p[1]], [p[2]]]
# def p_fallthrough_stmt(p):
#     '''FallthroughStmt : FALLTHROUGH'''
#     p[0] = [p[1]]



def p_error(p):
 if p:
      print("Syntax error at line no:", p.lineno, "at position", p.lexpos, "in the code.   " "TOKEN VALUE=", p.value,  "TOKEN TYPE=" ,p.type)
      parser.errok()
 else:
      print("Syntax error at EOF")


tokens = lexer.tokens
lexer = lex.lex()
#-------------------------------------------------------------------------------------
file = open(sys.argv[1], 'r')
data = file.read()
parser = yacc.yacc(debug=True)
res = parser.parse(data, lexer=lexer)
import pprint
# pprint.pprint(res)
