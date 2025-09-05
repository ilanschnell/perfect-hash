#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "keys.code.h"


/* return index of key in K if key is found, -1 otherwise */
int get_index(const char *key)
{
    int f1 = 0, f2 = 0, i;
    unsigned char c;

    for (i = 0; (c = key[i]) && i < NS; i++) {
        f1 += S1[i] * c;
        f2 += S2[i] * c;
    }
    i = (G[f1 % NG] + G[f2 % NG]) % NG;
    if (i < NK && strcmp(key, K[i]) == 0)
        return i;

    return -1;
}

int main()
{
    char *key;
    int i;

    key = (char *) malloc(64);
    for (i = 0; i < NK; i++) {
        strcpy(key, K[i]);
        key[2] = '+';
        assert(get_index(key) == -1);
    }

    for (i = 0; i < NK; i++)
        assert(get_index(K[i]) == i);

    printf("OK\n");

    return 0;
}
