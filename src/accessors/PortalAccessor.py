'''
Created on 2012-6-1

@author: Sky
'''
from Db.PortalDatabase import PortalDB
from Entities.Action import Action

class portal:
    def __init__(self, p_data):
        if type(p_data) == str:
            self.m_portal = PortalDB.Get(p_data)
            self.m_portal.AddRef()
        else:
            self.m_portal.DelRef()
            self.m_portal = p_data.m_portal
            self.m_portal.AddRef()
            
    def __del__(self):
        self.m_portal.DelRef()
        
    def GetId(self):
        return self.m_portal.GetId()
    
    def GetName(self):
        return self.m_portal.GetName()
    
    def GetDescription(self):
        return self.m_portal.GetDescription()
    
    def SetId(self, p_id):
        self.m_portal.SetId(p_id)
        
    def SetName(self, p_name):
        self.m_portal.SetName(p_name)
        
    def SetDescription(self, p_desc):
        self.m_portal.SetDescription(p_desc)
        
    def GetRegion(self):
        return self.m_portal.GetRegion()
    
    def SetRegion(self, p_region):
        self.m_portal.SetRegion(p_region)
        
    def GetAttribute(self, p_name):
        return self.m_portal.GetAttribute(p_name)
    
    def SetAttribute(self, p_name, p_val):
        self.m_portal.SetAttribute(p_name, p_val)
        
    def HasAttribute(self, p_name):
        return self.m_portal.HasAttribute(p_name)
    
    def AddAttribute(self, p_name, p_initialval):
        self.m_portal.AddAttribute(p_name, p_initialval)
        
    def DelAttribute(self, p_name):
        self.m_portal.DelAttribute(p_name)
        
    def AddLogic(self, p_logic):
        return self.m_portal.AddLogic(p_logic)
    
    def AddExistingLogic(self, p_logic):
        return self.m_portal.AddExistingLogic(p_logic)
    
    def DelLogic(self, p_logic):
        return self.m_portal.DelLogic(p_logic)
    
    def GetLogic(self, p_logic):
        return self.m_portal.GetLogic(p_logic)
    
    def HasLogic(self, p_logic):
        return self.m_portal.HasLogic(p_logic)
    
    def DoAction(self, p_action, p_data1 = "0", p_data2 = "0", p_data3 = "0", p_data4 = "0", p_data = ""):
        if type(p_action) != str:
            return self.m_portal.DoAction(p_action)
        else:
            return self.m_portal.DoAction(Action(p_action, p_data1, p_data2, p_data3, p_data4, p_data))
        
    def GetLogicAttribute(self, p_logic, p_attr):
        return self.m_portal.GetLogicAttribute(p_logic, p_attr)
    
    def AddHook(self, p_hook):
        self.m_portal.AddHook(p_hook)
        
    def DelHook(self, p_hook):
        self.m_portal.DelHook(p_hook)
        
    def Hooks(self):
        return self.m_portal.Hooks()
    
    def KillHook(self, p_act, p_stringdata):
        self.m_portal.KillHook(p_act, p_stringdata)
        
    def ClearHooks(self):
        self.m_portal.ClearHooks()
        
    def ClearLogicHooks(self, p_logic):
        self.m_portal.ClearLogicHooks(p_logic)
'''        
    def SeekStartRoom(self, p_room):
        for i in self.m_portal.m_portals:
            if i.startroom == p_room:
                return i
        return None
    
    def SeekEndRoom(self, p_room):
        for id1 in self.m_portal.m_portals:
            i = PortalDB.Get(id1)
            if i.destinationroom == p_room:
                return i
        return None
'''

        
    
