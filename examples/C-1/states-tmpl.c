#include <string.h>
#include <assert.h>

#include "states-code.h"


static int T1[] = {$S1};
static int T2[] = {$S2};
static int G[] = {$G};
static char *K[] = {$K};

static int
hash_g(const char *key, const int *T)
{
    int i, sum = 0;

    for (i = 0; key[i] != '\0'; i++) {
        assert(i < $NS);
        sum += T[i] * key[i];
        sum %= $NG;
    }
    return G[sum];
}

/* return index of `key` in K if key is found, -1 otherwise */
int index_key(const char *key)
{
    int hash_value;

    if (strlen(key) > $NS)
        return -1;

    hash_value = (hash_g(key, T1) + hash_g(key, T2)) % $NG;
    if (hash_value < $NK && strcmp(key, K[hash_value]) == 0)
        return hash_value;

    return -1;
}
