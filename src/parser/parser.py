from ply import lex
import ply.yacc as yacc
from ply.lex import TOKEN
import sys
sys.path.insert(0, '/home/nibir/nibir/cs335/project/Group_5_CS335_Project/src/lexer')
import lexer

file = open(sys.argv[1], 'r')
data = file.read()

tokens = lexer.Process(data)

precedence = (
    ('right', 'ASSIGNMENT'),
    ('left', 'LOGICAL_OR'),
    ('left', 'LOGICAL_AND'),
    ('left', 'EQUAL', 'NOT_EQUAL', 'LESS_THAN', 'LESS_THAN_EQUAL', 'GREATER_THAN', 'GREATER_THAN_EQUAL'),
    ('left', 'ADD', 'SUBTRACT', 'OR', 'XOR'),
    ('left', 'MULTIPLY', 'QUOTIENT', 'REMAINDER', 'SHIFT_LEFT', 'SHIFT_RIGHT', 'AND', 'AND_NOT'),
    ('right', 'NOT'),
)


def p_type(p):
    '''Type : TypeName | TypeLit | LEFT_PARENTHESIS Type RIGHT_PARENTHESIS'''
    p[0] = p[1]

def p_type_name(p):
    ''''TypeName : IDENT | QualifiedIdent'''
    p[0] = p[1]

def p_package_name(p):
    '''PackageName : IDENT'''
    p[0] = p[1]

def p_type_lit(p):
    '''TypeLit : ArrayType | StructType | PointerType | FunctionType | InterfaceType | SliceType | MapType | ChannelType'''
    p[0] = p[1]

def p_array_type(p):
    '''ArrayType : LEFT_BRACKET ArrayLength RIGHT_BRACKET ElementType'''
    p[0] = p[3] + "[" + p[2] + "]"

def p_array_length(p):
    '''ArrayLength : Expression'''
    p[0] = p[1]

def p_element_type(p):
    '''ElementType : Type'''
    p[0] = p[1]

def p_slice_type(p):
    '''SliceType : LEFT_BRACKET RIGHT_BRACKET ElementType'''
    p[0] = p[3] + "[]"

def p_struct_type(p):
    '''StructType : STRUCT LEFT_BRACE ManyFieldDecl RIGHT_BRACE'''
    p[0] = "struct"

def p_many_field_decl(p):
    '''ManyFieldDecl : ManyFieldDecl FieldDecl SEMICOLON
                     | empty'''
    p[0] = p[1] + p[2]

def p_field_decl(p):
    '''FieldDecl : IdentifierList Type ZeroOneTag 
                 | EmbeddedField ZeroOneTag'''
    p[0] = p[1] + " " + p[2]

def p_zero_one_tag(p):
    '''ZeroOneTag : Tag
                  | EmptyStmt'''
    p[0] = p[1]

def p_embedded_field(p):
    '''EmbeddedField : ZeroOneStar TypeName'''
    p[0] = p[1] + p[2]

def p_zero_one_star(p):
    '''ZeroOneStar : STAR
                   | EmptyStmt'''
    p[0] = p[1]

def p_tag(p):
    '''Tag : STRING'''
    p[0] = p[1]

def p_pointer_type(p):
    '''PointerType : STAR BaseType'''
    p[0] = "*" + p[3] 

def p_base_type(p):
    '''BaseType : Type'''
    p[0] = p[1]

def p_function_type(p):
    '''FunctionType : FUNC Signature'''
    p[0] = "func"

def p_signature(p):
    '''Signature : Parameters ZeroOneResult'''
    p[0] = p[1] + " " + p[2]

def p_zero_one_result(p):
    '''ZeroOneResult : Result
                     | EmptyStmt'''
    p[0] = p[1]

def p_result(p):
    '''Result : Parameters | Type'''
    p[0] = p[1]

def p_parameters(p):
    '''Parameters : LEFT_PARENTHESIS ParameterListPlus RIGHT_PARENTHESIS'''
    p[0] = "(" + p[2] + ")"

