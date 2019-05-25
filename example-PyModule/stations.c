#include "Python.h"

#include "stations-code.h"

static struct {
    char *callsign;
    char *locator;
} station_list[] = {
#include "stations.dat.h"
};

static int
hash_f(const char *s, const int *T)
{
    register int i, sum = 0;

    for (i = 0; s[i] != '\0'; i++) {
        sum += T[i] * s[i];
        sum %= NG;
    }
    return sum;
}

static int
perf_hash(const char *k)
{
    if (strlen(k) > NS)
        return 0;

    return (G[hash_f(k, T1) ] + G[hash_f(k, T2)]) % NG;
}

static int
getlocator(const char *callsign, char *locator)
{
    int hashval = perf_hash(callsign);

    if (hashval < NK &&
        strcmp(callsign, station_list[hashval].callsign) == 0)
        {
            strcpy(locator, station_list[hashval].locator);
            return 1;
        }
    return 0;
}

static PyObject *
stations_locator(PyObject *self, PyObject *args)
{
    char *callsign;
    char locator[7];

    if (!PyArg_ParseTuple(args, "s", &callsign))
        return NULL;

    if (getlocator(callsign, locator) == 1)
        return PyString_FromString(locator);
    else
        Py_RETURN_NONE;
}

static PyMethodDef module_functions[] = {
    {"locator",  stations_locator, METH_VARARGS, "Get locator from callsign."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
initstations(void)
{
    PyObject *m;

    m = Py_InitModule3("stations", module_functions, 0);
    if (m == NULL)
        return;
    PyModule_AddObject(m, "__version__", PyString_FromString("1.0.0"));
}
