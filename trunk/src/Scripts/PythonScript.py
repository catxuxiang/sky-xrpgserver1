'''
Created on 2012-6-3

@author: Sky
'''
import os
import sys
import inspect
import traceback
from Scripts.PythonObject import PythonObject
from Scripts.Script import SCRIPTRELOADMODE_LEAVEEXISTING
from BasicLib.Redis import sr

class PythonCallable:
    def __init__(self, p_object = None):
        self.m_module = p_object
        
    def Has(self, p_name):
        return self.m_module.Has(p_name)
    
    def Get(self):
        return self.m_module.Get()
    
    def PrintErrorStack(self):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print("*** print_tb:")
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        print("*** print_exception:")
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                  limit=2, file=sys.stdout)
        print("*** print_exc:")
        traceback.print_exc()
        '''
        print("*** format_exc, first and last line:")
        formatted_lines = traceback.format_exc().splitlines()
        print(formatted_lines[0])
        print(formatted_lines[-1])
        print("*** format_exception:")
        print(repr(traceback.format_exception(exc_type, exc_value,
                                              exc_traceback)))
        print("*** extract_tb:")
        print(repr(traceback.extract_tb(exc_traceback)))
        print("*** format_tb:")
        print(repr(traceback.format_tb(exc_traceback)))
        print("*** tb_lineno:", exc_traceback.tb_lineno)
        '''
    
    def Call(self, p_name, p_arg1 = "", p_arg2 = "0", p_arg3 = "0", p_arg4 = "0", p_arg5 = "0", p_arg6 = ""):
        method = getattr(self.m_module.m_object, p_name)
        num = len(inspect.getargspec(method).args)
        if num != 0 and inspect.getargspec(method).args[0] == "self":
            num -= 1
        try:
            if num == 0:
                return method()
            elif  num == 1:
                return method(p_arg1)
            elif  num == 2:
                return method(p_arg1, p_arg2)
            elif  num == 3:
                return method(p_arg1, p_arg2, p_arg3)
            elif  num == 4:
                return method(p_arg1, p_arg2, p_arg3, p_arg4)
            elif  num == 5:
                return method(p_arg1, p_arg2, p_arg3, p_arg4, p_arg5)
            elif  num == 6:
                return method(p_arg1, p_arg2, p_arg3, p_arg4, p_arg5, p_arg6)
        except Exception:
            self.PrintErrorStack()

class PythonModule(PythonCallable):
    def __init__(self):
        PythonCallable.__init__(self)
        self.m_spawns = []
        self.m_path = ""
        
    def GetName(self):
        return self.m_path
    
    def Import(self, modulename):
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
    
    def Load(self, p_path):
        self.m_path = p_path
        p = PythonObject(self.Import(self.m_path))
        if p.Get() == None:
            raise Exception("Couldn't load python module: " + self.m_path)
        self.m_module = p
        
    def Reload(self, p_mode):
        if self.m_path == "":
            raise Exception("Load path is empty!")
        
        self.m_module = PythonObject(self.Import(self.m_path))
        
        if p_mode == SCRIPTRELOADMODE_LEAVEEXISTING:
            return
        
        for i in self.m_spawns:
            i.Reload()
    
    def SpawnNew(self, p_str):
        c = PythonObject(getattr(self.m_module.m_object, p_str))
        if c.Get() == None:
            raise Exception("Could not find python class: " + p_str)
        
        i = PythonObject(c.Get()())
        if i.Get() == None:
            raise Exception("Could not create python class instance: " + p_str)
        
        mod = PythonInstance(i, self)
        if not mod:
            raise Exception("Error allocating memory for python module")
        self.m_spawns.append(mod)
        
        return mod
    
    def DeleteChild(self, p_instance):
        i = 0
        for data in self.m_spawns:
            if data == p_instance:
                break
            i += 1
        if i < len(self.m_spawns):
            del self.m_spawns[i]
    
class PythonInstance(PythonCallable):
    def __init__(self, p_instance, p_parent):
        PythonCallable.__init__(self, p_instance)
        self.m_parent = p_parent
        
    def GetName(self):
        return self.m_module.GetNameOfClass()
    
    def __del__(self):
        if self.m_parent != None:
            self.m_parent.DeleteChild(self)
            
    def Reload(self):
        clsname = self.m_module.GetNameOfClass()
        
        cls = PythonObject(getattr(self.m_parent.Get(), clsname))
        
        if cls.Get() == None:
            raise Exception("Could not find python class: " + clsname)
        
        setattr(self.m_module.Get(), "__class__", cls.Get())
        
    def Load(self, sr, prefix):
        self.Call("LoadScript", sr.get(prefix + ":DATA"))
        
    def Save(self, sr, prefix):
        sr.set(prefix + ":DATA", self.Call("SaveScript"))
    
class PythonDatabase:
    def __init__(self, p_directory):
        self.m_directory = p_directory
        self.m_modules = []
        
    def __del__(self):
        self.m_modules = []
        
    def Load(self):
        for i in range(0, sr.llen(self.m_directory)):
            modulename = sr.lindex(self.m_directory, i)
            self.LoadModule(modulename)
            
    def AddModule(self, p_module):
        self.LoadModule(p_module)
        sr.rpush(self.m_directory, p_module)
        
    def LoadModule(self, p_module):
        mod = PythonModule()
        if not mod:
            raise Exception("Not enough memory to load python module")
        
        mod.Load(p_module)
        self.m_modules.append(mod)
        
    def Reload(self, p_module, p_mode):
        try:
            for i in self.m_modules:
                if i.GetName() == p_module:
                    i.Reload(p_mode)
                    return
            #if we got this far, then the module doesn't exist, so load it
            self.LoadModule(p_module)
        except:
            self.PrintErrorStack()

        
    def SpawnNew(self, p_str):
        for i in self.m_modules:
            if i.Has(p_str):
                return i.SpawnNew(p_str)
        raise Exception("Error: Cannot load module: " + p_str)