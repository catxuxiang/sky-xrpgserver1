'''
Created on 2012-6-3

@author: Sky
'''
from Scripts.Command import Command

class PythonCommand(Command):
    def __init__(self, p_character, p_classinstance):
        self.m_script = p_classinstance
        self.m_script.Call("Init", p_character)
        
    def __del__(self):
        if self.m_script:
            del self.m_script

    def Execute(self, p_parameters):
        self.m_script.Call("Execute", p_parameters)
        
    def GetName(self):
        return self.m_script.Call("GetName")
    
    def GetUsage(self):
        return self.m_script.Call("GetUsage")
    
    def GetDescription(self):
        return self.m_script.Call("GetDescription")
    
    def Load(self, sr, prefix):
        self.m_script.Load(sr, prefix)
        
    def Save(self, sr, prefix):
        self.m_script.Save(sr, prefix)