def p_parameters_list_plus(p):
    '''ParameterListPlus : ParameterList CommaPlus
                         | empty'''
    p[0] = p[1]

def p_comma_plus(p):
    '''CommaPlus : COMMA
                 | EmptyStmt'''
    p[0] = p[1]

def p_parameter_list(p):
    '''ParameterList : ParameterDecl
                     | ParameterDecl COMMA ParameterList'''
    p[0] = p[1] + p[2]

def p_parameter_decl(p):
    '''IdentifierListPlus EllipsisPlus Type'''
    p[0] = p[1] + p[2] + p[3]

def p_ellipsis_plus(p):
    '''EllipsisPlus : ELLIPSIS
                    | EmptyStmt'''
    p[0] = p[1]

def p_interface_type(p):
    '''InterfaceType : INTERFACE LEFT_BRACE InterfaceTypePlus RIGHT_BRACE'''
    p[0] = "interface"

def p_interface_type_plus(p):
    '''InterfaceTypePlus : InterfaceTypePlus InterfaceTypeMethod SEMICOLON
                         | empty'''
    p[0] = p[1] + p[2]

def p_interface_type_method(p):
    '''InterfaceTypeMethod : MethodSpec | InterfaceTypeName'''
    p[0] = p[1]

def p_method_spec(p):
    '''MethodSpec : MethodName Signature'''
    p[0] = p[1] + " " + p[2]

def p_method_name(p):
    '''MethodName : IDENT'''
    p[0] = p[1]

def p_interface_type_name(p):
    '''InterfaceTypeName : TypeName'''
    p[0] = p[1]

def p_map_type(p):
    '''MapType : MAP LEFT_BRACKET KeyType RIGHT_BRACKET ElementType'''
    p[0] = "map"

def p_key_type(p):
    '''KeyType : Type'''
    p[0] = p[1]

def p_channel_type(p):
    '''ChannelType : ChannelTypeOr ElementType'''
    p[0] = "chan"

def p_channel_type_or(p):
    '''ChannelTypeOr : CHAN | CHAN ARROW | ARROW CHAN'''
    p[0] = p[1]

def p_block(p):
    '''Block : LEFT_BRACE StatementList RIGHT_BRACE'''
    p[0] = "{" + p[2] + "}"

def p_statement_list(p):
    '''StatementList : StatementList Statement SEMICOLON
                     | empty'''
    p[0] = p[1] + p[2]

def p_decalration(p):
    '''Decalration : ConstDecl | TypeDecl | VarDecl'''
    p[0] = p[1]

def p_top_level_decl(p):
    '''TopLevelDecl : Declaration | FunctionDecl | MethodDecl'''
    p[0] = p[1]

def p_const_decl(p):
    '''ConstDecl : CONST ConstSpecOr'''
    p[0] = "const"

def p_const_spec_or(p):
    '''ConstSpecOr : ConstSpec | LEFT_PARENTHESIS ConstSpecStar RIGHT_PARENTHESIS'''
    p[0] = p[1]

def p_const_spec_star(p):
    '''ConstSpecStar : ConstSpecStar ConstSpec SEMICOLON
                     | empty'''
    p[0] = p[1]

def p_const_spec(p):
    '''ConstSpec : IdentifierList ExpressionListPlus'''
    p[0] = p[1] + " " + p[2]

def p_expression_list_plus(p):
    '''ExpressionListPlus : TypePlus ASSIGNMENT ExpressionList 
                          | EmptyStmt'''
    p[0] = p[1]

def p_type_plus(p):
    '''TypePlus : Type | EmptyStmt'''
    p[0] = p[1]

def p_expression_list(p):
    '''ExpressionList : IDENT IdentStar'''
    p[0] = p[1] + p[2]

def p_indent_star(p):
    '''IdentStar : COMMA IDENT IdentStar
                 | empty'''
    p[0] = p[1]

def p_expression_list(p):
    '''ExpressionList : Expression ExpressionStar'''
    p[0] = p[1] + p[2]

