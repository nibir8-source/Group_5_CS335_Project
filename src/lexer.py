import sys
import ply.lex as lex
from ply.lex import TOKEN


keywords = {
    #Keywords
    'break'        :    'BREAK',
    'default'      :    'DEFAULT',
    'func'         :    'FUNCTION',
    'case'         :    'CASE',
    'struct'       :    'STRUCT',
    # 'goto'         :    'GOTO',
    'else'         :    'ELSE',
    'package'      :    'PACKAGE',
    'switch'       :    'SWITCH',
    'const'        :    'CONSTANT',
    # 'range'        :    'RANGE',
    'type'         :    'TYPE',
    'if'           :    'IF',
    'continue'     :    'CONTINUE',
    'return'       :    'RETURN',
    'for'          :    'FOR',
    'import'       :    'IMPORT',
    'var'          :    'VARIABLE',
    'const'        :    'CONST',
    'true'         :    'TRUE',
    'false'        :    'FALSE',
}

tokens = list(keywords.values()) + [

    # Identifiers and Basic Type Literals
    'IDENT',            # main
    'INT',              # 123
    'FLOAT',            # 123.4
    'IMAGINARY',             # 123.4i
    # 'CHAR',             # 'a'
    'RUNE',
    'STRING',           # "abc"

    # Operators and Delimiters
    'ADD',              # +
    'SUBTRACT',              # -
    'MULTIPLY',              # *
    'QUOTIENT',              # /
    'REMAINDER',              # %

    'ADD_ASSIGNMENT',       # +=
    'SUB_ASSIGNMENT',       # -=
    'MUL_ASSIGNMENT',       # *=
    'QUO_ASSIGNMENT',       # %=
    'REM_ASSIGNMENT',       # %=

    'AND',              # &
    'OR',               # |
    'XOR',              # ^
    'SHIFT_LEFT',              # <<
    'SHIFT_RIGHT',              # >>
    'AND_NOT',          # &^

    'AND_ASSIGNMENT',       # &=
    'OR_ASSIGNMENT',        # |=
    'XOR_ASSIGNMENT',       # ^=
    'SHIFT_LEFT_ASSIGNMENT',       # <<=
    'SHIFT_RIGHT_ASSIGNMENT',       # >>=
    'AND_NOT_ASSIGNMENT',   # &^=

    'LOGICAL_AND',             # &&
    'LOGICAL_OR',              # ||
    'ARROW',            # <-
    'INCREMENT',              # ++
    'DECREMENT',              # --

    'EQUAL',              # ==
    'LESS_THAN',              # <
    'GREATER_THAN',              # >
    'ASSIGNMENT',           # =
    'NOT',              # !

    'NOT_EQUAL',              # !=
    'LESS_THAN_EQUAL',              # <=
    'GREATER_THAN_EQUAL',              # >=
    'DEFINE',           # :=

    'LEFT_PARENTHESIS',           # (
    'LEFT_BRACKET',           # [
    'LEFT_BRACE',           # {
    'COMMA',            # ,
    'PERIOD',           # .

    'RIGHT_PARENTHESIS',           # )
    'RIGHT_BRACKET',           # ]
    'RIGHT_BRACE',           # }
    'SEMICOLON',        # ;
    'COLON',            # :
]

prev_tok = ""

# Regular expression rules for different tokens
t_ADD   = r"\+"
t_SUBTRACT   = r"-"
t_MULTIPLY   = r"\*"
t_QUOTIENT   = r"/"
t_REMAINDER   = r"%"

t_ADD_ASSIGNMENT    = r"\+="
t_SUB_ASSIGNMENT    = r"-="
t_MUL_ASSIGNMENT    = r"\*="
t_QUO_ASSIGNMENT    = r"/="
t_REM_ASSIGNMENT    = r"%="

t_AND   = r"&"
t_OR    = r"\|"
t_XOR   = r"\^"
t_SHIFT_LEFT   = r"<<"
t_SHIFT_RIGHT   = r">>"
t_AND_NOT   = r"&\^"

t_AND_ASSIGNMENT  = r"&="
t_OR_ASSIGNMENT  = r"\|="
t_XOR_ASSIGNMENT  = r"\^="
t_SHIFT_LEFT_ASSIGNMENT  = r"<<="
t_SHIFT_RIGHT_ASSIGNMENT  = r">>="
t_AND_NOT_ASSIGNMENT  = r"&\^="

t_LOGICAL_AND  = r"&&"
t_LOGICAL_OR   = r"\|\|"
t_ARROW = r"<-"
t_INCREMENT   = r"\+\+"
t_DECREMENT   = r"--"

