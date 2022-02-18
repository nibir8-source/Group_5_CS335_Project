import sys
import ply.yacc as yacc
from ply.lex import TOKEN
import sys
import lexer
from lexer import * 

precedence = (
    ('left','IDENT'),
    ('left','DEFINE'),
    ('left','COMMA'),
    ('left','LEFT_BRACKET'),
    ('left','RIGHT_BRACKET'),
    ('left','LEFT_BRACE'),
    ('left','RIGHT_BRACE'),
    ('left','ELLIPSIS'),
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
    ('right', 'ASSIGNMENT'),
    ('left', 'LOGICAL_OR'),
    ('left', 'LOGICAL_AND'),
    ('left', 'EQUAL', 'NOT_EQUAL', 'LESS_THAN', 'LESS_THAN_EQUAL', 'GREATER_THAN', 'GREATER_THAN_EQUAL'),
    ('left', 'ADD', 'SUBTRACT', 'OR', 'XOR'),
    ('left', 'MULTIPLY', 'QUOTIENT', 'REMAINDER', 'SHIFT_LEFT', 'SHIFT_RIGHT', 'AND', 'AND_NOT'),
    ('right', 'NOT'),
)

#----------------------------------------------------------------------------------------
def p_source_file(p):
    '''SourceFile  : PackageClause SEMICOLON ImportDeclStar TopLevelDeclStar'''
    p[0] = ['SourceFile', p[1], p[3], p[4]]
def p_import_decl_star(p):
    '''ImportDeclStar : ImportDeclStar ImportDecl SEMICOLON 
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['ImportDeclStar', p[1], p[2]]
def p_top_level_decl_star(p):
    '''TopLevelDeclStar : TopLevelDeclStar TopLevelDecl SEMICOLON 
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['TopLevelDeclStar', p[1], p[2]]
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
    | FunctionDecl 
    | MethodDecl'''
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
    '''IdentifierList : IDENT IdentifierListStar'''
    p[0]=['IdentifierList', [p[1]], p[2]]
def p_identifier_list_star(p):
    '''IdentifierListStar : COMMA IDENT IdentifierListStar
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['IdentifierListStar', [p[2]], p[3]]
def p_expression_list(p):
    '''ExpressionList : Expression ExpressionListStar'''
    p[0]=['ExpressionList', p[1], p[2]]
def p_expression_list_star(p):
    '''ExpressionListStar : COMMA Expression ExpressionListStar
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['ExpressionListStar', p[2], p[3]]
def p_type_decl(p):
    '''TypeDecl : TYPE TypeSpec
                | TYPE LEFT_PARENTHESIS TypeSpecStar RIGHT_PARENTHESIS'''
    if len(p)==3:
        p[0]=['TypeDecl', [p[1]], p[2]]
    else:
        p[0]=['TypeDecl', [p[1]], p[3]]
def p_type_spec_star(p):
    '''TypeSpecStar : TypeSpecStar TypeSpec SEMICOLON
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['TypeSpecStar', p[1], p[2]]
def p_type_spec(p):
    '''TypeSpec : AliasDecl 
    | TypeDef'''
    p[0] = p[1] 