def p_expression_star(p):
    '''ExpressionStar : COMMA Expression ExpressionStar
                      | empty'''
    p[0] = p[1]

def p_type_decl(p):
    '''TypeDecl : TYPE TypeSpecOr'''
    p[0] = "type"

def p_type_spec_or(p):
    '''TypeSpecOr : TypeSpec | LEFT_PARENTHESIS TypeSpecStar RIGHT_PARENTHESIS'''
    p[0] = p[1]

def p_type_spec_star(p):
    '''TypeSpecStar : TypeSpecStar TypeSpec SEMICOLON
                    | empty'''
    p[0] = p[1]

def p_type_spec(p):
    '''TypeSpec : AliasDecl | TypeDef'''
    p[0] = p[1] 

def p_alias_decl(p):
    '''AliasDecl : IDENT ASSIGNMENT Type'''
    p[0] = p[1] + " " + p[2] + " " + p[3]

def p_type_def(p):
    '''TypeDef : IDENT Type'''
    p[0] = p[1] + " " + p[2]
    
def p_var_decl(p):
    '''VarDecl : VAR VarSpecOr'''
    p[0] = p[1] + " " + p[2]

def p_var_spec_or(p):
    '''VarSpecOr : VarSpec | LEFT_PARENTHESIS VarSpecStar RIGHT_PARENTHESIS'''
    p[0] = p[1]

def p_var_spec_star(p):
    '''VarSpecStar : VarSpecStar VarSpec SEMICOLON | Empty'''
    p[0] = p[1]

def p_var_spec(p):
    '''VarSpec : IdentifierList TypeExpressionListOr'''
    p[0] = p[1] + " " + p[2]

def p_type_expression_list_plus(p):
    '''TypeExpressionListOr : Type AssignmentExpressionListPlus | ASSIGNMENT ExpressionList'''
    p[0] = p[1]

def p_assignment_expression_list_plus(p):
    '''AssignementExpressionListPlus : ASSIGNMENT Expression | EmptyStmt'''
    p[0] = p[1]

def p_short_var_decl(p):
    '''ShortValDecl : IdentifierList DEFINE ExpressionList'''
    p[0] = p[1] + " " + p[2] + " " + p[3]

def p_function_decl(p):
    '''FunctionDecl : FUNC FunctionName Signature FunctionBodyPlus'''
    p[0] = p[1] + " " + p[2] + " " + p[3] + " " + p[4]

def p_function_body_plus(p):
    '''FunctionBodyPlus : FunctionBody | EmptyStmt'''
    p[0] = p[1]

def p_function_name(p):
    '''FunctionName : IDENT'''
    p[0] = p[1]

def p_function_body(p):
    '''FunctionBody : Block'''
    p[0] = p[1]

def p_method_decl(p):
    '''MethodDecl : FUNC Receiver MethodName Signature FunctionBodyPlus'''
    p[0] = p[1] + " " + p[2] + " " + p[3] + " " + p[4]

def p_receiver(p):
    '''Receiver : Parameters'''
    p[0] = p[1]

def p_operand(p):
    '''Operand : Literal | OperandName | LEFT_PARENTHESIS Expression RIGHT_PARENTHESIS'''
    p[0] = p[1]

def p_literal(p):
    '''Literal : BasicLit | CompositeLit | FunctionLit'''
    p[0] = p[1]

def p_basic_lit(p):
    '''BasicLit : INT | FLOAT | IMAGINARY | FLOAT | RUNE | STRING'''
    p[0] = p[1]

def p_operand_name(p):
    '''OperandName : IDENT | QualifiedIdent'''
    p[0] = p[1]


def p_qualified_ident(p):
    '''QualifiedIdent : PackageName PERIOD IDENT'''
    p[0] = p[1] + "." + p[3]

def p_composite_lit(p):
    '''CompositeLit : LiteralType LiteralValue'''
    p[0] = p[1] + " " + p[2]

def p_literal_type(p):
    '''LiteralType : StructType | ArrayType | LEFT_BRACKET ELLIPSIS RIGHT_BRACKET ElementType |
                    SliceType | MapType | TypeName'''
    p[0] = p[1]

