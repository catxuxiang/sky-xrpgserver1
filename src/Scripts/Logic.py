'''
Created on 2012-5-30

@author: Sky
'''
from Scripts.Script import Script
class Logic(Script):
    def GetName(self):
        raise Exception("Virtual Method!")

    def CanSave(self):
        return True
    
    def GetAttribute(self, p_attr):
        raise Exception("Virtual Method!")
    
    def DoAction(self, p_action):
        raise Exception("Virtual Method!")
