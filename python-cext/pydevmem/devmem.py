
import _devmem

def usage():
    _devmem.usage()

def read_mem(addr=None):
    return _devmem.devmem_read(addr)

def write_mem(addr=None, value=None):
    return _devmem.devmem_write(addr, value)