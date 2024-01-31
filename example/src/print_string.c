#include "good_header.h"

#include <iso646.h> // and
#include <stdio.h>  // perror
#include <unistd.h> // write STDOUT_FILENO

bool ensure_write(int file_descriptor, const char* string, size_t length)
{
	ssize_t returned;
	size_t  written = 0;

	while (written < length and (returned = write(file_descriptor, string + written, length - written)) > 0)
		written += returned;
	if (written == length)
		return true;
	perror("write");
	return false;
}

bool print_string(const char* string, size_t length)
{
	char buffer[length + 1];
	memcpy(buffer, string, length);
	buffer[length] = '\n';
	return ensure_write(STDOUT_FILENO, buffer, length + 1);
}
