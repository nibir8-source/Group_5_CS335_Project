from ply import lex
import ply.yacc as yacc
from ply.lex import TOKEN
import sys
sys.path.insert(0, '/home/nibir/nibir/cs335/project/Group_5_CS335_Project/src/lexer')
import lexer

precedence = (
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
def p_packageclause(p):
    '''PackageClause : PACKAGE IDENT'''
    p[0] = ['PackageClause', [p[2]]]
def p_importdecl(p):
    '''ImportDecl : IMPORT ImportSpecOr'''
    p[0] = ['ImportDecl', p[2]]
def p_import_spec_or(p):
    '''ImportSpecOr : ImportSpec 
    | LEFT_PARENTHESIS ImportSpecSemicolonStar RIGHT_PARENTHESIS'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]
def p_import_spec_semicolon_star(p):
    '''ImportSpecSemicolonStar : ImportSpecSemicolonStar ImportSpec SEMICOLON 
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['ImportSpecSemicolonStar', p[1], p[2]]
def p_import_spec(p):
    '''ImportSpec : PeriodPackageNamePlus ImportPath'''
    p[0] = ['ImportSpec', p[1], p[2]]
def p_period_package_name_plus(p):
    '''PeriodPackageNamePlus : PeriodPackageNameOr 
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['PeriodPackageNamePlus', p[1]]
def p_period_package_name_or(p):
    '''PeriodPackageNameOr : PERIOD 
    | IDENT'''
    p[0] = [p[1]]
def p_import_path(p):
    '''ImportPath : STRING'''
    p[0] = p[1]

# --------------------- TYPES -------------------------------------
def p_type(p):
    '''Type : TypeName 
    | TypeLit 
    | LEFT_PARENTHESIS Type RIGHT_PARENTHESIS'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]
def p_type_name(p):
    '''TypeName : IDENT 
    | QualifiedIdent'''
    if isinstance(p[1], str):
        p[0] = [p[1]]
    else:
        p[0] = p[1]
def p_type_lit(p):
    '''TypeLit : ArrayType 
    | StructType 
    | PointerType 
    | FunctionType 
    | InterfaceType 
    | SliceType 
    | MapType 
    | ChannelType'''
    p[0] = p[1]
def p_array_type(p):
    '''ArrayType : LEFT_BRACKET ArrayLength RIGHT_BRACKET Type'''
    p[0] = ['ArrayType', p[2], p[4]]
def p_array_length(p):
    '''ArrayLength : Expression'''
    p[0] = p[1]
def p_slice_type(p):
    '''SliceType : LEFT_BRACKET RIGHT_BRACKET Type'''
    p[0] = ['SliceType', p[3]]
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
    '''FieldDecl : IdentifierList Type TagPlus 
    | EmbeddedField TagPlus'''
    if len(p) == 3:
        p[0] = ['FieldDecl', p[1], p[2], p[3]]
    else:
        p[0] = ['FieldDecl', p[1], p[2]]
def p_tag_plus(p):
    '''TagPlus : Tag
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
def p_embedded_field(p):
    '''EmbeddedField : MULTIPLY TypeName 
    | TypeName'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ['EmbeddedField', [p[1]], p[2]]
def p_tag(p):
    '''Tag : STRING'''
    p[0] = [p[1]]
def p_pointer_type(p):
    '''PointerType : MULTIPLY BaseType'''
    p[0] = ['PointerType', [p[1]], p[2]]
def p_base_type(p):
    '''BaseType : Type'''
    p[0] = p[1]
def p_function_type(p):
    '''FunctionType : FUNCTION Signature'''
    p[0] = ['FunctionType', [p[0]], p[1]]
def p_signature(p):
    '''Signature : Parameters ResultPlus'''
    p[0] = ['Signature', p[1], p[2]]
def p_result_plus(p):
    '''ResultPlus : Result
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
def p_result(p):
    '''Result : Parameters 
    | Type'''
    p[0] = p[1]
def p_parameters(p):
    '''Parameters : LEFT_PARENTHESIS ParameterListPlus RIGHT_PARENTHESIS'''
    p[0] = ['Parameters', p[2]]
def p_parameters_list_plus(p):
    '''ParameterListPlus : ParameterList COMMA 
    | ParameterList 
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
def p_parameter_list(p):
    '''ParameterList : ParameterDecl
    | ParameterDecl COMMA ParameterList'''
    if len(p) == 1:
        p[0] = p[1]
    else:
        p[0] = ['ParamterList', p[1], p[3]]
def p_parameter_decl(p):
    '''ParameterDecl : IdentifierListPlus EllipsisPlus Type'''
    p[0] = ['ParameterDecl', p[1], p[2], p[3]]
def p_identifier_list_plus(p):
    '''IdentifierListPlus : IdentifierList
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
def p_ellipsis_plus(p):
    '''EllipsisPlus : ELLIPSIS
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[1]]
#--------------------------------------------------------------------
def p_interface_type(p):
    '''InterfaceType : INTERFACE LEFT_BRACE InterfaceTypePlus RIGHT_BRACE'''
    p[0] = ['InterfaceType', [p[1]], p[3]]
