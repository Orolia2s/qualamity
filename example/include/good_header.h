#pragma once

#include <stdbool.h>
#include <string.h> // strlen

int               my_function(int parameter);

extern const int  my_global;
extern const char my_global_array[20];

bool ensure_write(int file_descriptor, const char* string, size_t length);
bool print_string(const char* string, size_t length);

#define print_string_(STRING, LENGTH, ...) print_string(STRING, LENGTH)
#define print_string(STRING, ...) print_string_(STRING, ## __VA_ARGS__, strlen(STRING))
