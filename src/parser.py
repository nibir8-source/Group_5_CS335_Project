import sys
import ply.yacc as yacc
from ply.lex import TOKEN
import sys
import lexer
from lexer import * 
from data_structures import SymTable
from data_structures import Node
from data_structures import Errors

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
scope_list = [0]
scope_table= {}
scope_table[0] = SymTable()
open_for = 0
open_switch = 0
curr_func = 0
errors = Errors()
start_for = []
end_for = []

def open_scope():
    global curr_scope
    prev_scope = curr_scope
    curr_scope += 1
    scope_list.append(curr_scope)
    scope_table[curr_scope] = SymTable()
    scope_table[curr_scope].set_parent(prev_scope)


def close_scope():
    global curr_scope
    curr_scope = scope_list[-2] 
    scope_list.pop()



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

def p_close_for(p):
    '''CloseFor : '''
    global open_for
    open_for -= 1

def p_open_switch(p):
    '''OpenSwitch : '''
    global open_switch
    open_switch += 1

def p_close_switch(p):
    '''CloseSwitch : '''
    global open_switch
    open_switch -= 1


#----------------------------------------------------------------------------------------
def p_source_file(p):
    '''SourceFile  : PackageClause SEMICOLON ImportDeclStar TopLevelDeclStar'''
    p[0].code = p[1].code + p[3].code + p[4].code
    # p[0] = ['SourceFile', p[1], p[3], p[4]]

def p_import_decl_star(p):
    '''ImportDeclStar : ImportDeclStar ImportDecl SEMICOLON 
    |'''
    p[0] = Node()
    if(len(p)>1):
        p[0].code+=p[1].code
        p[0].code+=p[2].code
    # if len(p) == 1:
    #     p[0] = []
    # else:
    #     p[0] = ['ImportDeclStar', p[1], p[2]]

def p_top_level_decl_star(p):
    '''TopLevelDeclStar : TopLevelDeclStar TopLevelDecl SEMICOLON 
    |'''
    p[0] = Node()
    if(len(p)>1):
        p[0].code+=p[1].code
        p[0].code+=p[2].code
    # if len(p) == 1:
    #     p[0] = []
    # else:
    #     p[0] = ['TopLevelDeclStar', p[1], p[2]]

def p_package_clause(p):
    '''PackageClause : PACKAGE IDENT'''
    p[0] = ['PackageClause', [p[2]]]
def p_import_decl(p):
    '''ImportDecl : IMPORT ImportSpec 
                    | IMPORT LEFT_PARENTHESIS ImportSpecSemicolonStar RIGHT_PARENTHESIS'''
    if len(p)==3:
        p[0]=p[2]
    else:
        p[0]=p[3]
def p_import_spec_semicolon_star(p):
    '''ImportSpecSemicolonStar : ImportSpecSemicolonStar ImportSpec SEMICOLON 
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['ImportSpecSemicolonStar', p[1], p[2]]
def p_import_spec(p):
    '''ImportSpec : PERIOD ImportPath
                    | IDENT ImportPath
                    | ImportPath'''
    if(len(p)==2):
        p[0]=p[1]                             
    else:
        p[0]=['ImportSpec',[p[1]],p[2]]
def p_import_path(p):
    '''ImportPath : STRING'''
    p[0] = p[1]

#-----------------------------------------------------------------------------
def p_top_level_decl(p):
    '''TopLevelDecl : Declaration 
    | FunctionDecl'''
    p[0] = p[1]
def p_declaration(p):
    '''Declaration : ConstDecl 
    | TypeDecl 
    | VarDecl'''
    p[0] = p[1]
def p_const_decl(p):
    '''ConstDecl : CONST ConstSpec
                | CONST LEFT_PARENTHESIS ConstSpecStar RIGHT_PARENTHESIS'''
    if len(p)==3:
        p[0]=p[2]
    else:
        p[0]=p[3]
def p_const_spec_star(p):
    '''ConstSpecStar : ConstSpecStar ConstSpec SEMICOLON
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['ConstSpecStar', p[1], p[2]]
def p_const_spec(p):
    '''ConstSpec : IdentifierList
                | IdentifierList ASSIGNMENT ExpressionList
                | IdentifierList Type ASSIGNMENT ExpressionList
                | IdentifierList IDENT ASSIGNMENT ExpressionList
                | IdentifierList IDENT PERIOD IDENT ASSIGNMENT ExpressionList'''
    if len(p)==2:
        p[0]=p[1]
    elif (len(p)==4):
        p[0]=['ConstSpec', p[1], [p[2]], p[3] ]
    elif len(p) == 7:
        p[0]=['ConstSpec', p[1], [p[2]], [p[3]], [p[4]], [p[5]], p[6]]
    elif isinstance(p[1],str):
        p[0]=['ConstSpec', [p[1]], [p[2]], [p[3]], p[4]]
    else:
        p[0]=['ConstSpec', [p[1]], p[2], [p[3]], p[4]]
