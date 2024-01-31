#pragma once

/** @file bad_header.h */

const char some_global_array[10] = {'H', 'e', 'l', 'l', 'o'};
const int  some_global           = 42;

int defined_in_header(int parameter)
{
	return parameter;
}
