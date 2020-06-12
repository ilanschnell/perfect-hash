#ifndef STH
#define STH

struct {
    char *name;
    char *abbr;
    int pop;
} states[] = {
#include "states.dat.h"
};

int get_index(const char *key);

#endif  /* STH */
