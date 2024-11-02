import ctypes

#calling libraray
clib = ctypes.CDLL("clibrary.so")

# displaying functions
clib.display()