def p_literal_value(p):
    '''LiteralValue : LEFT_BRACKET ElementListPlus RIGHT BRACKET'''
    p[0] = p[1] + " " + p[2] + " " + p[3]

def p_element_list_plus(p):
    '''ElementListPlus : ElementList CommaPlus | EmptyStmt'''
    p[0] = p[1]

def p_element_list(p):
    '''ElementList : KeyedElement KeyedelementStar'''
    p[0] = p[1] + " " + p[2]

def KeyedElementStar(p):
    '''KeyedElementPlus : KeyedElementStar KeyedElement | EmptyStmt'''
    p[0] = p[1]

def KeyedElement(p):
    '''KeyedElement : KeyPlus Element'''
    p[0] = p[1] + " " + p[1]

def p_key_plus(p):
    '''KeyPlus : Key | EmptyStmt'''
    p[0] = p[1]

def p_key(p):
    '''Key : FieldName | Expression | LiteralValue'''
    p[0] = p[1]

def p_field_name(p):
    '''FieldName : IDENT'''
    p[0] = p[1]

def p_element(p):
    '''Element : Expression | LiteralVal'''
    p[0] = p[1]

def p_function_lit(p):
    '''FunctionLit : FUNC Signature FunctionBody'''
    p[0] = p[1]

def p_primary_expr(p):
    '''PrimaryExpr : Operand |
	Conversion |
	MethodExpr |
	PrimaryExpr Selector |
	PrimaryExpr Index |
	PrimaryExpr Slice |
	PrimaryExpr TypeAssertion |
	PrimaryExpr Arguments'''
    p[0] = p[1]

def p_selector(p):
    '''Selector : PERIOD IDENT'''
    p[0] = p[1] + " " + p[2]

def p_index(p):
    '''Index : LEFT_BRACKET Expression RIGHT_BRACKET'''
    p[0] = p[1] + " " + p[2] + " " + p[3]

def p_slice(p):
    '''Slice : LEFT_BRACKET ExpressionPlus COLON ExpressionPlus RIGHT_BRACKET | LEFT_BRACKET ExpressionPlus COLON Expression COLON Expression RIGHT_BRACKET'''
    p[0] = p[1]

def p_expression_plus(p):
    '''ExpressionPlus : Expression | EmptyStmt'''
    p[0] = p[1]

def p_type_assertion(p):
    '''TypeAssertion : PERIOD LEFT_PARENTHESIS Type RIGHT_PARENTHESIS'''
    p[0] = p[1] + " " + p[2] + " " + p[3] + " " + p[4]

def p_arguments(p):
    '''Arguments: LEFT_PARENTHESIS ArgumentsPlus RIGHT_PARENTHESIS'''
    p[0] = p[1] + " " + p[2] + " " + p[3]

def p_arguments_plus(p):
    '''ArgumentsPlus : ArgumentsInOr | EmptyStmt'''
    p[0] = p[1]

def p_arguments_in_or(p):
    '''ArgumentsInOr : ExpressionList | Type CommaExpressionListPlus'''
    p[0] = p[1]

def p_comma_expression_list_plus(p):
    '''CommaExpressionListPlus : CommaPlus ExpressionList | EmptyStmt'''
    p[0] = p[1]

def p_method_expr(p):
    '''MethodExpr : ReceiverType PERIOD MethodName'''
    p[0] = p[1] + " " + p[2] + " " + p[3]

def p_receiver_type(p):
    '''ReceiverType : Type'''
    p[0] = p[1]

def p_expression(p):
    '''Expression : UnaryExpr | Expression binary_op Expression'''
    p[0] = p[1]

def p_unary_expr(p):
    '''UnaryEpr : PrimaryExpr | unary_op UnaryExpr'''
    p[0] = p[1]

def p_binary_op(p):
    '''binary_op : LOGICAL_OR | LOGICAL_AND | rel_op | add_op | mul_op'''
    p[0] = p[1]