def p_alias_decl(p):
    '''AliasDecl : IDENT ASSIGNMENT Type
    | IDENT ASSIGNMENT IDENT
    | IDENT ASSIGNMENT IDENT PERIOD IDENT'''
    p[0] = ['AliasDecl']
    for idx in range(1,len(p)):
        if isinstance(p[idx],str):
            p[0].append([p[idx]])
        else:
            p[0].append(p[idx])
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
    '''VarSpecStar : VarSpecStar VarSpec SEMICOLON 
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
def p_method_decl(p):
    '''MethodDecl : FUNCTION Receiver IDENT Signature Block
                    | FUNCTION Receiver IDENT Signature'''
    if len(p) == 5:
        p[0] = ['FunctionDecl', p[2], [p[3]], p[4]]
    else:
        p[0] = ['FunctionDecl', p[2], [p[3]], p[4], p[5]]
def p_receiver(p):
    '''Receiver : Parameters'''
    p[0] = p[1]

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
    | InterfaceType 
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
    '''ParameterList : ParameterDecl ParameterDeclStar'''
    p[0] = ['ParamterList', p[1], p[2]]
def p_parameter_decl_star(p):
    """ParameterDeclStar : COMMA ParameterDecl ParameterDeclStar
    |"""
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['ParameterDeclStar', p[2], p[3]]

def p_ParameterDecl(p):
    '''ParameterDecl : IdentifierList ELLIPSIS Type
    | IdentifierList ELLIPSIS IDENT
    | IdentifierList ELLIPSIS IDENT PERIOD IDENT
    | IdentifierList Type
    | IdentifierList IDENT
    | IdentifierList IDENT PERIOD IDENT
    | ELLIPSIS Type
    | ELLIPSIS IDENT
    | ELLIPSIS IDENT PERIOD IDENT
    | Type
    | IDENT
    | IDENT PERIOD IDENT'''
    p[0]=['ParameterDecl']
    for index in range(1,len(p)):
      if isinstance(p[index],str):
        p[0].append([p[index]])
      else:
        p[0].append(p[index])
#--------------------------------------------------------------------
def p_interface_type(p):
    '''InterfaceType : INTERFACE LEFT_BRACE MethodSpecStar RIGHT_BRACE'''
    p[0] = ['InterfaceType', [p[1]], p[3]]
def p_method_spec_star(p):
    '''MethodSpecStar : MethodSpecStar MethodSpec SEMICOLON
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['MethodSpecStar', p[1], p[2]]
def p_method_spec(p):
    '''MethodSpec : IDENT Signature
                    | IDENT
                    | IDENT PERIOD IDENT'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p)==3:
        p[0] = ['MethodSpec',[p[1]],p[2]]
    else:
        p[0] = ['MethodSpec',[p[1]],[p[2]],[p[3]]]
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
# def p_channel_type(p):
#     '''ChannelType : CHAN Type
#     | CHAN IDENT
#     | CHAN IDENT PERIOD IDENT
#     | CHAN ARROW Type
#     | CHAN ARROW IDENT
#     | CHAN ARROW IDENT PERIOD IDENT
#     | ARROW CHAN Type
#     | ARROW CHAN IDENT
#     | ARROW CHAN IDENT PERIOD IDENT
#     '''
#     p[0]=['ChannelType']
#     for index in range(1,len(p)):
#       if isinstance(p[index],str):
#         p[0].append([p[index]])
#       else:
#         p[0].append(p[index])
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
    | Expression binary_op Expression'''
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
def p_binary_op(p):
    '''binary_op : LOGICAL_OR 
    | LOGICAL_AND 
    | rel_op 
    | add_op 
    | mul_op'''
    p[0] = ['binary_op']
    if(isinstance(p[1],str)):
        p[0].append([p[1]])
    else:
        p[0].append(p[1])
def p_rel_op(p):
    '''rel_op : EQUAL 
    | NOT_EQUAL 
    | LESS_THAN 
    | LESS_THAN_EQUAL 
    | GREATER_THAN 
    | GREATER_THAN_EQUAL'''
    p[0] = [p[1]]
def p_add_op(p):
    '''add_op : ADD 
    | SUBTRACT 
    | OR 
    | XOR'''
    p[0] = [p[1]]
def p_mul_op(p):
    '''mul_op : MULTIPLY 
    | QUOTIENT 
    | REMAINDER 
    | SHIFT_LEFT 
    | SHIFT_RIGHT 
    | AND 
    | AND_NOT'''
    p[0] = [p[1]]
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
    | Conversion
    | PrimaryExpr Selector 
    | PrimaryExpr Index 
    | PrimaryExpr Slice 
    | PrimaryExpr TypeAssertion 
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

def p_type_assertion(p):
    '''TypeAssertion : PERIOD LEFT_PARENTHESIS Type RIGHT_PARENTHESIS
    | PERIOD LEFT_PARENTHESIS IDENT RIGHT_PARENTHESIS
    | PERIOD LEFT_PARENTHESIS IDENT PERIOD IDENT RIGHT_PARENTHESIS'''
    p[0] = ['TypeAssertion']
    for idx in range(1,len(p)):
        if isinstance(p[idx],str) and p[idx]!="(" and p[idx]!=")":
            p[0].append([p[idx]])
        elif p[idx]!="(" and p[idx]!=")":
            p[0].append(p[idx])
def p_arguments(p):
    '''Arguments : LEFT_PARENTHESIS RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS ExpressionList RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS ExpressionList COMMA RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS ExpressionList ELLIPSIS RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS ExpressionList ELLIPSIS COMMA RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS Type RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS Type COMMA RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS Type ELLIPSIS RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS Type ELLIPSIS COMMA RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS Type COMMA ExpressionList RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS Type COMMA ExpressionList COMMA RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS Type COMMA ExpressionList ELLIPSIS RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS Type COMMA ExpressionList ELLIPSIS COMMA RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS IDENT RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS IDENT COMMA RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS IDENT ELLIPSIS RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS IDENT ELLIPSIS COMMA RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS IDENT COMMA ExpressionList RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS IDENT COMMA ExpressionList COMMA RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS IDENT COMMA ExpressionList ELLIPSIS RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS IDENT COMMA ExpressionList ELLIPSIS COMMA RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS IDENT PERIOD IDENT RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS IDENT PERIOD IDENT COMMA RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS IDENT PERIOD IDENT ELLIPSIS RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS IDENT PERIOD IDENT ELLIPSIS COMMA RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS IDENT PERIOD IDENT COMMA ExpressionList RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS IDENT PERIOD IDENT COMMA ExpressionList COMMA RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS IDENT PERIOD IDENT COMMA ExpressionList ELLIPSIS RIGHT_PARENTHESIS
              | LEFT_PARENTHESIS IDENT PERIOD IDENT COMMA ExpressionList ELLIPSIS COMMA RIGHT_PARENTHESIS'''
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

def p_conversion(p):
    '''Conversion : Type LEFT_PARENTHESIS Expression COMMA RIGHT_PARENTHESIS
    | Type LEFT_PARENTHESIS Expression LEFT_PARENTHESIS
    | IDENT LEFT_PARENTHESIS Expression RIGHT_PARENTHESIS
    | IDENT LEFT_PARENTHESIS Expression COMMA RIGHT_PARENTHESIS
    | IDENT PERIOD IDENT LEFT_PARENTHESIS Expression RIGHT_PARENTHESIS
    | IDENT PERIOD IDENT LEFT_PARENTHESIS Expression COMMA RIGHT_PARENTHESIS'''
    p[0] = ['Conversion']
    for idx in range(1,len(p)):
        if p[idx] == '(' or p[idx] == ')' or p[idx] == ',':
            continue
        if isinstance(p[idx],str):
            p[0].append([p[idx]])
        else:
            p[0].append(p[idx])

def p_composite_lit(p):
    '''CompositeLit : StructType LiteralValue
                | ArrayType LiteralValue
                | SliceType LiteralValue
                | MapType LiteralValue
                | Type LiteralValue
                | IDENT LiteralValue
                | IDENT PERIOD IDENT LiteralValue
                | LEFT_BRACKET ELLIPSIS RIGHT_BRACKET Type LiteralValue
                | LEFT_BRACKET ELLIPSIS RIGHT_BRACKET IDENT LiteralValue
                | LEFT_BRACKET ELLIPSIS RIGHT_BRACKET IDENT PERIOD IDENT LiteralValue'''
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
    '''ElementList : KeyedElement KeyedElementStar'''
    p[0] = ['ElementList', p[1], p[2]]
def p_keyed_element_star(p):
    '''KeyedElementStar : KeyedElementStar COMMA KeyedElement 
                        |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['KeyedElementStar', p[1], p[3]]
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
    | GoStmt 
    | ReturnStmt 
    | BreakStmt 
    | ContinueStmt 
    | GotoStmt 
    | FallthroughStmt 
    | Block 
    | IfStmt 
    | SwitchStmt 
    | SelectStmt 
    | ForStmt 
    | DeferStmt '''
    p[0] = p[1]
def p_simple_stmt(p):
    '''SimpleStmt : ExpressionStmt 
    | SendStmt 
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
def p_send_stmt(p):
    '''SendStmt : Expression ARROW Expression'''
    p[0] = ['SendStmt', p[1], [p[2]], p[3]]
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
    | IF Expression Block Expression Block ELSE IfStmt
    | IF Expression Block Expression Block ELSE Block
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
def p_go_stmt(p):
    '''GoStmt : GO Expression '''
    p[0] = ['GoStmt', [p[1]], p[2]]

