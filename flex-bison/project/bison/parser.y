%{

	#include <stdio.h>
	#include <stdlib.h>
	#include <string.h>

	extern int yylex (void);
	extern int yylineno;
	extern FILE * yyin;

	void yyerror (const char * msg);

%}

%token MYHTML MYHTML_
%token HEAD BODY HEAD_ BODY_
%token TITLE P A FORM LABEL DIV TITLE_ P_ A_ FORM_ LABEL_ DIV_
%token META IMG INPUT CT ASSIGN
%token CHARSET NAME CONTENT ID STYLE HREF SRC ALT WIDTH HEIGHT TYPE VALUE FOR
%token ALPHA TEXT

%%

myhtml		: MYHTML head body MYHTML_;

head		: %empty
			| HEAD title meta HEAD_;

title		: TITLE text TITLE_;

meta		: %empty
			| meta META name content CT
			| meta META charset CT;

body		: BODY body_cont BODY_;

body_cont	: %empty
			| body_cont div_cont
			| body_cont div;

div			: DIV id style CT div_cont DIV_;

div_cont	: form
			| img
			| a
			| p;

p			: P id style CT text P_;

a			: A id href CT a_cont A_;

a_cont		: text
			| img;

img			: IMG id src alt width height CT;

form		: FORM id style CT form_cont FORM_;

form_cont	: form_cont label
			| form_cont input
			| label
			| input;

input		: INPUT id type style value CT;

label		: LABEL id for style CT text LABEL_;

id			: ID ASSIGN ALPHA;

charset		: CHARSET ASSIGN ALPHA;

name		: NAME ASSIGN ALPHA;

content		: CONTENT ASSIGN ALPHA;

style		: %empty
			| STYLE ASSIGN ALPHA;

href		: HREF ASSIGN ALPHA;

src			: SRC ASSIGN ALPHA;

alt			: ALT ASSIGN ALPHA;

width		: %empty
			| WIDTH ASSIGN ALPHA;

height		: %empty
			| HEIGHT ASSIGN ALPHA;

value		: %empty
			| VALUE ASSIGN ALPHA;

type		: TYPE ASSIGN ALPHA;

for			: FOR ASSIGN ALPHA;

text		: %empty
			| TEXT;

%%

void yyerror (const char * msg) {

	// exiting stops at the location of error instead
	// of continuing to the end of file

	fprintf (stderr, "\n\nerror at line %d. Exiting...\n\n", yylineno);
	
	exit (0);
}

int main (int argc, char ** argv) {

	// used to deactivate buffer in console,
	// or the output doesn't make sense

	setvbuf (stdout, NULL, _IONBF, 0);

	// guard clause for launch with no args

	if (--argc < 1) return 0;

	// open file stream

	yyin = fopen (* ++argv, "r");

	// handle failure to open file stream

	if (!yyin) {

		perror ("file not found.\n\n");
		return 0;
	}

	printf ("\n");

	yyparse ();

	printf ("\n\nfile correctly formatted.\n\n");

	return 0;
}