def p_rel_op(p):
    '''rel_op : EQUAL | NOT_EQUAL | LESS_THAN | LESS_THAN_EQUAL | GREATER_THAN | GREATER_THAN_EQUAL'''
    p[0] = p[1]

def p_add_op(p):
    '''add_op : ADD | SUBTRACT | OR | XOR'''
    p[0] = p[1]

def p_mul_op(p):
    '''mul_op : MULTIPLY | QUOTIENT | REMAINDER | SHIFT_LEFT | SHIFT_RIGHT | AND | AND_NOT'''
    p[0] = p[1]

def p_unary_op(p):
    '''unary_op : ADD | SUBTRACT | NOT | XOR | MULTIPLY | AND | ARROW'''
    p[0] = p[1]

def p_conversion(p):
    '''Conversion : Type LEFT_PARENTHESIS Expression CommaPlus RIGHT_PARENTHESIS'''
    p[0] = p[1] + " " + p[1] + " " + p[2] + " " + p[3] + " " + p[4] + " " + p[5]


#STATEMENT
def p_statement(p):
    '''Statement : Declaration | LabeledStmt | SimpleStmt | GoStmt | ReturnStmt | BreakStmt | ContinueStmt | GotoStmt | FallthroughStmt | Block | IfStmt | SwitchStmt | SelectStmt | ForStmt | DeferStmt '''
    p[0]=p[1]

def p_simplestmt(p):
    '''SimpleStmt : EmptyStmt | ExpressionStmt | SendStmt | IncDecStmt | Assignment | ShortVarDecl '''
    p[0]=p[1]

def p_emptystmt(p):
    '''EmptyStmt :'''
    # p[0] = ""
    pass


def p_labeledstmt(p):
    '''LabeledStmt : Label COLON Statement '''
    p[0]=p[1] + " " + p[2] + " " +p[3]

def p_label(p):
    '''Label : IDENT'''
    p[0]=p[1]

def p_expressionstmt(p):
    '''ExpressionStmt : Expression'''
    p[0]=p[1]

def p_sendstmt(p):
    '''SendStmt : Channel ARROW Expression'''
    p[0]=p[1]+" "+p[2] + " " + p[3]

def p_channel(p):
    '''Channel : Expression'''
    p[0]=p[1]

def p_incdecstmt(p):
    '''IncDecStmt : Expression Incordec'''
    p[0]=p[1]+" " + p[2]

def p_incordec(p):
    '''Incordec : INCREMENT | DECREMENT '''
    p[0]=p[1]

def p_assignment(p):
    '''Assignment : ExpressionList assign_op ExpressionList'''
    p[0]=p[1] + " " + p[2] + " " + p[3]

def p_assign_op(p):
    '''assign_op : add_op_or_mul_op_plus ASSIGNMENT'''
    p[0]=p[1]+" "+p[2]

def p_add_op_or_mul_op_plus(p):
    '''add_op_or_mul_op_plus : add_op_or_mul_op | EmptyStmt'''
    p[0]=p[1]

def p_add_op_or_mul_op(p):
    '''add_op_or_mul_op : add_op | mul_op'''
    p[0]=p[1]

def p_ifstmt(p):
    '''IfStmt : IF Simplestmt_semicolon_or_emptystmt  Expression Block Else_present_or_not'''

def p_simplestmt_semicolon_or_emptystmt(p):
    '''Simplestmt_semicolon_or_emptystmt : SimpleStmt SEMICOLON | EmptyStmt '''

    if(len(p)==2):
        p[0]=p[1]
    else:
        p[0]=p[1]+" "+p[2]
    #some error

def else_present_or_not(p):
    '''Else_present_or_not : ELSE Nested_if_block | EmptyStmt'''

    if(len(p)==2):
        p[0]=p[1]
    else:
        p[0]=p[1]+" "+p[2]
    #some error

def p_nested_if_block(p):
    '''Nested_if_block : IfStmt | Block '''
    p[0]=p[1]

def p_switchstmt(p):
    '''SwitchStmt : ExprSwitchStmt | TypeSwitchStmt'''
    p[0]=p[1]