t_EQUAL   = r"=="
t_LESS_THAN   = r"<"
t_GREATER_THAN   = r">"
t_ASSIGNMENT    = r"="
t_NOT   = "!"

t_NOT_EQUAL   = r"!="
t_LESS_THAN_EQUAL   = r"<="
t_GREATER_THAN_EQUAL   = r">="
t_DEFINE    = r":="

t_LEFT_PARENTHESIS    = r"\("
t_LEFT_BRACKET    = r"\["
t_LEFT_BRACE    = r"\{"
t_COMMA     = r","
t_PERIOD    = r"\."

t_RIGHT_PARENTHESIS    = r"\)"
t_RIGHT_BRACKET    = r"\]"
t_RIGHT_BRACE    = r"\}"
t_SEMICOLON = r";"
t_COLON     = r":"

letter          = r"([_A-Za-z])"
decimal_digit   = r"([0-9])"
binary_digit    = r"([0-1])" 
octal_digit     = r"([0-7])" 
hex_digit       = r"([0-9A-Fa-f])"

identifier = r"(" + letter + r"(" + letter + r"|" + decimal_digit + r")*)"

decimal_digits  = r"(" + decimal_digit + r"(\_?" + decimal_digit + r")*)"
binary_digits   = r"(" + binary_digit + r"(\_?" + binary_digit + r")*)"
octal_digits    = r"(" + octal_digit + r"(\_?" + octal_digit + r")*)"
hex_digits      = r"(" + hex_digit + r"(\_?" + hex_digit + r")*)"

decimal_literal = r"(0|([1-9](\_?" + decimal_digits + r")?))"
binary_literal  = r"(0[bB]\_?" + binary_digits + r")" 
octal_literal   = r"(0[oO]?\_?" + octal_digits + r")" 
hex_literal     = r"(0[xX]\_?" + hex_digits + r")"

t_INT = r"(" + binary_literal + r"|" + octal_literal + r"|" + hex_literal + r"|" + decimal_literal + r")"

decimal_exponent  =  r"([eE][\+-]?" + decimal_digits + r")"
decimal_float_literal = r"(((" + decimal_digits + r")\.(" + decimal_digits + r")?(" + decimal_exponent + r")?)|(" + decimal_digits + decimal_exponent + r")|(\." + decimal_digits + r"(" + decimal_exponent + r")?))"

hex_exponent    = r"([pP][\+-]?" + decimal_digits + r")"
hex_mantissa    = r"(((\_?" + hex_digits + r"\." + hex_digits + r"?)|(\_?" + hex_digits + r")|(\." + hex_digits + r")))"
hex_float_literal   = r"(0[xX]" + hex_mantissa + hex_exponent + r")"

t_FLOAT = r"((" + hex_float_literal + ")|(" + decimal_float_literal + r"))"

t_IMAGINARY = r"(" + decimal_digits + "|" + t_INT + "|" + t_FLOAT + r")i" 

escp_char = r"(\\(a|b|f|n|r|t|v|\\|\'|\"))"
big_u_val = r"(\\U" + hex_digit + hex_digit + hex_digit + hex_digit + hex_digit + hex_digit + hex_digit + hex_digit + r")"
little_u_val = r"(\\u" + hex_digit + hex_digit + hex_digit + hex_digit + r")"
hex_byte_val = r"(\\x" + hex_digit + hex_digit + r")"
octal_byte_val = r"(\\" + octal_digit + octal_digit + octal_digit + r")"
byte_val = r"(" + octal_byte_val + "|" + hex_byte_val + r")"
unicode_char = r"([^\n\'\\])"
unicode_val = r"(" + unicode_char + r"|" + little_u_val + r"|" + big_u_val + r"|" + escp_char + r")"

t_RUNE = r"(\'(" + unicode_val + r"|" + byte_val + r")\')"

t_STRING    = r"(\"[^\"\\\n]*(\\.[^\"\\\n]*)*\")|(\`[^\`]*\`)" 
t_ignore = " \t\n"

def t_error(t):
    print(f"[ERROR] Invalid token: {t.value[0]} in #Line: {t.lineno}")
    t.lexer.skip(1)

# def t_NEWLINE(t):
#     r'\n+'
#     t.lexer.lineno += len(t.value)
#     pass

@TOKEN(identifier)
def t_IDENT(t):
    t.type = keywords.get(t.value,"IDENT")
    return t

def t_COMMENT(t):
    r"(//.*)|(/\*(.|\n)*?\*/)"
    pass

#Function to find #Column
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

#Token Processing
def Process(data):
    lexer = lex.lex()
    lexer.input(data)

    tokens = []

    while True:
        tok = lexer.token()
        if not tok:
            break
        elif tok.type == 'COMMENT':
            continue
        tokens.append(tok)
    return tokens