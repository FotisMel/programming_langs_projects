default: lexer parser program

demo: myParser.exe ../test/ok.myhtml ../test/lex.myhtml ../test/syn.myhtml ../test/com.myhtml
	./myParser.exe ../test/ok.myhtml
	./myParser.exe ../test/lex.myhtml
	./myParser.exe ../test/syn.myhtml
	./myParser.exe ../test/com.myhtml

program: parser.tab.c lex.yy.c
	gcc -o myParser.exe parser.tab.c lex.yy.c -lfl

parser: ../bison/parser.y
	bison -d ../bison/parser.y

lexer: ../flex/lexer.l
	flex ../flex/lexer.l

clean:
	rm ./*.*