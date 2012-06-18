'''
Created on 2012-6-3

@author: Sky
'''
from Scripts.Script import Script
class Command(Script):
    def Execute(self, p_parameters):
        raise Exception("Virtual Method!")
        
    def GetUsage(self):
        raise Exception("Virtual Method!")
    
    def GetDescription(self):
        raise Exception("Virtual Method!")
