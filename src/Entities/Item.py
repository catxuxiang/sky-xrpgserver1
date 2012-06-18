'''
Created on 2012-6-1

@author: Sky
'''
from Entities.Entity import Entity, HasRoom, HasRegion, HasTemplateId
from Entities.DataEntity import DataEntity
from Entities.LogicEntity import LogicEntity
from Entities.Attributes import Databank

class ItemTemplate(Entity, DataEntity):
    def __init__(self):
        Entity.__init__(self)
        DataEntity.__init__(self)
        self.m_isquantity = False
        self.m_quantity = 1
        self.m_logics = []
        self.m_room = "0"
        self.m_region = "0"
        
    def IsQuantity(self):
        return self.m_isquantity
    
    def GetQuantity(self):
        return self.m_quantity
    
    def Load(self, sr, prefix):
        self.m_name = sr.get(prefix + ":NAME")
        self.m_description = sr.get(prefix + ":DESCRIPTION")
        self.m_isquantity = sr.get(prefix + ":ISQUANTITY")
        if self.m_isquantity == "False":
            self.m_isquantity = False
        else:
            self.m_isquantity = True
        self.m_quantity = int(sr.get(prefix + ":QUANTITY"))
        
        self.m_attributes.Load(sr, prefix)
        
        logics = sr.get(prefix + ":LOGICS").split(" ")
        self.m_logics = []
        for i in logics:
            self.m_logics.append(i)
    
class Item(LogicEntity, DataEntity, HasRoom, HasRegion, HasTemplateId):
    def __init__(self):
        LogicEntity.__init__(self)
        DataEntity.__init__(self)
        HasRoom.__init__(self)
        HasRegion.__init__(self)
        HasTemplateId.__init__(self)
        
        self.m_isquantity = False
        self.m_quantity = 1
        
    def GetName(self):
        if self.m_isquantity:
            return self.m_name.replace("<#>", str(self.m_quantity))
        else:
            return self.m_name        
        
    def IsQuantity(self):
        return self.m_isquantity
    
    def GetQuantity(self):
        return self.m_quantity
    
    def SetQuantity(self, p_quantity):
        self.m_quantity = p_quantity
        
    def LoadTemplate(self, p_template):
        self.m_templateid = p_template.GetId()
        self.m_name = p_template.GetName()
        self.m_description = p_template.GetDescription()
        self.m_isquantity = p_template.m_isquantity
        self.m_quantity = p_template.m_quantity
        self.m_attributes = Databank()
        for i in p_template.m_attributes.m_bank.keys():
            self.m_attributes.Add(i, p_template.m_attributes.m_bank[i])        
        
        for i in p_template.m_logics:
            self.AddLogic(i)
            
    def Load(self, sr, prefix):
        #self.Remove()
        
        self.m_name = sr.get(prefix + ":NAME")
        self.m_description = sr.get(prefix + ":DESCRIPTION")
        self.m_room = sr.get(prefix + ":ROOM")
        self.m_region = sr.get(prefix + ":REGION")
        self.m_isquantity = sr.get(prefix + ":ISQUANTITY")
        if self.m_isquantity == "False":
            self.m_isquantity = False
        else:
            self.m_isquantity = True
        self.m_quantity = int(sr.get(prefix + ":QUANTITY"))
        
        self.m_templateid = sr.get(prefix + ":TEMPLATEID")
        
        self.m_attributes.Load(sr, prefix)
        
        self.m_logic.Load(sr, prefix, self.m_id)
        
        #self.Add()
        
    def Save(self, sr, prefix):
        sr.set(prefix + ":NAME", self.m_name)
        sr.set(prefix + ":DESCRIPTION", self.m_description)
        sr.set(prefix + ":ROOM", self.m_room)
        sr.set(prefix + ":REGION", self.m_region)
        sr.set(prefix + ":ISQUANTITY", str(self.m_isquantity))
        sr.set(prefix + ":QUANTITY", str(self.m_quantity))
        sr.set(prefix + ":TEMPLATEID", self.m_templateid)
        
        self.m_attributes.Save(sr, prefix)
        
        self.m_logic.Save(sr, prefix)
        
    def Add(self, character, region, room):
        if self.m_region == "0":
            # when regions are 0, that means the item is on a Item.character
            c = character(self.m_room)
            c.AddItem(self.m_id)
        else:
            reg = region(self.m_region)
            reg.AddItem(self.m_id)
            
            r = room(self.m_room)
            r.AddItem(self.m_id)
            
    def Remove(self, character, region, room):
        if self.m_room == "0":
            return
        
        # when regions are 0, that means the item is on a Item.character
        if self.m_region == "0":
            c = character(self.m_room)
            c.DelItem(self.m_id)
        else:
            reg = region(self.m_region)
            reg.DelItem(self.m_id)
            
            r = room(self.m_room)
            r.DelItem(self.m_id)
