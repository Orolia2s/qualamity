/** @file ko.c */

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
