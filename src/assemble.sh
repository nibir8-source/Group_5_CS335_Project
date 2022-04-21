#!/bin/sh

python3 parser.py test.go
python3 codegen.py

nasm -f elf32 "assembly.asm" -o "assembly.o"
gcc -m32 "assembly.o" -o "a.out"