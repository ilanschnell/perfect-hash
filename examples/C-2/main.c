#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>

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
    if (strcmp(key, K[i]) == 0)
        return i;

    return -1;
}

int main()
{
    int i;

    assert(get_index("A.B") == -1);

    for (i = 0; i < NK; i++) {
        assert(get_index(K[i]) == i);
    }

    puts("OK");

    return 0;
}