def p_identifier_list(p):
    '''IdentifierList : IDENT
    | IDENT COMMA IdentifierList'''
    if len(p)==2:
        p[0]=[p[1]]
    else:
        p[0]=['IdentifierList', [p[1]], p[2]]
def p_expression_list(p):
    '''ExpressionList : Expression
    | ExpressionList COMMA Expression'''
    if len(p)==2:
        p[0]=p[1]
    else:
        p[0]=['ExpressionList', p[1], p[3]]
def p_type_decl(p):
    '''TypeDecl : TYPE TypeDef
                | TYPE LEFT_PARENTHESIS TypeDefStar RIGHT_PARENTHESIS'''
    if len(p)==3:
        p[0]=['TypeDecl', [p[1]], p[2]]
    else:
        p[0]=['TypeDecl', [p[1]], p[3]]
def p_type_spec_star(p):
    '''TypeDefStar : TypeDef SEMICOLON TypeDefStar
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['TypeDefStar', p[1], p[2]]
def p_type_def(p):
    '''TypeDef : IDENT Type
    | IDENT IDENT PERIOD IDENT
    | IDENT IDENT'''
    if len(p)==5:
        p[0] = ['TypeDef', [p[1]], [p[2]], [p[3]], [p[4]]]
    elif isinstance(p[2], str):
        p[0] = ['TypeDef', [p[1]], [p[2]]]
    else:
        p[0] = ['TypeDef', [p[1]], p[2]]
    
def p_var_decl(p):
    '''VarDecl : VARIABLE VarSpec
    | VARIABLE LEFT_PARENTHESIS VarSpecStar RIGHT_PARENTHESIS'''   
    if len(p) == 3:
        p[0] = ['VarDecl', [p[1]], p[2]]
    else:
        p[0] = ['VarDecl', [p[1]], p[3]]
def p_var_spec_star(p):
    '''VarSpecStar : VarSpec SEMICOLON VarSpecStar
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['VarSpecStar', p[1], p[2]]
def p_var_spec(p):
    '''VarSpec : IdentifierList Type 
                | IdentifierList Type ASSIGNMENT Expression
                | IdentifierList IDENT ASSIGNMENT ExpressionList
                | IdentifierList IDENT PERIOD IDENT ASSIGNMENT ExpressionList
                | IdentifierList IDENT PERIOD IDENT
                | IdentifierList IDENT
                | IdentifierList ASSIGNMENT ExpressionList'''
    p[0] = ['VarSpec']
    for idx in range(1,len(p)):
      if(isinstance(p[idx],str)):
        p[0].append([p[idx]])
      else:
        p[0].append(p[idx])
def p_short_var_decl(p):
    '''ShortVarDecl : IdentifierList DEFINE ExpressionList'''
    p[0] = ['ShortVarDecl', p[1], [p[2]], p[3]]
def p_function_decl(p):
    '''FunctionDecl : FUNCTION IDENT Signature Block
                    | FUNCTION IDENT Signature'''
    if len(p) == 4:
        p[0] = ['FunctionDecl', [p[2]], p[3]]
    else:
        p[0] = ['FunctionDecl', [p[2]], p[3], p[4]]