def p_interface_type_plus(p):
    '''InterfaceTypePlus : InterfaceTypePlus InterfaceTypeMethod SEMICOLON
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['InterfaceTypePlus', p[1], p[2]]
def p_interface_type_method(p):
    '''InterfaceTypeMethod : MethodSpec 
    | InterfaceTypeName'''
    p[0] = p[1]
def p_method_spec(p):
    '''MethodSpec : MethodName Signature'''
    p[0] = ['MetodSpec', p[1], p[2]]
def p_method_name(p):
    '''MethodName : IDENT'''
    p[0] = [p[1]]
def p_interface_type_name(p):
    '''InterfaceTypeName : TypeName'''
    p[0] = p[1]
def p_map_type(p):
    '''MapType : MAP LEFT_BRACKET KeyType RIGHT_BRACKET Type'''
    p[0] = ['MapType', p[1], p[3], p[5]]
def p_key_type(p):
    '''KeyType : Type'''
    p[0] = p[1]
def p_channel_type(p):
    '''ChannelType : ChannelTypeOr Type'''
    p[0] = ['ChannelType', p[1], p[2]]
def p_channel_type_or(p):
    '''ChannelTypeOr : CHAN 
    | CHAN ARROW 
    | ARROW CHAN'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = ['ChannelTypeOr', [p[1]], [p[2]]]
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
#-----------------------------------------------------------------------------
def p_declaration(p):
    '''Declaration : ConstDecl 
    | TypeDecl 
    | VarDecl'''
    p[0] = p[1]
def p_top_level_decl(p):
    '''TopLevelDecl : Declaration 
    | FunctionDecl 
    | MethodDecl'''
    p[0] = p[1]
def p_const_decl(p):
    '''ConstDecl : CONST ConstSpecOr'''
    p[0] = p[2]
def p_const_spec_or(p):
    '''ConstSpecOr : ConstSpec 
    | LEFT_PARENTHESIS ConstSpecStar RIGHT_PARENTHESIS'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]
def p_const_spec_star(p):
    '''ConstSpecStar : ConstSpecStar ConstSpec SEMICOLON
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['ConstSpecStar', p[1], p[2]]
def p_const_spec(p):
    '''ConstSpec : IdentifierList TypeAssignmentExpressionListPlus'''
    p[0] = ['ConstSpec', p[1], p[2]]
def p_type_assignment_expression_list_plus(p):
    '''TypeAssignmentExpressionListPlus : TypePlus ASSIGNMENT ExpressionList 
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['TypeAssignmentExpressionListPlus', p[1], [p[2]], p[3]]
def p_type_plus(p):
    '''TypePlus : Type 
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
def p_identifier_list(p):
    '''IdentifierList : IDENT IdentStar'''
    p[0] = ['IdentifierList', [p[1]], p[2]]
