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


