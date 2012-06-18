'''
Created on 2012-4-14

@author: Sky
'''
import sys
import os
import time
import inspect

def Import(modulename):
    dirname = os.path.dirname(os.path.abspath(modulename))
    filename, ext = os.path.splitext(os.path.basename(modulename))
    if ext.lower() != ".py":
        return None
    if filename in sys.modules:
        del sys.modules[filename]
    if dirname:
        sys.path.insert(0, dirname)
    mod = __import__(filename)
    if dirname:
        del sys.path[0]
    return mod

mod = Import("../data/commands/test2.py")
#print(mod)
#print(dir(mod))
#getattr(mod, "AA")(1, 2, 3)
x= getattr(mod, "AA")
y=inspect.getargspec(x).args
print(y)
#print("B" in dir(mod))
mod = getattr(mod, "B")()
mod1 = getattr(mod, "BB")
z = inspect.getargspec(mod1).args
print(z)
cls = getattr(mod, "__class__")
#print(cls)
#print(getattr(cls, "__name__"))