def p_ident_star(p):
    '''IdentStar : COMMA IDENT IdentStar
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['IdentStar', [p[2]], p[3]]
def p_expression_list(p):
    '''ExpressionList : Expression ExpressionStar'''
    p[0] = ['ExpressionList', p[1], p[2]]
def p_expression_star(p):
    '''ExpressionStar : COMMA Expression ExpressionStar
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['ExpressionStar', p[2], p[3]]
def p_type_decl(p):
    '''TypeDecl : TYPE TypeSpecOr'''
    p[0] = p[2]
def p_type_spec_or(p):
    '''TypeSpecOr : TypeSpec 
    | LEFT_PARENTHESIS TypeSpecStar RIGHT_PARENTHESIS'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]
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
    '''AliasDecl : IDENT ASSIGNMENT Type'''
    p[0] = ['AliasDecl', [p[1]], [p[2]], p[3]]
def p_type_def(p):
    '''TypeDef : IDENT Type'''
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
    '''VarSpec : IdentifierList TypeExpressionListOr'''
    p[0] = ['VarSpec', p[1], p[2]]
def p_type_expression_list_plus(p):
    '''TypeExpressionListOr : Type AssignmentExpressionListPlus 
    | ASSIGNMENT ExpressionList'''
    p[0] = ['TypeExpressionListOr']
    for idx in range(1,len(p)):
      if(isinstance(p[idx],str)):
        p[0].append([p[idx]])
      else:
        p[0].append(p[idx])
def p_assignment_expression_list_plus(p):
    '''AssignmentExpressionListPlus : ASSIGNMENT Expression 
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['AssignmentExpressionListPlus', [p[1]], p[2]]
def p_short_var_decl(p):
    '''ShortVarDecl : IdentifierList DEFINE ExpressionList'''
    p[0] = ['ShortVarDecl', [p[1]], p[3]]
def p_function_decl(p):
    '''FunctionDecl : FUNCTION FunctionName Signature FunctionBodyPlus'''
    p[0] = ['FunctionDecl', p[2], p[3], p[4]]
def p_function_body_plus(p):
    '''FunctionBodyPlus : FunctionBody 
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
def p_function_name(p):
    '''FunctionName : IDENT'''
    p[0] = [p[1]]
def p_function_body(p):
    '''FunctionBody : Block'''
    p[0] = p[1]
def p_method_decl(p):
    '''MethodDecl : FUNCTION Receiver MethodName Signature FunctionBodyPlus'''
    p[0] = ['MethodDecl', p[2], p[3], p[4], p[5]]
def p_receiver(p):
    '''Receiver : Parameters'''
    p[0] = p[1]
def p_operand(p):
    '''Operand : Literal 
    | OperandName 
    | LEFT_PARENTHESIS Expression RIGHT_PARENTHESIS'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]
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
def p_operand_name(p):
    '''OperandName : IDENT 
    | QualifiedIdent'''
    if(isinstance(p[1],str)):
        p[0] = [p[1]]
    else:
        p[0] = p[1]    

def p_qualified_ident(p):
    '''QualifiedIdent : IDENT PERIOD IDENT'''
    p[0] = ['QualifiedIdent', [p[1]], [p[2]], [p[3]]]
def p_composite_lit(p):
    '''CompositeLit : LiteralType LiteralValue'''
    p[0] = ['CompositeLit', p[1], p[2]]
def p_literal_type(p):
    '''LiteralType : StructType 
    | ArrayType 
    | LEFT_BRACKET ELLIPSIS RIGHT_BRACKET Type 
    | SliceType 
    | MapType 
    | TypeName'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ['LiteralType', p[2], p[4]]
def p_literal_value(p):
    '''LiteralValue : LEFT_BRACKET ElementListPlus RIGHT_BRACKET'''
    p[0] = p[2]
def p_element_list_plus(p):
    '''ElementListPlus : ElementList 
    | ElementList COMMA
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
def p_element_list(p):
    '''ElementList : KeyedElement KeyedElementStar'''
    p[0] = ['ElementList', p[1], p[2]]