def p_exprswitchstmt(p):
    '''ExprSwitchStmt : SWITCH Simplestmt_semicolon_or_emptystmt Expression_or_empty LEFT_BRACE Exprcaseclause_zero_or_more_time RIGHT_BRACE '''
    p[0]= p[1]+" "+p[2] + " " + p[3] + " " + p[4] + " "+ p[5] +" "+ p[6]

def p_expression_or_empty(p):
    '''Expression_or_empty : Expression | EmptyStmt'''
    p[0]=p[1]

def p_exprcaseclause_zero_or_more_time(p):
    '''Exprcaseclause_zero_or_more_time : Exprcaseclause_zero_or_more_time ExprCaseClause | EmptyStmt'''
    if(len(p)==2):
        p[0]=p[1]
    else:
        p[0]=p[1]+" "+p[2]
     #error

def p_exprcaseclause(p):
    '''ExprCaseClause : ExprSwitchCase COLON StatementList'''
    p[0]=p[1]+" "+p[2]+" "+p[3]

def p_exprswitchcase(p):
    '''ExprSwitchCase : CASE ExpressionList | DEFAULT '''
    if(len(p)==2):
        p[0]=p[1]
    else:
        p[0]=p[1]+" "+p[2]
    # p[0]=p[1]
    #some error


# TypeSwitchStmt  = "switch" [ SimpleStmt ";" ] TypeSwitchGuard "{" { TypeCaseClause } "}" .
# TypeSwitchGuard = [ identifier ":=" ] PrimaryExpr "." "(" "type" ")" .
# TypeCaseClause  = TypeSwitchCase ":" StatementList .
# TypeSwitchCase  = "case" TypeList | "default" .
# TypeList        = Type { "," Type } .

def p_typeswitchstmt(p):
    '''TypeSwitchStmt  : SWITCH Simplestmt_semicolon_or_emptystmt TypeSwitchGuard LEFT_BRACE Typecaseclause_zero_or_more RIGHT_BRACE '''
    p[0]=p[1]+ " " + p[2] + " " +p[3] + " " + p[4] +" " + p[5] +" "+p[6]

def p_typecaseclause_zero_or_more(p):
    '''Typecaseclause_zero_or_more : Typecaseclause_zero_or_more TypeCaseClause | EmptyStmt'''
    if(len(p)==2):
        p[0]=p[1]
    else:
        p[0]=p[1]+" "+p[2]
     #some error

def p_typeswitchguard(p):
    '''TypeSwitchGuard : Identifier_define_zero_or_one PrimaryExpr PERIOD LEFT_PARANTHESIS TYPE RIGHT_PARANTHESIS '''
    p[0]=p[1]+" "+p[2]+" "+p[3]+" "+p[4]+" "+p[5]+" "+p[6]

def p_identifier_define_zero_or_one(p):
    '''Identifier_define_zero_or_one : IDENT DEFINE | EmptyStmt'''
    if(len(p)==2):
        p[0]=p[1]
    else:
        p[0]=p[1]+" "+p[2]
    #some error

def p_typecaseclause(p):
    '''TypeCaseClause  : TypeSwitchCase COLON StatementList '''
    p[0]=p[1]+" "+p[2]+" "+p[3]

def p_typeswitchcase(p):
    '''TypeSwitchCase : CASE TypeList | DEFAULT'''
    if(len(p)==2):
        p[0]=p[1]
    else:
        p[0]=p[1]+" "+p[2]
    #some error

def p_typelist(p):
    '''TypeList : Type Comma_type_zero_or_more '''
    p[0]=p[1]+" "+p[2]
   
def p_comma_type_zero_or_more(p):
    '''Comma_type_zero_or_more : Comma_type_zero_or_more COMMA TYPE | EmptyStmt '''
    if(len(p)==2):
        p[0]=p[1]
    else:
        p[0]=p[1]+" "+p[2]
    #some error

# ForStmt = "for" [ Condition | ForClause | RangeClause ] Block .
# Condition = Expression 

