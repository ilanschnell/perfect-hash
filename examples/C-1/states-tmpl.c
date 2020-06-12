#include <string.h>

#define NK  $NK       /* number of keys */
#define NG  $NG       /* number of vertices */
#define NS  $NS       /* length of array T1 and T2 */

static int S1[] = {$S1};
static int S2[] = {$S2};
static int G[] = {$G};
static char *K[] = {$K};


/* return index of `key` in K if key is found, -1 otherwise */
int get_index(const char *key)
{
    int i, f1 = 0, f2 = 0;

    for (i = 0; key[i] != '\0' && i < NS; i++) {
        f1 += S1[i] * key[i];
        f2 += S2[i] * key[i];
    }
    i = (G[f1 % NG] + G[f2 % NG]) % NG;
    if (i < NK && strcmp(key, K[i]) == 0)
        return i;

    return -1;
}
