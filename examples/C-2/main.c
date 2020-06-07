#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>

#include "keys.code.h"


int hash_g(char *s, int *T)
{
    int i, f = 0;

    for (i = 0; s[i] != '\0'; i++) {
        assert(i < NS);
        f += T[i] * s[i];
        f %= NG;
    }
    return G[f];
}

/* return index of `key` in K if key is found, -1 otherwise */
int get_index(char *k)
{
    int h;

    if (strlen(k) > NS)
        return -1;

    h = (hash_g(k, T1) + hash_g(k, T2)) % NG;
    if (h < NK && strcmp(k, K[h]) == 0)
        return h;

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
