# CS335_Go_Compiler
A Go compiler developed as part of the course project for CS335. </br>
SIT -> Go Python x86 </br>
Group Members:</br>
Adit Khokar 190054</br>
Nibir Baruah 190545</br>
Manish 190477</br>
Manish Mayank 190482</br>

<br>

# Milestone 1
Language Manual: https://github.com/nibir8-source/CS335_Go_Compiler/blob/main/docs/LanguageManual.pdf

<br>


# Milestone 2

The actual Scanner or Lexer is in the folder src/lexer named lexer.py, and lexer_driver.py in the same folder is the program that prints the output given by the lexer.<br>
The script lexer in the bin folder runs the lexer against test cases.<br>

For running the first test case given in the tests folder run the following command:<br>
 
./bin/lexer ./tests/test1.go<br>

And similarly for the rest of the test files(test2.go, test3.go, test4.go, test5.go)


# Milestone 3

The Parser exists in the folder src named parser.py.</br>

For running the first test case given in the tests folder run the following command:</br>

./bin/parser ./tests/parser_tests/test0.go</br>

And similarly for the rest of the test files(test1.go, test2.go, test3.go, test4.go)</br>

# Milestone 4

For running the first test case given in the tests folder run the following command:</br>

./bin/semantic ./tests/Ast_tests/test0.go</br>

And similarly for the rest of the test files(test1.go, test2.go, test3.go, test4.go)</br>
