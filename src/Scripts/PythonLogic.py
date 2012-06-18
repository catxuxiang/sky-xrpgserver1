'''
Created on 2012-6-3

@author: Sky
'''
from Scripts.Logic import Logic

class PythonLogic(Logic):
    def __init__(self, p_inst):
        self.m_instance = p_inst
        
    def __del__(self):
        del self.m_instance
        
    def GetName(self):
        return self.m_instance.GetName()


    def Init(self, p_id):
        self.m_instance.Call("Init", p_id)
        
    def GetAttribute(self, p_attr):
        return self.m_instance.Call("Attribute", p_attr)
    
    def DoAction(self, p_action):
        return self.m_instance.Call("Execute", p_action.actiontype, p_action.data1, p_action.data2, p_action.data3, p_action.data4, p_action.stringdata)
