'''
Created on 2012-6-2

@author: Sky
'''
from Entities.LogicEntity import LogicEntity
from Entities.DataEntity import DataEntity
from Entities.Entity import HasCharacters, HasItems, HasRooms, HasPortals
class Region(LogicEntity, DataEntity, HasCharacters, HasItems, HasRooms, HasPortals):
    def __init__(self):
        LogicEntity.__init__(self)
        DataEntity.__init__(self)
        HasCharacters.__init__(self)
        HasItems.__init__(self)
        HasRooms.__init__(self)
        HasPortals.__init__(self)
        
        self.m_diskname = ""
    
    def GetDiskname(self):
        return self.m_diskname
    
    def SetDiskname(self, p_name):
        self.m_diskname = p_name
        
    def Load(self, sr, prefix):
        self.m_name = sr.get(prefix + ":NAME")
        self.m_description = sr.get(prefix + ":DESCRIPTION")
        
        self.m_attributes.Load(sr, prefix)
        
        self.m_logic.Load(sr, prefix, self.m_id)
        
    def Save(self, sr, prefix):
        sr.set(prefix + ":NAME", self.m_name)
        sr.set(prefix + ":DESCRIPTION", self.m_description)
        
        self.m_attributes.Save(sr, prefix)
        
        self.m_logic.Save(sr, prefix)