
#include <Python.h>
#include "lib/devmem2.h"

static PyObject *DevMemError;

static PyObject* devmem_usage(PyObject *self, PyObject *args) {
    usage();
    Py_RETURN_NONE;
}

static PyObject* devmem_read(PyObject *self, PyObject *args) {
    int ok;
    unsigned long addr;
    unsigned int value = 0;
    ok = PyArg_ParseTuple(args, "l", &addr);
    if (ok) {
        value = read_addr((off_t)addr);
    }
    return Py_BuildValue("i", value);
}

static PyObject* devmem_write(PyObject *self, PyObject *args) {
    int ok;
    unsigned long addr;
    unsigned int value = 0, write_value;
    ok = PyArg_ParseTuple(args, "ll", &addr, &write_value);
    if (ok) {
        value = write_addr((off_t)addr, write_value);
    }
    return Py_BuildValue("i", value);
}

static PyMethodDef DevMemMethods[] = {
    {"devmem_usage",  devmem_usage, METH_NOARGS,
     "print usage of devemem"},
    {"devmem_read",  devmem_read, METH_VARARGS,
     "read data at memory location"},
    {"devmem_write",  devmem_write, METH_VARARGS,
     "write given data at the memory location"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef DevMemModule = {
   PyModuleDef_HEAD_INIT,
   "_devmem",   /* name of module */
   NULL, /* module documentation, may be NULL */
   -1,       /* size of per-interpreter state of the module,
                or -1 if the module keeps state in global variables. */
   DevMemMethods
};

PyMODINIT_FUNC
PyInit__devmem(void)
{

    PyObject *module = PyModule_Create(&DevMemModule);

    if (module == NULL) {
      return NULL;
    }

    DevMemError = PyErr_NewException("devmem.Error", NULL, NULL);
    Py_INCREF(DevMemError);
    PyModule_AddObject(module, "Error", DevMemError);
    return module;

}