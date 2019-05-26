#include "Python.h"

#include "stations-code.h"

static struct {
    char *callsign;
    char *locator;
} station_list[] = {
#include "stations.dat.h"
};

static unsigned int
DEKhash(const unsigned int init, const char *s)
{
    register unsigned int x;

    x = init;
    for (; *s != '\0'; s++)
        x = ((x << 5) ^ (x >> 27) ^ (*s)) % (1 << 31);

    return x;
}

static int
perf_hash(const char *k)
{
    return (G[DEKhash(S1, k) % NG] + G[DEKhash(S2, k) % NG]) % NG;
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
    {"locator", stations_locator, METH_VARARGS, "Get locator from callsign."},
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
