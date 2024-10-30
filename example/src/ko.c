/** @file ko.c */

#include <errno.h>  // errno
#include <signal.h> // signal
#include <stdio.h>  // printf
#include <string.h> // strerror

enum cardinal {
	north,
	east,
	south,
	west
};

const char* name(int i)
{
	switch (i)
	{
	case 1: return "Unique";
	case 2: return "Couple";
	case 42: return "Hitchhicker's Guide";
	case 314: return "100 circles";
	}
}

const char* cardinal_to_string(enum cardinal cardinal)
{
	switch (cardinal)
	{
	case north: return "North";
	case east: return "East";
	case south: return "South";
	}
}

static void my_handler(int signum)
{
	(void)signum;
}

void foobarbaz(void)
{
	if (signal(SIGALRM, my_handler) == SIG_ERR)
	{
		printf("Error registering signal handler: %s", strerror(errno));
	}
}