def p_forstmt(p):
    '''ForStmt : FOR For_internal Block'''
    p[0]=p[1]+" "+p[2]+" "+p[3]

def p_for_internal(p):
    '''For_internal : Condition | ForClause | RangeClause | EmptyStmt'''
    p[0]=p[1]

def p_condition(p):
    '''Condition : Expression'''
    p[0]=p[1]

# ForClause = [ InitStmt ] ";" [ Condition ] ";" [ PostStmt ] .
# InitStmt = SimpleStmt .
# PostStmt = SimpleStmt .
def p_forclause(p):
    '''ForClause : Initstmt_zero_or_one SEMICOLON Condition_zero_or_one SEMICOLON Poststmt_zero_or_one'''
    p[0]=p[1]+" "+p[2]+" "+p[3]+" "+p[4]+" "+p[5]

def p_initstmt_zero_or_one(p):
    '''Initstmt_zero_or_one : InitStmt | EmptyStmt'''
    p[0]=p[1]

def p_condition_zero_or_one(p):
    '''Condition_zero_or_one : Condition | EmptyStmt'''
    p[0]=p[1]

def p_poststmt_zero_or_one(p):
    '''Poststmt_zero_or_one : PostStmt | EmptyStmt'''
    p[0]=p[1]

def p_initstmt(p):
    '''InitStmt : SimpleStmt'''
    p[0]=p[1]

def p_poststmt(p):
    '''PostStmt : SimpleStmt'''
    p[0]=p[1]

#RangeClause = [ ExpressionList "=" | IdentifierList ":=" ] "range" Expression 
def p_rangeclause(p):
    '''RangeClause :  Above_exp_zero_or_one RANGE Expression '''
    p[0]=p[1]+" "+p[2]+" "+p[3]
    
def p_above_exp_zero_or_one(p):
    '''Above_exp_zero_or_one : ExpressionList ASSIGNMENT | IdentifierList DEFINE | EmptyStmt'''
    if(len(p)==2):
        p[0]=p[1]
    else:
        p[0]=p[1]+" "+p[2]
    #some error

# GoStmt = "go" Expression 
def p_gostmt(p):
    '''GoStmt : GO Expression '''
    p[0]=p[1]+" "+p[2]

# SelectStmt = "select" "{" { CommClause } "}" .
# CommClause = CommCase ":" StatementList .
# CommCase   = "case" ( SendStmt | RecvStmt ) | "default" .
# RecvStmt   = [ ExpressionList "=" | IdentifierList ":=" ] RecvExpr .
# RecvExpr   = Expression .

def p_selectstmt(p):
    '''SelectStmt : SELECT LEFT_BRACE Commclause_zero_or_one RIGHT_BRACE '''
    p[0]=p[1]+" "+p[2]+" "+p[3]+" "+p[4]


def p_commclause_zero_or_one(p):
    '''Commclause_zero_or_one : commclause_zero_or_one CommClause | EmptyStmt'''
    if(len(p)==2):
        p[0]=p[1]
    else:
        p[0]=p[1]+" "+p[2]
    
    #some error

def p_commclause(p):
    '''CommClause : CommCase COLON StatementList'''
    p[0]=p[1]+" "+p[2]+" "+p[3]

def p_commcase(p):
    '''CommCase : CASE Sentstmt_recvstmt | DEFAULT'''
    if(len(p)==2):
        p[0]=p[1]
    else:
        p[0]=p[1]+" "+p[2]
    
     #some error

def p_sentstmt_recvstmt(p):
    '''Sentstmt_recvstmt : SendStmt | RecvStmt'''
    p[0]=p[1]

def p_recvstmt(p):
    '''RecvStmt : Above_exp_zero_or_one RecvExpr'''
    p[0]=p[1]+" "+p[2]

def p_recvexpr(p):
    '''RecvExpr : Expression'''
    p[0]=p[1]

# ReturnStmt = "return" [ ExpressionList ] 
def p_returnstmt(p):
    '''ReturnStmt : RETURN Expression_list_zero_or_one'''
    p[0]=p[1]+" "+p[2]