# --------------------- TYPES -------------------------------------
def p_type(p):
    '''Type : LEFT_PARENTHESIS IDENT RIGHT_PARENTHESIS
    | LEFT_PARENTHESIS IDENT PERIOD IDENT RIGHT_PARENTHESIS
    | TypeLit 
    | LEFT_PARENTHESIS Type RIGHT_PARENTHESIS'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4 and isinstance(p[2], str):
        p[0] = [p[2]]
    elif len(p) == 4 and not isinstance(p[2], str):
        p[0] = p[2]
    else:
        p[0] = ['Type', [p[1]], [p[2]], [p[3]]]
def p_type_lit(p):
    '''TypeLit : ArrayType 
    | StructType 
    | PointerType 
    | FunctionType 
    | SliceType 
    | MapType'''
    p[0] = p[1]
def p_array_type(p):
    '''ArrayType : LEFT_BRACKET Expression RIGHT_BRACKET Type
                | LEFT_BRACKET Expression RIGHT_BRACKET IDENT
                | LEFT_BRACKET Expression RIGHT_BRACKET IDENT PERIOD IDENT'''    
    p[0] = ['ArrayType']
    for idx in range(1,len(p)):
        if p[idx] == '[' or p[idx] == ']' or p[idx] == ';':
            continue
        if isinstance(p[idx],str):
            p[0].append([p[idx]])
        else:
            p[0].append(p[idx])
def p_slice_type(p):
    '''SliceType : LEFT_BRACKET RIGHT_BRACKET Type
    | LEFT_BRACKET RIGHT_BRACKET IDENT PERIOD IDENT
    | LEFT_BRACKET RIGHT_BRACKET IDENT'''
    p[0] = ['SliceType']
    for idx in range(1,len(p)):
        if p[idx] == '[' or p[idx] == ']':
            continue
        if isinstance(p[idx],str):
            p[0].append([p[idx]])
        else:
            p[0].append(p[idx])
def p_struct_type(p):
    '''StructType : STRUCT LEFT_BRACE FieldDeclStar RIGHT_BRACE'''
    p[0] = ['StructType', [p[1]], p[3]]
# --------------------------------------------------------------------
def p_field_decl_star(p):
    '''FieldDeclStar : FieldDeclStar FieldDecl SEMICOLON
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['FieldDeclStar', p[1], p[2]]
def p_field_decl(p):
    '''FieldDecl : IdentifierList Type Tag
    | IdentifierList IDENT Tag
    | IdentifierList IDENT PERIOD IDENT Tag
    | IdentifierList Type 
    | IdentifierList IDENT
    | IdentifierList IDENT PERIOD IDENT
    | EmbeddedField Tag
    | EmbeddedField'''
    p[0] = ['FieldDecl']
    for idx in range(1,len(p)):
        if isinstance(p[idx],str):
            p[0].append([p[idx]])
        else:
            p[0].append(p[idx])
def p_embedded_field(p):
    '''EmbeddedField : MULTIPLY IDENT 
    | MULTIPLY IDENT PERIOD IDENT 
    | IDENT
    | IDENT PERIOD IDENT'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = ['EmbeddedField']
        for index in range(1,len(p)):
            p[0].append([p[index]])
def p_tag(p):
    '''Tag : STRING'''
    p[0] = [p[1]]
def p_pointer_type(p):
    '''PointerType : MULTIPLY Type
        | MULTIPLY IDENT
        | MULTIPLY IDENT PERIOD IDENT'''
    p[0] = ['PointerType', [p[1]], p[2]]
def p_function_type(p):
    '''FunctionType : FUNCTION Signature'''
    p[0] = ['FunctionType', [p[0]], p[1]]
def p_signature(p):
    '''Signature : Parameters Result
    | Result'''
    if len(p) == 2:
        p[0] = p[1]
    else: 
        p[0] = ['Signature', p[1], p[2]]
def p_result(p):
    '''Result : Parameters 
    | Type
    | IDENT
    | IDENT PERIOD IDENT'''
    if len(p) == 2:
        if isinstance(p[1],str):
            p[0] = [p[1]]
        else:
            p[0] = p[1]
    else:
        p[0] = ['Result', [p[1]], [p[2]], [p[3]]]
def p_parameters(p):
    '''Parameters : LEFT_PARENTHESIS RIGHT_PARENTHESIS
                | LEFT_PARENTHESIS ParameterList RIGHT_PARENTHESIS
                | LEFT_PARENTHESIS ParameterList COMMA RIGHT_PARENTHESIS'''
    if len(p) == 3:
        p[0] = []
    else:
        p[0] = ['Parameters', p[2]]
def p_parameter_list(p):
    '''ParameterList : ParameterDecl 
    | ParameterList COMMA ParameterDecl
    | ParameterList COMMA Type
    | ParameterList COMMA IDENT
    | ParameterList COMMA IDENT PERIOD IDENT'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ['ParameterList', p[1], p[3]]

