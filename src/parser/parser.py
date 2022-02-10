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
    '''QualifiedIdent : PackageName DOT IDENT'''
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
    '''Selector : DOT IDENT'''
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
    '''TypeAssertion : DOT LEFT_PARENTHESIS Type RIGHT_PARENTHESIS'''
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
    '''MethodExpr : ReceiverType DOT MethodName'''
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


