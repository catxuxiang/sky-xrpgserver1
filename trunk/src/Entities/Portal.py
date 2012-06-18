'''
Created on 2012-6-2

@author: Sky
'''
from Entities.Entity import HasRegion
from Entities.LogicEntity import LogicEntity
from Entities.DataEntity import DataEntity

class portalentry:
    def __init__(self):
        self.startroom = "0"
        self.directionname = ""
        self.destinationroom = "0"
        
    def Load(self, sr, prefix):
        self.startroom = sr.get(prefix + ":STARTROOM")
        self.directionname = sr.get(prefix + ":DIRECTION")
        self.destinationroom = sr.get(prefix + ":DESTROOM")
        
    def Save(self, sr, prefix):
        sr.set(prefix + ":STARTROOM", self.startroom)
        sr.set(prefix + ":DIRECTION", self.directionname)
        sr.set(prefix + ":DESTROOM", self.destinationroom)

class Portal(LogicEntity, DataEntity, HasRegion):
    def __init__(self):
        LogicEntity.__init__(self)
        DataEntity.__init__(self)
        HasRegion.__init__(self)
        
        self.m_portals = []
        
    def Load(self, sr, prefix):
        #self.Remove()
        
        self.m_region = sr.get(prefix + ":REGION")
        self.m_name = sr.get(prefix + ":NAME")
        self.m_description = sr.get(prefix + ":DESCRIPTION")
        
        self.m_portals = []
        for i in range(sr.llen(prefix + ":ENTRY")):
            data = sr.lindex(prefix + ":ENTRY", i)
            e = portalentry()
            e.Load(sr, prefix + ":ENTRY:" + data)
            self.m_portals.append(e)
            
        self.m_attributes.Load(sr, prefix)
        
        self.m_logic.Load(sr, prefix, self.m_id)
        
        #self.Add()
        
    def Save(self, sr, prefix):
        sr.set(prefix + ":REGION", self.m_region)
        sr.set(prefix + ":NAME", self.m_name)
        sr.set(prefix + ":DESCRIPTION", self.m_description)
        
        sr.ltrim(prefix + ":ENTRY", 2, 1)
        i = 0
        for portal in self.m_portals:
            sr.rpush(prefix + ":ENTRY", i)
            portal.Save(sr, prefix + ":ENTRY:" + str(i))
            i += 1
            
        self.m_attributes.Save(sr, prefix)
        
        self.m_logic.Save(sr, prefix)
        
    def Remove(self, region, room):
        if self.m_region != "0":
            reg = region(self.m_region)
            reg.DelPortal(self.m_id)
            
        for i in self.m_portals:
            r = room(i.startroom)
            r.DelPortal(self.m_id)
            
    def Add(self, region, room):
        if self.m_region != "0":
            reg = region(self.m_region)
            reg.AddPortal(self.m_id)
            
        for i in self.m_portals:
            r = room(i.startroom)
            r.AddPortal(self.m_id)