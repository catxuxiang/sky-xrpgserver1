'''
Created on 2012-6-3

@author: Sky
'''
from Scripts.PythonScript import PythonDatabase
from Scripts.PythonLogic import PythonLogic

class LogicDatabase(PythonDatabase):
    def __init__(self):
        PythonDatabase.__init__(self, "logics")

    def Generate(self, p_str, p_id):
        logic = self.SpawnNew(p_str)
        l = PythonLogic(logic)
        l.Init(p_id)
        return l
    
LogicDB = LogicDatabase()