def p_selectstmt(p):
    '''SelectStmt : SELECT LEFT_BRACE CommClauseStar RIGHT_BRACE '''
    p[0] = ['SelectStmt', p[3]]

def p_comm_clause_plus(p):
    '''CommClauseStar : CommClauseStar CommClause 
    |'''
    if len(p) == 1:
        p[0] = p[1]
    else:
        p[0] = ['CommClauseStar', p[1], p[2]]
def p_comm_clause(p):
    '''CommClause : CommCase COLON StatementList'''
    p[0] = ['CommClause', p[1], [p[2]], p[3]]
def p_comm_case(p):
    '''CommCase : CASE SendStmt
    | CASE RecvStmt 
    | DEFAULT'''
    if len(p)==2:
        p[0] = [p[1]]
    else:
        p[0]=['CommCase', [p[1]], p[2]]
def p_recv_stmt(p):
    """RecvStmt : IdentifierList DEFINE Expression
             | ExpressionList ASSIGNMENT Expression
             | Expression"""
    if len(p)==2:
        p[0]=p[1]
    else:
        p[0]=['RecvStmt', p[1], [p[2]], p[3] ]
 
def p_returnstmt(p):
    '''ReturnStmt : RETURN ExpressionList
                    | RETURN'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = ['ReturnStmt', [p[1]], p[2]]
#---------------------------------
def p_break_stmt(p):
    '''BreakStmt : BREAK IDENT
                | BREAK'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = ['ReturnStmt', [p[1]], [p[2]]]
#-------------------------------------
def p_continue_stmt(p):
    '''ContinueStmt : CONTINUE IDENT
                | CONTINUE'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = ['ContinueStmt', [p[1]], [p[2]]]
def p_goto_stmt(p):
    '''GotoStmt : GOTO IDENT'''
    p[0] = ['GotoStmt', [p[1]], [p[2]]]
def p_fallthrough_stmt(p):
    '''FallthroughStmt : FALLTHROUGH'''
    p[0] = [p[1]]
def p_defer_stmt(p):
    '''DeferStmt : DEFER Expression'''
    p[0] = ['DeferStmt', [p[1]], p[2]]



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