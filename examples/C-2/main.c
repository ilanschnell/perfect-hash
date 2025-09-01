#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>

#include "keys.code.h"


/* return index of key in K if key is found, -1 otherwise */
int get_index(const char *key)
{
    int i, f1 = 0, f2 = 0;

    for (i = 0; key[i] && i < NS; i++) {
        unsigned char c = key[i];
        f1 += S1[i] * c;
        f2 += S2[i] * c;
        f1 %= NG;
        f2 %= NG;
    }
    i = (G[f1] + G[f2]) % NG;
    if (i < NK && strcmp(key, K[i]) == 0)
        return i;

    return -1;
}

int main()
{
    int i;

    char *junk = "acnhuvn5yushvghnw7og5siuhgsiuhnglsh45vgghwn";

    assert(get_index(junk) == -1);

    for (i = 0; i < NK; i++) {
        /* printf("i=%d    %s     %d\n", i, K[i], get_index(K[i])); */
        assert(get_index(K[i]) == i);
    }

    puts("OK");

    return 0;
}