def p_expression_list_zero_or_one(p):
    '''Expression_list_zero_or_one : ExpressionList | EmptyStmt'''
    p[0]=p[1]

# BreakStmt = "break" [ Label ]
def p_breakstmt(p):
    '''BreakStmt : BREAK Label_zero_or_one'''
    p[0]=p[1]+" "+p[2]
    

def p_label_zero_or_one(p):
    '''Label_zero_or_one : Label | EmptyStmt'''
    p[0]=p[1]

# ContinueStmt = "continue" [ Label ] 
def p_continuestmt(p):
    '''ContinueStmt : CONTINUE Label_zero_or_one'''
    p[0]=p[1]+" "+p[2]

# GotoStmt = "goto" Label
def p_gotostmt(p):
    '''GotoStmt : GOTO Label'''
    p[0]=p[1]+" "+p[2]

# FallthroughStmt = "fallthrough"
def p_fallthroughstmt(p):
    '''FallthroughStmt : FALLTHROUGH'''
    p[0]=p[1]

# DeferStmt = "defer" Expression 
def p_deferstmt(p):
    '''DeferStmt : DEFER Expression'''
    p[0]=p[1]

# SourceFile       = PackageClause ";" { ImportDecl ";" } { TopLevelDecl ";" } 
def p_sourcefile(p):
    '''SourceFile  : PackageClause SEMICOLON Importdecl_zero_or_more Topleveldecl_zero_or_more'''
    p[0]=p[1]+" "+p[2]+" "+p[3]+" "+p[4]

def p_importdecl_zero_or_more(p):
    '''Importdecl_zero_or_more : Importdecl_zero_or_more ImportDecl SEMICOLON | EmptyStmt'''
    if(len(p)==2):
        p[0]=p[1]
    else:
        p[0]=p[1]+" "+p[2]+" "+p[3]
     #some error

def p_topleveldecl_zero_or_more(p):
    '''Topleveldecl_zero_or_more : topleveldecl_zero_or_more TopLevelDecl SEMICOLON | EmptyStmt'''
    if(len(p)==2):
        p[0]=p[1]
    else:
        p[0]=p[1]+" "+p[2]+" "+p[3]
    #some error

# PackageClause  = "package" PackageName .
# PackageName    = identifier .
def p_packageclause(p):
    '''PackageClause : "package" PackageName'''
    p[0]=p[1]+" "+p[2]

def p_packagename(p):
    '''PackageName : IDENT'''
    p[0]=p[1]

# ImportDecl       = "import" ( ImportSpec | "(" { ImportSpec ";" } ")" ) .
# ImportSpec       = [ "." | PackageName ] ImportPath .
# ImportPath       = string_lit .

def p_importdecl(p):
    '''ImportDecl = IMPORT ImportSpecOr'''
    p[0] = p[1] + " " + p[2]

def p_import_spec_or(p):
    '''ImportSpecOr : ImportSpec | LEFT_PARENTHESIS ImportSpecColonStar RIGHT_PARENTHESIS'''
    if(len(p)==2):
        p[0]=p[1]
    else:
        p[0]=p[1]+" "+p[2]+" "+p[3]
    #SOME ERROR

def p_import_spec_star(p):
    '''ImportSpecStar : ImportSpecStar ImportSpec COLON | EmptyStmt'''
    if(len(p)==2):
        p[0]=p[1]
    else:
        p[0]=p[1]+" "+p[2]+" "+p[3]
    #some error
def p_import_spec(p):
    '''ImportSpec : PeriodPackageNamePlus ImportPath'''
    p[0] = p[1] + " " + p[2]

def p_period_package_name_plus(p):
    '''PeriodPackageNamePlus : PeriodOrPackageName | EmptyStmt'''
    p[0] = p[1]

def p_period_or_package_name(p):
    '''PeriodPackageName : PERIOD PackageName'''
    p[0] = p[1] + " " + p[2]

def p_import_path(p):
    '''ImportPath : STRING'''
    p[0] = p[1]

