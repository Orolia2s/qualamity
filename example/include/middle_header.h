#pragma once

#include <math.h> // sqrt

static const int answer = 42;

inline float     square_root(float number)
{
	return sqrtf(number);
};

void do_nothing(void);
int  print_env(int ac, const char* const* av, const char* const* env);