def p_keyed_element_star(p):
    '''KeyedElementStar : COMMA KeyedElement KeyedElementStar 
                        |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['KeyedElementStar', [p[1]], p[2], p[3]]
def p_keyed_element(p):
    '''KeyedElement : KeyPlus Element'''
    p[0] = ['KeyedElement', p[1], p[2]]
def p_key_plus(p):
    '''KeyPlus : Key COLON
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
def p_key(p):
    '''Key : FieldName 
    | Expression 
    | LiteralValue'''
    p[0] = p[1]
def p_field_name(p):
    '''FieldName : IDENT'''
    p[0] = [p[1]]
def p_element(p):
    '''Element : Expression 
    | LiteralValue'''
    p[0] = p[1]
def p_function_lit(p):
    '''FunctionLit : FUNCTION Signature FunctionBody'''
    p[0] = ['FunctionLit', p[2], p[3]]
def p_primary_expr(p):
    '''PrimaryExpr : Operand 
    | Conversion
    | MethodExpr 
    | PrimaryExpr Selector 
    | PrimaryExpr Index 
    | PrimaryExpr Slice 
    | PrimaryExpr TypeAssertion 
    | PrimaryExpr Arguments'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ['PrimaryExpr', p[1], p[2]]
def p_selector(p):
    '''Selector : PERIOD IDENT'''
    p[0] = ['Selector', [p[1]], [p[2]]]
def p_index(p):
    '''Index : LEFT_BRACKET Expression RIGHT_BRACKET'''
    p[0] = p[2]
def p_slice(p):
    '''Slice : LEFT_BRACKET ExpressionPlus COLON ExpressionPlus RIGHT_BRACKET 
    | LEFT_BRACKET ExpressionPlus COLON Expression COLON Expression RIGHT_BRACKET'''
    if len(p) == 6:
        p[0] = ['Slice', p[2], [p[3]], p[4]]
    else:
        p[0] = ['Slice', p[2], [p[3]], p[4], [p[5]], p[6]]
def p_type_assertion(p):
    '''TypeAssertion : PERIOD LEFT_PARENTHESIS Type RIGHT_PARENTHESIS'''
    p[0] = ['TypeAssertion', [p[1]], p[3]]
def p_arguments(p):
    '''Arguments : LEFT_PARENTHESIS ArgumentsPlus RIGHT_PARENTHESIS'''
    p[0] = ['Arguments', p[2]]
def p_arguments_plus(p):
    '''ArgumentsPlus : ArgumentsInOr 
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
def p_arguments_in_or(p):
    '''ArgumentsInOr : ExpressionList 
    | Type CommaExpressionListPlus'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ['ArgumentsInOr', p[1], p[2]]
def p_comma_expression_list_plus(p):
    '''CommaExpressionListPlus : COMMA ExpressionList
    | ExpressionList 
    |'''
    if len(p) == 1:
        p[0] = []
    elif len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]
def p_method_expr(p):
    '''MethodExpr : ReceiverType PERIOD MethodName'''
    p[0] = ['MethodExpr', p[1], [p[2]], p[3]]
def p_receiver_type(p):
    '''ReceiverType : Type'''
    p[0] = p[1]
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
def p_conversion(p):
    '''Conversion : Type LEFT_PARENTHESIS Expression COMMA RIGHT_PARENTHESIS
    | Type LEFT_PARENTHESIS Expression RIGHT_PARENTHESIS'''
    p[0] = ['Conversion', p[1], p[3]]

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
    '''LabeledStmt : Label COLON Statement '''
    p[0] = ['LabeledStmt', p[1], [p[2]], p[3]]
def p_label(p):
    '''Label : IDENT'''
    p[0] = p[1]
def p_expression_stmt(p):
    '''ExpressionStmt : Expression'''
    p[0] = p[1]
def p_send_stmt(p):
    '''SendStmt : Channel ARROW Expression'''
    p[0] = ['SendStmt', p[1], [p[2]], p[3]]
def p_channel(p):
    '''Channel : Expression'''
    p[0] = p[1]
def p_inc_dec_stmt(p):
    '''IncDecStmt : Expression IncDecOr'''
    p[0] = ['InDecStmt', p[1], p[2]]
def p_inc_dec_or(p):
    '''IncDecOr : INCREMENT 
    | DECREMENT'''
    p[0] = [p[1]]
def p_assignment(p):
    '''Assignment : ExpressionList assign_op ExpressionList'''
    p[0] = ['Assignment', p[1], p[2], p[3]]
def p_assign_op(p):
    '''assign_op : add_op_mul_op_or_plus ASSIGNMENT'''
    p[0] = ['assign_op', p[1], [p[2]]]
def p_add_op_or_mul_op_plus(p):
    '''add_op_mul_op_or_plus : add_op_mul_op_or 
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
def p_add_op_mul_op_or(p):
    '''add_op_mul_op_or : add_op 
    | mul_op'''
    p[0] = p[1]
