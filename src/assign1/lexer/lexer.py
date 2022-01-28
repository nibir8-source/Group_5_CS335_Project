from ply import lex
import ply.lex as lex
from ply.lex import TOKEN

keywords = {
    'break'        :    'BREAK',
    'default'      :    'DEFAULT',
    'select'       :    'SELECT',
    'func'         :    'FUNCTION',
    'case'         :    'CASE',
    'interface'    :    'INTERFACE',
    'defer'        :    'DEFER',
    'go'           :    'GO',
    'struct'       :    'STRUCT',
    'goto'         :    'GOTO',
    'chan'         :    'CHAN',
    'else'         :    'ELSE',
    'map'          :    'MAP',
    'fallthrough'  :    'FALLTHROUGH',
    'package'      :    'PACKAGE',
    'switch'       :    'SWITCH',
    'const'        :    'CONSTANT',
    'range'        :    'RANGE',
    'type'         :    'TYPE',
    'if'           :    'IF',
    'continue'     :    'CONTINUE',
    'return'       :    'RETURN',
    'for'          :    'FOR',
    'import'       :    'IMPORT',
    'var'          :    'VARIABLE',
}

tokens = list(keywords.values()) + [
    'IDENT',            # main
    'INT',              # 123
    'FLOAT',            # 123.4
    'IMAGINARY',             # 123.4i
    'CHAR',             # 'a'
    'STRING',           # "abc"
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
    'ELLIPSIS',         # ...
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
AND_ASSIGNMENT  = r"&="
OR_ASSIGNMENT   = r"!="
XOR_ASSIGNMENT  = r"\^="
SHL_ASSIGNMENT  = r"<<="
SHR_ASSIGNMENT  = r">>="
AND_NOT_ASSIGNMENT  = r"&\^="
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
t_ELLIPSIS  = r"\.\.\."
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

letter          = r"[_A-Za-z]"
decimal_digit   = r"[0-9]"

identifier = letter + r"(" + letter + r"|" + decimal_digit + r")*"

decimal_literal = r"[1-9][0-9]*"
t_INT           = decimal_literal
t_FLOAT         = r"[0-9]+\.[0-9]+"

t_ignore = " \t"

@TOKEN(identifier)
def t_IDENT(t):
    t.type = keywords.get(t.value,"IDENT")
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_STRING(t):
    r"(\"(.|\n)*?)\""
    return t


def t_error(t):
    print("[ERROR] Invalid token:",t.value[0])
    t.lexer.skip(1) #skip ahead 1 character


lexer = lex.lex()

# Test it out
data = '''
package main
import "fmt"
func main() {
    int a = 23
    fmt.Println("hello world")
}
'''

 # Give the lexer some input
lexer.input(data)
def find_column(input, token):
     line_start = input.rfind('\n', 0, token.lexpos) + 1
     return (token.lexpos - line_start) + 1
 # Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break
          # No more input
    print(tok.type,tok.value,tok.lineno,find_column(data,tok))