def p_ParameterDecl(p):
    '''ParameterDecl : IdentifierList Type
    | IdentifierList IDENT
    | IdentifierList IDENT PERIOD IDENT'''
    p[0]=['ParameterDecl']
    for index in range(1,len(p)):
      if isinstance(p[index],str):
        p[0].append([p[index]])
      else:
        p[0].append(p[index])
#--------------------------------------------------------------------
def p_MapType(p):
    '''MapType : MAP LEFT_BRACKET Type RIGHT_BRACKET Type
    | MAP LEFT_BRACKET Type RIGHT_BRACKET IDENT
    | MAP LEFT_BRACKET Type RIGHT_BRACKET IDENT PERIOD IDENT
    | MAP LEFT_BRACKET IDENT RIGHT_BRACKET Type
    | MAP LEFT_BRACKET IDENT RIGHT_BRACKET IDENT
    | MAP LEFT_BRACKET IDENT RIGHT_BRACKET IDENT PERIOD IDENT
    | MAP LEFT_BRACKET IDENT PERIOD IDENT RIGHT_BRACKET Type
    | MAP LEFT_BRACKET IDENT PERIOD IDENT RIGHT_BRACKET IDENT
    | MAP LEFT_BRACKET IDENT PERIOD IDENT RIGHT_BRACKET IDENT PERIOD IDENT'''
    p[0]=['MapType']
    for index in range(1,len(p)):
      if(isinstance(p[index],str) and p[index]!="[" and p[index]!="]" and p[index]!="map"):
        p[0].append([p[index]])
      elif(p[index]!="[" and p[index]!="]" and p[index]!="map"):
        p[0].append(p[index])
def p_block(p):
    '''Block : LEFT_BRACE StatementList RIGHT_BRACE'''
    p[0] = p[2]
def p_statement_list(p):
    '''StatementList : StatementList Statement SEMICOLON
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['StatementList', p[1], p[2]]
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
        p[0] = ['Expression', p[1], p[2], p[3]]
def p_unary_expr(p):
    '''UnaryExpr : PrimaryExpr 
    | unary_op UnaryExpr'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ['UnaryExpr', p[1], p[2]]
   
def p_unary_op(p):
    '''unary_op : ADD 
    | SUBTRACT 
    | NOT 
    | XOR 
    | MULTIPLY 
    | AND 
    | ARROW'''
    p[0] = [p[1]]
def p_literal(p):
    '''Literal : BasicLit 
    | CompositeLit 
    | FunctionLit'''
    p[0] = p[1]
def p_basic_lit(p):
    '''BasicLit : INT 
    | FLOAT 
    | IMAGINARY 
    | RUNE 
    | STRING'''
    p[0] = [p[1]]   


def p_primary_expr(p):
    '''PrimaryExpr : IDENT
    | LEFT_PARENTHESIS Expression RIGHT_PARENTHESIS
    | IDENT PERIOD IDENT
    | Literal
    | PrimaryExpr Selector 
    | PrimaryExpr Index 
    | PrimaryExpr Slice 
    | PrimaryExpr Arguments'''
    p[0] = ['PrimaryExpr']
    for idx in range(1,len(p)):
        if isinstance(p[idx],str) and p[idx]!="(" and p[idx]!=")":
            p[0].append([p[idx]])
        elif p[idx]!="(" and p[idx]!=")":
            p[0].append(p[idx])
def p_selector(p):
    '''Selector : PERIOD IDENT'''
    p[0] = ['Selector', [p[1]], [p[2]]]
def p_index(p):
    '''Index : LEFT_BRACKET Expression RIGHT_BRACKET'''
    p[0] = p[2]
def p_slice(p):
    '''Slice : LEFT_BRACKET Expression COLON Expression RIGHT_BRACKET
    | LEFT_BRACKET Expression COLON RIGHT_BRACKET
    | LEFT_BRACKET COLON Expression RIGHT_BRACKET
    | LEFT_BRACKET COLON RIGHT_BRACKET 
    | LEFT_BRACKET Expression COLON Expression COLON Expression RIGHT_BRACKET
    | LEFT_BRACKET COLON Expression COLON Expression RIGHT_BRACKET'''
    p[0] = ['Slice']
    for idx in range(1,len(p)):
        if p[idx] == '[' or p[idx] == ']' or p[idx] == ':':
            continue
        if isinstance(p[idx],str):
            p[0].append([p[idx]])
        else:
            p[0].append(p[idx])