def p_if_stmt(p):
    '''IfStmt : IF SimpleStmtSemicolonPlus Expression Block ElsePlus'''
def p_simple_stmt_semicolon_plus(p):
    '''SimpleStmtSemicolonPlus : SimpleStmt SEMICOLON 
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
def p_else_plus(p):
    '''ElsePlus : ELSE Nested_if_block 
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['ElsePlus', [p[1]], p[2]]
def p_nested_if_block(p):
    '''Nested_if_block : IfStmt 
    | Block '''
    p[0] = p[1]
def p_switch_stmt(p):
    '''SwitchStmt : ExprSwitchStmt 
    | TypeSwitchStmt'''
    p[0] = p[1]
def p_expr_switch_stmt(p):
    '''ExprSwitchStmt : SWITCH SimpleStmtSemicolonPlus ExpressionPlus LEFT_BRACE ExprCaseClauseStar RIGHT_BRACE '''
    p[0]= ['ExprSwitchStmt', [p[1]], p[2], p[3], p[5]]
def p_expression_plus(p):
    '''ExpressionPlus : Expression 
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0]=p[1]
def p_expr_case_clause_plus(p):
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
    '''TypeSwitchStmt  : SWITCH SimpleStmtSemicolonPlus TypeSwitchGuard LEFT_BRACE TypeCaseClauseStar RIGHT_BRACE '''
    p[0] = ['TypeSwitchstmt', [p[1]], ]
def p_type_case_clause_star(p):
    '''TypeCaseClauseStar : TypeCaseClauseStar TypeCaseClause 
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['TypeCaseClauseStar', p[1], p[2]]
def p_typeswitchguard(p):
    '''TypeSwitchGuard : IdentDefinePlus PrimaryExpr PERIOD LEFT_PARENTHESIS TYPE RIGHT_PARENTHESIS '''
    p[0]=p[1]+" "+p[2]+" "+p[3]+" "+p[4]+" "+p[5]+" "+p[6]
def p_ident_define_plus(p):
    '''IdentDefinePlus : IDENT DEFINE 
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['IdentDefinePlus', [p[1]], [p[2]]]
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
    '''TypeList : Type CommaTypePlus '''
    p[0]=p[1]+" "+p[2]
   
def p_comma_type_plus(p):
    '''CommaTypePlus : CommaTypePlus COMMA TYPE 
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['CommaTypePlus', p[1], p[3]]
def p_for_stmt(p):
    '''ForStmt : FOR ForInternal Block'''
    p[0] = ['ForStmt', [p[1]], p[2], p[3]]
