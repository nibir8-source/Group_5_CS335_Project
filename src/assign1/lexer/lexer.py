from ply import lex
import ply.lex as lex
from ply.lex import TOKEN

keywords = {
    'break'        :    'BREAK',
    'default'      :    'DEFAULT',
    'select'       :    'SELECT',
    'func'         :    'FUNC',
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
    'const'        :    'CONST',
    'range'        :    'RANGE',
    'type'         :    'TYPE',
    'if'           :    'IF',
    'continue'     :    'CONTINUE',
    'return'       :    'RETURN',
    'for'          :    'FOR',
    'import'       :    'IMPORT',
    'var'          :    'VAR',
}

tokens = list(keywords.values()) + [
    'IDENT',            # main
    'INT',              # 123
    'FLOAT',            # 123.4
    'IMAG',             # 123.4i
    'CHAR',             # 'a'
    'STRING',           # "abc"
    'ADD',              # +
    'SUB',              # -
    'MUL',              # *
    'QUO',              # /
    'REM',              # %
    'ADD_ASSIGN',       # +=
    'SUB_ASSIGN',       # -=
    'MUL_ASSIGN',       # *=
    'QUO_ASSIGN',       # %=
    'REM_ASSIGN',       # %=
    'AND',              # &
    'OR',               # |
    'XOR',              # ^
    'SHL',              # <<
    'SHR',              # >>
    'AND_NOT',          # &^
    'AND_ASSIGN',       # &=
    'OR_ASSIGN',        # |=
    'XOR_ASSIGN',       # ^=
    'SHL_ASSIGN',       # <<=
    'SHR_ASSIGN',       # >>=
    'AND_NOT_ASSIGN',   # &^=
    'LAND',             # &&
    'LOR',              # ||
    'ARROW',            # <-
    'INC',              # ++
    'DEC',              # --
    'EQL',              # ==
    'LSS',              # <
    'GTR',              # >
    'ASSIGN',           # =
    'NOT',              # !
    'NEQ',              # !=
    'LEQ',              # <=
    'GEQ',              # >=
    'DEFINE',           # :=
    'ELLIPSIS',         # ...
    'LPAREN',           # (
    'LBRACK',           # [
    'LBRACE',           # {
    'COMMA',            # ,
    'PERIOD',           # .
    'RPAREN',           # )
    'RBRACK',           # ]
    'RBRACE',           # }
    'SEMICOLON',        # ;
    'COLON',            # :
]

t_ADD   = r"\+"
t_SUB   = r"-"
t_MUL   = r"\*"
t_QUO   = r"/"
t_REM   = r"%"
t_ADD_ASSIGN    = r"\+="
t_SUB_ASSIGN    = r"-="
t_MUL_ASSIGN    = r"\*="
t_QUO_ASSIGN    = r"/="
t_REM_ASSIGN    = r"%="
t_AND   = r"&"
t_OR    = r"\|"
t_XOR   = r"\^"
t_SHL   = r"<<"
t_SHR   = r">>"
t_AND_NOT   = r"&\^"
AND_ASSIGN  = r"&="
OR_ASSIGN   = r"!="
XOR_ASSIGN  = r"\^="
SHL_ASSIGN  = r"<<="
SHR_ASSIGN  = r">>="
AND_NOT_ASSIGN  = r"&\^="
t_LAND  = r"&&"
t_LOR   = r"\|\|"
t_ARROW = r"<-"
t_INC   = r"\+\+"
t_DEC   = r"--"
t_EQL   = r"=="
t_LSS   = r"<"
t_GTR   = r">"
t_ASSIGN    = r"="
t_NOT   = "!"
t_NEQ   = r"!="
t_LEQ   = r"<="
t_GEQ   = r">="
t_DEFINE    = r":="
t_ELLIPSIS  = r"\.\.\."
t_LPAREN    = r"\("
t_LBRACK    = r"\["
t_LBRACE    = r"\{"
t_COMMA     = r","
t_PERIOD    = r"\."
t_RPAREN    = r"\)"
t_RBRACK    = r"\]"
t_RBRACE    = r"\}"
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
 
 # Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)