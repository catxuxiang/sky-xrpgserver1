'''
Created on 2012-5-30

@author: Sky
'''
from Entities.Attributes import Databank

class DataEntity:
    def __init__(self):
        self.m_attributes = Databank()
        
    def GetAttribute(self, p_name):
        return self.m_attributes.Get(p_name)
    
    def SetAttribute(self, p_name, p_val):
        self.m_attributes.Set(p_name, p_val)
        
    def HasAttribute(self, p_name):
        return self.m_attributes.Has(p_name)

    def AddAttribute(self, p_name, p_initialval):
        self.m_attributes.Add(p_name, p_initialval)
        
    def DelAttribute(self, p_name):
        self.m_attributes.Del(p_name)