def p_for_internal(p):
    '''ForInternal : Condition 
    | ForClause 
    | RangeClause 
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
def p_condition(p):
    '''Condition : Expression'''
    p[0] = p[1]
#----------------------------------------------------------------
def p_for_clause(p):
    '''ForClause : InitStmtPlus SEMICOLON ConditionPlus SEMICOLON PostStmtPlus'''
    p[0] = ['ForClause', p[1], p[3], p[5]]
def p_init_stmt_plus(p):
    '''InitStmtPlus : InitStmt 
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
def p_condition_plus(p):
    '''ConditionPlus : Condition 
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
def p_post_stmt_plus(p):
    '''PostStmtPlus : PostStmt 
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
def p_init_stmt(p):
    '''InitStmt : SimpleStmt'''
    p[0] = p[1]
def p_post_stmt(p):
    '''PostStmt : SimpleStmt'''
    p[0] = p[1]
#---------------------------------------------------------------
def p_range_clause(p):
    '''RangeClause :  ExpListAssignIdListDefOrPlus RANGE Expression'''
    p[0] = ['RangeClause', p[1], [p[2]], p[3]]
    
def p_exp_list_assign_id_list_def_or_plus(p):
    '''ExpListAssignIdListDefOrPlus : ExpressionList ASSIGNMENT 
    | IdentifierList DEFINE 
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = ['ExpListAssignIdListDefOrPlus', p[1], [p[2]]]
def p_go_stmt(p):
    '''GoStmt : GO Expression '''
    p[0] = ['GoStmt', [p[1]], p[2]]
#------------------------------------------------------------------
def p_selectstmt(p):
    '''SelectStmt : SELECT LEFT_BRACE CommClausePlus RIGHT_BRACE '''
    p[0] = ['SelectStmt', p[3]]

def p_comm_clause_plus(p):
    '''CommClausePlus : CommClausePlus CommClause 
    |'''
    if len(p) == 1:
        p[0] = p[1]
    else:
        p[0] = ['CommClausePlus', p[1], p[2]]
def p_comm_clause(p):
    '''CommClause : CommCase COLON StatementList'''
    p[0] = ['CommClause', p[1], [p[2]], p[3]]
def p_comm_case(p):
    '''CommCase : CASE SentStmtRecvStmtOr 
    | DEFAULT'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ['CommCase', [p[1]], p[2]]
def p_sent_stmt_recv_stmt_or(p):
    '''SentStmtRecvStmtOr : SendStmt 
    | RecvStmt'''
    p[0] = p[1]
def p_recv_stmt(p):
    '''RecvStmt : ExpListAssignIdListDefOrPlus RecvExpr'''
    p[0] = ['RecvStmt', p[1], p[2]]
def p_recv_expr(p):
    '''RecvExpr : Expression'''
    p[0] = p[1]
 
def p_returnstmt(p):
    '''ReturnStmt : RETURN ExpressionListPlus'''
    p[0] = ['ReturnStmt', [p[1]], p[2]]
def p_expression_list_plus(p):
    '''ExpressionListPlus : ExpressionList 
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
#---------------------------------
def p_break_stmt(p):
    '''BreakStmt : BREAK LabelPlus'''
    p[0]=p[1]+" "+p[2]
    
#------------------------------------
def p_label_plus(p):
    '''LabelPlus : Label 
    |'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]
#-------------------------------------
def p_continue_stmt(p):
    '''ContinueStmt : CONTINUE LabelPlus'''
    p[0] = ['ContinueStmt', [p[1]], p[2]]
def p_goto_stmt(p):
    '''GotoStmt : GOTO Label'''
    p[0] = ['GotoStmt', [p[1]], p[2]]
def p_fallthrough_stmt(p):
    '''FallthroughStmt : FALLTHROUGH'''
    p[0] = [p[1]]
def p_defer_stmt(p):
    '''DeferStmt : DEFER Expression'''
    p[0] = ['DeferStmt', [p[1]], p[2]]



def p_error(p):
    print("Syntax error in input! ", p)


#-------------------------------------------------------------------------------------
file = open(sys.argv[1], 'r')
data = file.read()
tokens = lexer.tokens
parser = yacc.yacc(debug=True)
res = parser.parse(data)
import pprint
pprint.pprint(res)