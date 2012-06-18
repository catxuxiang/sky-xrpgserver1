'''
Created on 2012-6-2

@author: Sky
'''
from Entities.LogicEntity import LogicEntity
from Entities.DataEntity import DataEntity
from Entities.Entity import HasRegion, HasCharacters, HasItems, HasPortals

class Room(LogicEntity, DataEntity, HasRegion, HasCharacters, HasItems, HasPortals):
    def __init__(self):
        LogicEntity.__init__(self)
        DataEntity.__init__(self)
        HasRegion.__init__(self)
        HasCharacters.__init__(self)
        HasItems.__init__(self)
        HasPortals.__init__(self)
        
    def Load(self, sr, prefix):
        #self.Remove()
        
        self.m_region = sr.get(prefix + ":REGION")
        self.m_name = sr.get(prefix + ":NAME")
        self.m_description = sr.get(prefix + ":DESCRIPTION")
        
        self.m_attributes.Load(sr, prefix)
        
        self.m_logic.Load(sr, prefix, self.m_id)
        
        #self.Add()
        
    def Save(self, sr, prefix):
        sr.set(prefix + ":REGION", self.m_region)
        sr.set(prefix + ":NAME", self.m_name)
        sr.set(prefix + ":DESCRIPTION", self.m_description)
        
        self.m_attributes.Save(sr, prefix)
        
        self.m_logic.Save(sr, prefix)
        
    def Add(self, region):
        if self.m_region != "0" and self.m_id != "0":
            r = region(self.m_region)
            r.AddRoom(self.m_id)
            
    def Remove(self, region):
        if self.m_region != "0" and self.m_id != "0":
            r = region(self.m_region)
            r.DelRoom(self.m_id)
