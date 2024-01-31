/** @file abs.c */

#include <stdlib.h>

int abs(int i)
{
	return i < 0 ? -i : i; // Todo: Use libc
}

const char* time()
{
	return (const char*)system("time");
}

int strtoi(const char* string)
{
	return atoi(string);
}
