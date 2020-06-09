#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>

#include "keys.code.h"


/* return index of `key` in K if key is found, -1 otherwise */
int get_index(char *k)
{
    int f1 = 0, f2 = 0, i;

    for (i = 0; k[i] != '\0' && i < NS; i++) {
        f1 += S1[i] * k[i];
        f2 += S2[i] * k[i];
        f1 %= NG;
        f2 %= NG;
    }
    i = (G[f1] + G[f2]) % NG;
    if (i < NK && strcmp(k, K[i]) == 0)
        return i;

    return -1;
}

int main()
{
    int i;

    char *junk = "ACASSICUHAIUSCSACASCASKHCKJHSAKJCHK827349RFEWIHIWUEHUI";
    assert(get_index(junk) == -1);

    for (i = 0; i < NK; i++) {
        /* printf("i=%d    %s     %d\n", i, K[i], get_index(K[i])); */
        assert(get_index(K[i]) == i);
    }

    printf("OK\n");
    return 0;
}
