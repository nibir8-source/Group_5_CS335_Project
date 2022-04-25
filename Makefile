for_loop_array.go:
	./bin/codegen ./tests/final_tests/for_loop_array.go
	rm -rf *.asm *.o *.txt parser.out scopeTabDump *.p *.csv

break_continue.go:
	./bin/codegen ./tests/final_tests/break_continue.go
	rm -rf *.asm *.o *.txt parser.out scopeTabDump *.p *.csv

func_arg_depth.go:
	./bin/codegen ./tests/final_tests/func_arg_depth.go
	rm -rf *.asm *.o *.txt parser.out scopeTabDump *.p *.csv

if_else.go:
	./bin/codegen ./tests/final_tests/if_else.go
	rm -rf *.asm *.o *.txt parser.out scopeTabDump *.p *.csv

large_expression.go:
	./bin/codegen ./tests/final_tests/large_expression.go
	rm -rf *.asm *.o *.txt parser.out scopeTabDump *.p *.csv

pointer.go:
	./bin/codegen ./tests/final_tests/pointer.go
	rm -rf *.asm *.o *.txt parser.out scopeTabDump *.p *.csv

recursion.go:
	./bin/codegen ./tests/final_tests/recursion.go
	rm -rf *.asm *.o *.txt parser.out scopeTabDump *.p *.csv

struct.go:
	./bin/codegen ./tests/final_tests/struct.go
	rm -rf *.asm *.o *.txt parser.out scopeTabDump *.p *.csv

switch.go:
	./bin/codegen ./tests/final_tests/switch.go
	rm -rf *.asm *.o *.txt parser.out scopeTabDump *.p *.csv

