#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>

#define NK  $NK       /* number of keys */
#define NG  $NG       /* number of vertices */
#define NS  $NS       /* length of salt strings */

int G[] = {$G};

char *K[] = {$K};


/* return index of key in K if key is found, -1 otherwise */
int get_index(const char *key)
{
    int f1 = 0, f2 = 0, i;

    for (i = 0; key[i] && i < NS; i++) {
        unsigned char c = key[i];
        f1 += "$S1"[i] * c;
        f2 += "$S2"[i] * c;
    }
    i = (G[f1 % NG] + G[f2 % NG]) % NG;
    if (i < NK && strcmp(key, K[i]) == 0)
        return i;

    return -1;
}

int main()
{
    int i;
    char *junk[] = {"Überflieger", "abc", "König", "99"};

    for (i = 0; i < 4; i++) {
        printf("'%s'\n", junk[i]);
        assert(get_index(junk[i]) == -1);
    }

    for (i = 0; i < NK; i++) {
        printf("'%s'\n", K[i]);
        assert(get_index(K[i]) == i);
    }

    printf("OK\n");
    return 0;
}
