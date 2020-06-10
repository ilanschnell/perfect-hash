#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>

#define NK  $NK       /* number of keys */
#define NG  $NG       /* number of vertices */
#define NS  $NS       /* length of salt strings */

int G[] = {$G};

char *K[] = {$K};


/* return index of `key` in K if key is found, -1 otherwise */
int get_index(char *k)
{
    int f1 = 0, f2 = 0, i;

    for (i = 0; k[i] != '\0' && i < NS; i++) {
        f1 += "$S1"[i] * k[i];
        f2 += "$S2"[i] * k[i];
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
    char *junk[] = {"ACASSICUHAIUSCSACASCASKHCKJHSAKJCHK827349RFEWIHIWUE",
                    "abc", "x", "99"};

    for (i = 0; i < 4; i++)
        assert(get_index(junk[i]) == -1);

    for (i = 0; i < NK; i++)
        assert(get_index(K[i]) == i);

    printf("OK\n");
    return 0;
}
