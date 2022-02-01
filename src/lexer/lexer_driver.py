import lexer
import sys
import pandas as pd

if(len(sys.argv) == 1):
    print("[ERROR!] Enter File Name")
    sys.exit(1)

file = open(sys.argv[1], 'r')
data = file.read()

Tokens = lexer.Process(data)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

df = pd.DataFrame([[tok.type,tok.value,tok.lineno,lexer.find_column(data,tok)] for tok in Tokens])
df = df.rename(columns={0:'Token',1:'Lexeme',2:'Line#',3:'Column#'})

print(df)