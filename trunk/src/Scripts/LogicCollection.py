'''
Created on 2012-5-30

@author: Sky
'''
from Db.LogicDatabase import LogicDB
from Entities.Attributes import Databank

class LogicCollection:
    def __init__(self):
        self.m_collection = Databank()
        
    def Get(self, p_name):
        return self.m_collection.Get(p_name)
    
    def AddExisting(self, l):
        self.m_collection.Add(l.GetName(), l)
        
    def Add(self, p_name, p_id):
        l = LogicDB.Generate(p_name, p_id)
        self.AddExisting(l)
        
    def Del(self, p_name):
        l = self.m_collection.Get(p_name)
        del l
        self.m_collection.Del(p_name)
        
    def Has(self, p_name):
        return self.m_collection.Has(p_name)
    
    def GetAttribute(self, p_module, p_attr):
        return self.m_collection.Get(p_module).GetAttribute(p_attr)
    
    def DoAction(self, p_action):
        for item in self.m_collection:
            i = self.m_collection[item].DoAction(p_action)
            if i != 0:
                return i
        return 0
    
    def Load(self, sr, prefix, p_id):
        prefix += ":LOGICS"
        for i in sr.hkeys(prefix):
            self.Add(i, p_id)
            c = self.Get(i)
            #c.Load(sr.hget(prefix, i))
            
    def Save(self, sr, prefix):
        prefix += ":LOGICS"
        for i in self.m_collection:
            item = self.m_collection[i]
            if item.CanSave():
                sr.hset(prefix, item.GetName(), "")
                #item.Save(sr, prefix)