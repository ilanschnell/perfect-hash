#include "Python.h"

#if PY_MAJOR_VERSION == 2
#error "no supported for Python 2"
#endif

#include "stations-code.h"

static struct {
    char *callsign;
    char *locator;
} station_list[] = {
#include "stations.dat.h"
};

/* return index of `key` in K if key is found, -1 otherwise */
static int get_index(const char *key)
{
    int f1 = 0, f2 = 0, i;

    for (i = 0; key[i] && i < NS; i++) {
        unsigned char c = key[i];
        f1 += S1[i] * c;
        f2 += S2[i] * c;
    }
    i = (G[f1 % NG] + G[f2 % NG]) % NG;
    if (i < NK && strcmp(key, station_list[i].callsign) == 0)
        return i;

    return -1;
}

static PyObject *stations_locator(PyObject *self, PyObject *obj)
{
    const char *callsign;
    int index;

    if (!PyUnicode_Check(obj)) {
        PyErr_SetString(PyExc_TypeError, "string expected");
        return NULL;
    }
    callsign = PyUnicode_AsUTF8(obj);
    index = get_index(callsign);
    if (index < 0) {
        PyErr_SetString(PyExc_KeyError, callsign);
        return NULL;
    }
    return PyUnicode_FromString(station_list[index].locator);
}

static PyMethodDef module_functions[] = {
    {"locator", stations_locator, METH_O, "Get locator from callsign."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT, "stations", 0, -1, module_functions,
};

PyMODINIT_FUNC
PyInit_stations(void)
{
    PyObject *m;

    m = PyModule_Create(&moduledef);
    if (m == NULL)
        return NULL;

    return m;
}
