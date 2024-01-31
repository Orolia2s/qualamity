#include "middle_header.h"

#include <stdio.h>  // fgetc stdin fputc stdout
#include <string.h> // strlen
#include <unistd.h> // write

void do_nothing(void)
{
	char c = fgetc(stdin);
	return ;
}

int print_env(int ac, const char* const* av, const char* const* env)
{
	while (*env)
	{
		write(1, *env, strlen(*env));
		fputc('\n', stdout);
		env++;
	}
	return 0;
}
