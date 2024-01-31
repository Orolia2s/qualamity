/** @file main.c */

#include "bad_header.h"
#include "good_header.h" // print_string

#include <stdio.h>  // getc putc stdin stdout
#include <stdlib.h> // getenv system abort EXIT_SUCCESS

int isdigit(int c)
{
	return '0' <= c && c <= '9';
}

int main(int ac, char** av)
{
	while (--ac && *++av)
		print_string(*av);
	return EXIT_SUCCESS;
}

void do_something(void)
{
	int c = getc(stdin);
	if (isdigit(c))
	{
		getenv("SHLVL");
		system(":");
		abort(); // TODO: handle cleanly
	}
	putc(c, stdout);
	_Exit(0);
}
