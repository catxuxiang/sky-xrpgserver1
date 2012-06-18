'''
Created on 2012-6-3

@author: Sky
'''
class PythonObject:
    def __init__(self, p_object):
        if type(p_object) == PythonObject:
            self.m_object = p_object.m_object
        else:
            self.m_object = p_object
            
    def Get(self):
        return self.m_object
    
    def Has(self, p_name):
        return p_name in dir(self.m_object)
    
    def GetNameOfClass(self):
        cls = getattr(self.m_object, "__class__")
        return getattr(cls, "__name__")
    
    def GetName(self):
        return getattr(self.m_object, "__name__")