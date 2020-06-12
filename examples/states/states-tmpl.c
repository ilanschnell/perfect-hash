#define NK  $NK       /* number of keys */
#define NG  $NG       /* number of vertices */
#define NS  $NS       /* length of array S1 and S2 */

static int S1[] = {$S1};
static int S2[] = {$S2};
static int G[] = {$G};


/* return hashval of key, -1 if key is definitely not a key */
int get_hashval(const char *key)
{
    int i, f1 = 0, f2 = 0;

    for (i = 0; key[i] != '\0' && i < NS; i++) {
        f1 += S1[i] * key[i];
        f2 += S2[i] * key[i];
    }
    i = (G[f1 % NG] + G[f2 % NG]) % NG;
    return (i < NK) ? i : -1;
}