def p_arguments(p):
    '''Arguments : LEFT_PARENTHESIS RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS ExpressionList RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS ExpressionList COMMA RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS Type RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS Type COMMA RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS Type COMMA ExpressionList RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS Type COMMA ExpressionList COMMA RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS IDENT RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS IDENT COMMA RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS IDENT COMMA ExpressionList RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS IDENT COMMA ExpressionList COMMA RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS IDENT PERIOD IDENT RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS IDENT PERIOD IDENT COMMA RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS IDENT PERIOD IDENT COMMA ExpressionList RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS IDENT PERIOD IDENT COMMA ExpressionList COMMA RIGHT_PARENTHESIS'''
    p[0] = ['Arguments']
    for idx in range(1,len(p)):
        if isinstance(p[idx],str) and p[idx]!="(" and p[idx]!=")" and p[idx] != ",":
            p[0].append([p[idx]])
        elif p[idx]!="(" and p[idx]!=")" and p[idx] != ",":
            p[0].append(p[idx])
# def p_method_expr(p):
#     """MethodExpr : Type PERIOD IDENT
#                | IDENT PERIOD IDENT
#                | IDENT PERIOD IDENT PERIOD IDENT"""
#     p[0]=['MethodExpr']
#     for idx in range(1,len(p)):
#         if p[idx] == 'chan':
#             continue
#         if isinstance(p[idx],str):
#             p[0].append([p[idx]])
#         else:
#             p[0].append(p[idx])

# def p_conversion(p):
#     '''Conversion : Type LEFT_PARENTHESIS Expression COMMA RIGHT_PARENTHESIS
#     | Type LEFT_PARENTHESIS Expression LEFT_PARENTHESIS
#     | IDENT LEFT_PARENTHESIS Expression RIGHT_PARENTHESIS
#     | IDENT LEFT_PARENTHESIS Expression COMMA RIGHT_PARENTHESIS
#     | IDENT PERIOD IDENT LEFT_PARENTHESIS Expression RIGHT_PARENTHESIS
#     | IDENT PERIOD IDENT LEFT_PARENTHESIS Expression COMMA RIGHT_PARENTHESIS'''
#     p[0] = ['Conversion']
#     for idx in range(1,len(p)):
#         if p[idx] == '(' or p[idx] == ')' or p[idx] == ',':
#             continue
#         if isinstance(p[idx],str):
#             p[0].append([p[idx]])
#         else:
#             p[0].append(p[idx])

def p_composite_lit(p):
    '''CompositeLit : StructType LiteralValue
                | ArrayType LiteralValue
                | SliceType LiteralValue
                | MapType LiteralValue
                | IDENT LiteralValue
                | IDENT PERIOD IDENT LiteralValue'''
    p[0] = ['CompositeLit']
    for idx in range(1,len(p)):
        if isinstance(p[idx],str) and p[idx]!="[" and p[idx]!="]" and p[idx]!=",":
            p[0].append([p[idx]])
        elif p[idx]!="[" and p[idx]!="]" and p[idx]!=",":
            p[0].append(p[idx])
def p_literal_value(p):
    '''LiteralValue : LEFT_BRACE RIGHT_BRACE
                    | LEFT_BRACE ElementList RIGHT_BRACE
                    | LEFT_BRACE ElementList COMMA RIGHT_BRACE'''
    if len(p) == 3:
        p[0] = []
    else:
        p[0] = p[2]
def p_element_list(p):
    '''ElementList : KeyedElement 
    | ElementList COMMA KeyedElement'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ['ElementList', p[1], p[3]]
def p_keyed_element(p):
    '''KeyedElement : Element
                    | IDENT COLON Element
                    | Expression COLON Element
                    | LiteralValue COLON Element'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ['KeyedElement']
        for idx in range(1,len(p)):
            if(isinstance(p[idx],str)):
                p[0].append([p[idx]])
            else:
                p[0].append(p[idx])
