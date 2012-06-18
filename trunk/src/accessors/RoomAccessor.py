'''
Created on 2012-6-1

@author: Sky
'''
from Db.RoomDatabase import RoomDB
from Entities.Action import Action
from Db.ItemDatabase import ItemDB
from Db.CharacterDatabase import CharacterDB
from Db.PortalDatabase import PortalDB

class room:
    def __init__(self, p_data):
        if type(p_data) == str:
            self.m_room = RoomDB.Get(p_data)
            self.m_room.AddRef()
        else:
            self.m_room.DelRef()
            self.m_room = p_data.m_room
            self.m_room.AddRef()
            
    def __del__(self):
        self.m_room.DelRef()
        
    def GetId(self):
        return self.m_room.GetId()
    
    def GetName(self):
        return self.m_room.GetName()
    
    def GetDescription(self):
        return self.m_room.GetDescription()
    
    def SetId(self, p_id):
        self.m_room.SetId(p_id)
        
    def SetName(self, p_name):
        self.m_room.SetName(p_name)
        
    def SetDescription(self, p_desc):
        self.m_room.SetDescription(p_desc)
        
    def GetRegion(self):
        return self.m_room.GetRegion()
    
    def SetRegion(self, p_region):
        self.m_room.SetRegion(p_region)
        
    def AddItem(self, p_id):
        self.m_room.AddItem(p_id)
        
    def DelItem(self, p_id):
        self.m_room.DelItem(p_id)
        
    def Items(self):
        return self.m_room.Items()
    
    def BeginItem(self):
        self.m_itemIter = 0
        
    def CurrentItem(self):
        if self.m_itemIter < len(self.m_room.m_items) and self.m_itemIter >= 0:
            return self.m_room.m_items[self.m_itemIter]
        else:
            return None
        
    def NextItem(self):
        self.m_itemIter += 1
        
    def IsValidItem(self):      
        if self.m_itemIter < len(self.m_room.m_items) and self.m_itemIter >= 0:
            return True
        else:
            return False
        
    def SeekItem(self, p_name):
        index = 0
        for i in self.m_room.m_items:
            if ItemDB.Get(i).GetName().lower() == p_name.lower().strip():
                self.m_itemIter = index
                return
            index += 1
            
        index = 0    
        for i in self.m_room.m_items:
            if ItemDB.Get(i).GetName().lower().find(p_name.lower().strip()) != -1:
                self.m_itemIter = index
                return
            index += 1    
            
        self.m_itemIter = -1  
    
    def AddCharacter(self, p_id):
        self.m_room.AddCharacter(p_id)
        
    def DelCharacter(self, p_id):
        self.m_room.DelCharacter(p_id)
        
    def Characters(self):
        return self.m_room.Characters()
    
    def BeginCharacter(self):
        self.m_characterIter = 0
        
    def CurrentCharacter(self):
        if self.m_characterIter < len(self.m_room.m_characters) and self.m_characterIter >= 0:
            return self.m_room.m_characters[self.m_characterIter]
        else:
            return None
        
    def NextCharacter(self):
        self.m_characterIter += 1
        
    def IsValidCharacter(self):      
        if self.m_characterIter < len(self.m_room.m_characters) and self.m_characterIter >= 0:
            return True
        else:
            return False
        
    def SeekCharacter(self, p_name):
        index = 0
        for i in self.m_room.m_characters:
            if CharacterDB.Get(i).GetName().lower() == p_name.lower().strip():
                self.m_characterIter = index
                return
            index += 1
        
        index = 0    
        for i in self.m_room.m_characters:
            if CharacterDB.Get(i).GetName().lower().find(p_name.lower().strip()) == 0:
                self.m_characterIter = index
                return    
            index += 1
            
        self.m_characterIter = -1  
    
    def AddPortal(self, p_id):
        self.m_room.AddPortal(p_id)
        
    def DelPortal(self, p_id):
        self.m_room.DelPortal(p_id)
        
    def Portals(self):
        return self.m_room.Portals()
    
    def BeginPortal(self):
        self.m_portalIter = 0
        
    def CurrentPortal(self):
        if self.m_portalIter < len(self.m_room.m_portals) and self.m_portalIter >= 0:
            return self.m_room.m_portals[self.m_portalIter]
        else:
            return None
        
    def NextPortal(self):
        self.m_portalIter += 1
        
    def IsValidPortal(self):      
        if self.m_portalIter < len(self.m_room.m_portals) and self.m_portalIter >= 0:
            return True
        else:
            return False
        
    def SeekPortal(self, p_name):
        index = 0
        for i in self.m_room.m_portals:
            for j in PortalDB.Get(i).m_portals:
                if j.directionname.lower() == p_name.lower().strip():
                    self.m_portalIter = index
                return
            index += 1
        
        index = 0    
        for i in self.m_room.m_portals:
            for j in PortalDB.Get(i).m_portals:
                if j.directionname.lower().find(p_name.lower().strip()) == 0:
                    self.m_portalIter = index
                return    
            index += 1
            
        self.m_portalIter = -1 
    
    def AddLogic(self, p_logic):
        return self.m_room.AddLogic(p_logic)
    
    def AddExistingLogic(self, p_logic):
        return self.m_room.AddExistingLogic(p_logic)
    
    def DelLogic(self, p_logic):
        return self.m_room.DelLogic(p_logic)
    
    def GetLogic(self, p_logic):
        return self.m_room.GetLogic(p_logic)
    
    def HasLogic(self, p_logic):
        return self.m_room.HasLogic(p_logic)
    
    def DoAction(self, p_action, p_data1 = "0", p_data2 = "0", p_data3 = "0", p_data4 = "0", p_data = ""):
        if type(p_action) != str:
            return self.m_room.DoAction(p_action)
        else:
            return self.m_room.DoAction(Action(p_action, p_data1, p_data2, p_data3, p_data4, p_data))
        
    def GetLogicAttribute(self, p_logic, p_attr):
        return self.m_room.GetLogicAttribute(p_logic, p_attr)
    
    def AddHook(self, p_hook):
        self.m_room.AddHook(p_hook)
        
    def DelHook(self, p_hook):
        self.m_room.DelHook(p_hook)
        
    def Hooks(self):
        return self.m_room.Hooks()
    
    def KillHook(self, p_act, p_stringdata):
        self.m_room.KillHook(p_act, p_stringdata)
        
    def ClearHooks(self):
        self.m_room.ClearHooks()
        
    def ClearLogicHooks(self, p_logic):
        self.m_room.ClearLogicHooks(p_logic)
        
    def GetAttribute(self, p_name):
        return self.m_room.GetAttribute(p_name)
    
    def SetAttribute(self, p_name, p_val):
        self.m_room.SetAttribute(p_name, p_val)
        
    def HasAttribute(self, p_name):
        return self.m_room.HasAttribute(p_name)
    
    def AddAttribute(self, p_name, p_initialval):
        self.m_room.AddAttribute(p_name, p_initialval)
        
    def DelAttribute(self, p_name):
        self.m_room.DelAttribute(p_name)