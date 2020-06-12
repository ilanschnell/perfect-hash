#ifndef STH
#define STH

struct {
    char *name;
    char *abbr;
    int pop;
} states[] = {
#include "states.dat.h"
};

int get_hashval(const char *key);

#endif  /* STH */