def p_element(p):
    '''Element : Expression 
    | LiteralValue'''
    p[0] = p[1]
def p_function_lit(p):
    '''FunctionLit : FUNCTION Signature Block'''
    p[0] = ['FunctionLit', p[2], p[3]]

#----------------------------------------------------------
def p_statement(p):
    '''Statement : Declaration 
    | LabeledStmt 
    | SimpleStmt 
    | ReturnStmt 
    | BreakStmt 
    | ContinueStmt 
    | GotoStmt 
    | FallthroughStmt 
    | OpenScope Block CloseScope 
    | IfStmt 
    | SwitchStmt 
    | ForStmt  '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_simple_stmt(p):
    '''SimpleStmt : ExpressionStmt 
    | IncDecStmt 
    | Assignment 
    | ShortVarDecl 
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0]=p[1]

def p_labeled_stmt(p):
    '''LabeledStmt : IDENT COLON Statement '''
    p[0] = ['LabeledStmt', [p[1]], [p[2]], p[3]]
def p_expression_stmt(p):
    '''ExpressionStmt : Expression'''
    p[0] = p[1]
def p_inc_dec_stmt(p):
    '''IncDecStmt : Expression INCREMENT
                    | Expression DECREMENT'''
    p[0] = ['InDecStmt', p[1], [p[2]]]
def p_assignment(p):
    '''Assignment : ExpressionList assign_op ExpressionList'''
    p[0] = ['Assignment', p[1], p[2], p[3]]
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
    p[0] = p[1]
def p_if_stmt(p):
    '''IfStmt : IF Expression Block
    | IF SimpleStmt SEMICOLON Expression Block
    | IF Expression Block ELSE IfStmt
    | IF Expression Block ELSE Block
    | IF SimpleStmt SEMICOLON Expression Block ELSE IfStmt
    | IF SimpleStmt SEMICOLON Expression Block ELSE Block'''
    p[0] = ['IfStmt']
    for idx in range(1,len(p)):
        if isinstance(p[idx],str) and p[idx]!=";":
            p[0].append([p[idx]])
        elif p[idx]!=";":
            p[0].append(p[idx])
def p_switch_stmt(p):
    '''SwitchStmt : ExprSwitchStmt 
    | TypeSwitchStmt'''
    p[0] = p[1]
def p_expr_switch_stmt(p):
    '''ExprSwitchStmt : SWITCH LEFT_BRACE ExprCaseClauseStar RIGHT_BRACE
    | SWITCH SimpleStmt SEMICOLON LEFT_BRACE ExprCaseClauseStar RIGHT_BRACE
    | SWITCH SimpleStmt SEMICOLON Expression LEFT_BRACE ExprCaseClauseStar RIGHT_BRACE
    | SWITCH Expression LEFT_BRACE ExprCaseClauseStar RIGHT_BRACE'''
    p[0]= ['ExprSwitchStmt']
    for idx in range(1,len(p)):
        if isinstance(p[idx],str) and p[idx]!=";" and p[idx] != "}" and p[idx] != "{":
            p[0].append([p[idx]])
        elif p[idx]!=";" and p[idx] != "}" and p[idx] != "{":
            p[0].append(p[idx])
def p_expr_case_clause_star(p):
    '''ExprCaseClauseStar : ExprCaseClauseStar ExprCaseClause 
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['ExprCaseClausePlus', p[1], p[2]]
def p_expr_case_clause(p):
    '''ExprCaseClause : ExprSwitchCase COLON StatementList'''
    p[0] = ['ExprCaseClause', p[1], [p[2]], p[3]]
def p_expr_switch_case(p):
    '''ExprSwitchCase : CASE ExpressionList 
    | DEFAULT'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = ['ExprSwitchCase', [p[1]], p[2]]
def p_type_switch_stmt(p):
    '''TypeSwitchStmt  : SWITCH TypeSwitchGuard LEFT_BRACE TypeCaseClauseStar RIGHT_BRACE
    | SWITCH SimpleStmt SEMICOLON TypeSwitchGuard LEFT_BRACE TypeCaseClauseStar RIGHT_BRACE'''
    p[0] = ['TypeSwitchstmt']
    for idx in range(1,len(p)):
        if isinstance(p[idx],str) and p[idx]!=";" and p[idx] != "}" and p[idx] != "{":
            p[0].append([p[idx]])
        elif p[idx]!=";" and p[idx] != "}" and p[idx] != "{":
            p[0].append(p[idx])
