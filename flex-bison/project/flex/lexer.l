%{

	#include "parser.tab.h"
	#include <stdio.h>
	#include <string.h>

	void echo (void);

%}

/* stop executing when you meet EOF */

%option noyywrap

/* automatically update the yylineno variable with the current number of lines */

%option yylineno

/* abstraction for easier use in ALPHA */

C									[A-Za-z0-9_ &.!:\-/]

/* Alplhanumeric handler for nested double or single quotes inside respectively opposite quotes */

ALPHA								(\"{C}*('({C}+)')?{C}*\")|('{C}*(\"({C}+)\"){C}*')

/* Text handler that doesn't recognize specific characters so that it may match only with text */

TEXT								[{C}{-}[\n\t<>/=]]+

%%

[ \t\r\n]							{ echo (); }

"\<!--"[^-]([^-]|-[^-])*"--\>"		{ echo (); }

"\<MYHTML\>"						{ echo (); return MYHTML; }
"\</MYHTML\>"						{ echo (); return MYHTML_; }

"\<head\>"							{ echo (); return HEAD; }
"\</head\>"							{ echo (); return HEAD_; }

"\<title\>"							{ echo (); return TITLE; }
"\</title\>"						{ echo (); return TITLE_; }

"\<meta"							{ echo (); return META; }

"\<body\>"							{ echo (); return BODY; }
"\</body\>"							{ echo (); return BODY_; }

"\<p"								{ echo (); return P; }
"\</p>"								{ echo (); return P_; }

"\<a"								{ echo (); return A; }
"</a\>"								{ echo (); return A_; }

"\<img"								{ echo (); return IMG; }

"\<form"							{ echo (); return FORM; }
"\</form\>"							{ echo (); return FORM_; }

"\<div"								{ echo (); return DIV; }
"\</div\>"							{ echo (); return DIV_; }

"charset"							{ echo (); return CHARSET; }
"name"								{ echo (); return NAME; }
"content"							{ echo (); return CONTENT; }

"id"								{ echo (); return ID; }

"style"								{ echo (); return STYLE; }

"href"								{ echo (); return HREF; }

"src"								{ echo (); return SRC; }
"alt"								{ echo (); return ALT; }
"width"								{ echo (); return WIDTH; }
"height"							{ echo (); return HEIGHT; }

"\<input"							{ echo (); return INPUT; }

"\<label"							{ echo (); return LABEL; }
"\</label\>"						{ echo (); return LABEL_; }

"type"								{ echo (); return TYPE; }

"value"								{ echo (); return VALUE; }

"for"								{ echo (); return FOR; }

"="									{ echo (); return ASSIGN; }

"\>"								{ echo (); return CT; }

{TEXT}								{ echo (); return TEXT; }

{ALPHA}								{ echo (); return ALPHA; }

%%

void echo (void) { printf ("%s", yytext); }