def p_type_case_clause_star(p):
    '''TypeCaseClauseStar : TypeCaseClauseStar TypeCaseClause 
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['TypeCaseClauseStar', p[1], p[2]]
def p_type_switch_guard(p):
    '''TypeSwitchGuard : IDENT DEFINE PrimaryExpr PERIOD LEFT_PARENTHESIS TYPE RIGHT_PARENTHESIS
    | PrimaryExpr PERIOD LEFT_PARENTHESIS TYPE RIGHT_PARENTHESIS'''
    p[0] = ['TypeSwitchGuard']
    for idx in range(1,len(p)):
        if isinstance(p[idx],str) and p[idx]!=";" and p[idx] != ")" and p[idx] != "(":
            p[0].append([p[idx]])
        elif p[idx]!=";" and p[idx] != "(" and p[idx] != ")":
            p[0].append(p[idx])
def p_type_case_clause(p):
    '''TypeCaseClause  : TypeSwitchCase COLON StatementList '''
    p[0] = ['TypeCaseClause', p[1], [p[2]], p[3]]
def p_type_switch_case(p):
    '''TypeSwitchCase : CASE TypeList 
    | DEFAULT'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = ['TypeSwitchCase', [p[1]], p[2]]
def p_type_list(p):
    '''TypeList : Type CommaTypeStar
    | IDENT CommaTypeStar
    | IDENT PERIOD IDENT CommaTypeStar'''
    p[0] = ['TypeList']
    for idx in range(1,len(p)):
        if p[idx] == ",":
            continue
        if isinstance(p[idx],str):
            p[0].append([p[idx]])
        else:
            p[0].append(p[idx])
   
def p_comma_type_star(p):
    '''CommaTypeStar : CommaTypeStar COMMA Type 
    | CommaTypeStar COMMA IDENT
    | CommaTypeStar COMMA IDENT PERIOD IDENT
    |'''
    p[0] = ['CommaTypeStar']
    for idx in range(1,len(p)):
        if p[idx] == ",":
            continue
        if isinstance(p[idx],str):
            p[0].append([p[idx]])
        else:
            p[0].append(p[idx])
def p_for_stmt(p):
    '''ForStmt : FOR ForClause Block
    | FOR RangeClause Block
    | FOR Expression Block
    | FOR Block'''
    p[0] = ['ForStmt']
    for idx in range(1,len(p)):
        if isinstance(p[idx],str):
            p[0].append([p[idx]])
        else:
            p[0].append(p[idx])
def p_for_clause(p):
    '''ForClause : SimpleStmt SEMICOLON Expression SEMICOLON SimpleStmt
    | SimpleStmt SEMICOLON SEMICOLON SimpleStmt'''
    p[0] = ['ForClause']
    for idx in range(1,len(p)):
        if isinstance(p[idx],str) and p[idx]!=";":
            p[0].append([p[idx]])
        elif p[idx]!=";":
            p[0].append(p[idx])
def p_range_clause(p):
    '''RangeClause : RANGE Expression
    | IdentifierList DEFINE RANGE Expression
    | ExpressionList ASSIGNMENT RANGE Expression'''
    p[0] = ['RangeClause']
    for idx in range(1,len(p)):
        if isinstance(p[idx],str) and p[idx]!=";":
            p[0].append([p[idx]])
        elif p[idx]!=";":
            p[0].append(p[idx])
 
def p_returnstmt(p):
    '''ReturnStmt : RETURN ExpressionList
                    | RETURN'''
    if len(p) == 2 and scope_table[curr_scope][curr_func]['return_type'] != "void":
        errors.add_error('Type Error',p.lineno(1), "Return statement without return value")
    elif len(p) == 3 and scope_table[curr_scope][curr_func]['return_type'] != p[2].type_list:
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

def p_goto_stmt(p):
    '''GotoStmt : GOTO IDENT'''
    p[0] = ['GotoStmt', [p[1]], [p[2]]]
def p_fallthrough_stmt(p):
    '''FallthroughStmt : FALLTHROUGH'''
    p[0] = [p[1]]



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
pprint.pprint(res)
