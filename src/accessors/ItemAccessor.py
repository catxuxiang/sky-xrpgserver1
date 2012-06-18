'''
Created on 2012-6-1

@author: Sky
'''
from Db.ItemDatabase import ItemDB
from Entities.Action import Action

class itemtemplate:
    def __init__(self, p_data):
        if type(p_data) == str:
            self.m_item = ItemDB.GetTemplate(p_data)
            self.m_item.AddRef()
        else:
            self.m_item.DelRef()
            self.m_item = p_data.m_item
            self.m_item.AddRef()
            
    def __del__(self):
        self.m_item.DelRef()
        
    def GetId(self):
        return self.m_item.GetId()
    
    def GetName(self):
        return self.m_item.GetName()
    
    def GetDescription(self):
        return self.m_item.GetDescription()
    
    def GetAttribute(self, p_name):
        return self.m_item.GetAttribute(p_name)
    
    def SetAttribute(self, p_name, p_val):
        self.m_item.SetAttribute(p_name, p_val)
        
    def HasAttribute(self, p_name):
        return self.m_item.HasAttribute(p_name)
    
    def AddAttribute(self, p_name, p_initialval):
        self.m_item.AddAttribute(p_name, p_initialval)
        
    def DelAttribute(self, p_name):
        self.m_item.DelAttribute(p_name)
        
    def IsQuantity(self):
        return self.m_item.IsQuantity()
    
    def GetQuantity(self):
        return self.m_item.GetQuantity()
    
class item:
    def __init__(self, p_data):
        if type(p_data) == str:
            self.m_item = ItemDB.Get(p_data)
            self.m_item.AddRef()
        else:
            self.m_item.DelRef()
            self.m_item = p_data.m_item
            self.m_item.AddRef()
            
    def __del__(self):
        self.m_item.DelRef()
        
    def GetId(self):
        return self.m_item.GetId()
    
    def GetName(self):
        return self.m_item.GetName()
    
    def GetDescription(self):
        return self.m_item.GetDescription()
    
    def SetId(self, p_id):
        self.m_item.SetId(p_id)
        
    def SetName(self, p_name):
        self.m_item.SetName(p_name)
        
    def SetDescription(self, p_desc):
        self.m_item.SetDescription(p_desc)
        
    def GetRoom(self):
        return self.m_item.GetRoom()
    
    def SetRoom(self, p_room):
        self.m_item.SetRoom(p_room)
        
    def GetRegion(self):
        return self.m_item.GetRegion()
    
    def SetRegion(self, p_region):
        self.m_item.SetRegion(p_region)
        
    def GetTemplateId(self):
        return self.m_item.GetTemplateId()
    
    def SetTemplateId(self, p_templateid):
        self.m_item.SetTemplateId(p_templateid)
        
    def AddLogic(self, p_logic):
        return self.m_item.AddLogic(p_logic)
    
    def AddExistingLogic(self, p_logic):
        return self.m_item.AddExistingLogic(p_logic)
    
    def DelLogic(self, p_logic):
        return self.m_item.DelLogic(p_logic)
    
    def GetLogic(self, p_logic):
        return self.m_item.GetLogic(p_logic)
    
    def HasLogic(self, p_logic):
        return self.m_item.HasLogic(p_logic)
    
    def DoAction(self, p_action, p_data1 = "0", p_data2 = "0", p_data3 = "0", p_data4 = "0", p_data = ""):
        if type(p_action) != str:
            return self.m_item.DoAction(p_action)
        else:
            return self.m_item.DoAction(Action(p_action, p_data1, p_data2, p_data3, p_data4, p_data))
        
    def GetLogicAttribute(self, p_logic, p_attr):
        return self.m_item.GetLogicAttribute(p_logic, p_attr)
    
    def AddHook(self, p_hook):
        self.m_item.AddHook(p_hook)
        
    def DelHook(self, p_hook):
        self.m_item.DelHook(p_hook)
        
    def Hooks(self):
        return self.m_item.Hooks()
    
    def KillHook(self, p_act, p_stringdata):
        self.m_item.KillHook(p_act, p_stringdata)
        
    def ClearHooks(self):
        self.m_item.ClearHooks()
        
    def ClearLogicHooks(self, p_logic):
        self.m_item.ClearLogicHooks(p_logic)
        
    def GetAttribute(self, p_name):
        return self.m_item.GetAttribute(p_name)
    
    def SetAttribute(self, p_name, p_val):
        self.m_item.SetAttribute(p_name, p_val)
        
    def HasAttribute(self, p_name):
        return self.m_item.HasAttribute(p_name)
    
    def AddAttribute(self, p_name, p_initialval):
        self.m_item.AddAttribute(p_name, p_initialval)
        
    def DelAttribute(self, p_name):
        self.m_item.DelAttribute(p_name)
        
    def IsQuantity(self):
        return self.m_item.IsQuantity()
    
    def GetQuantity(self):
        return self.m_item.GetQuantity()
    
    def SetQuantity(self, p_quantity):
        self.m_item.SetQuantity(p_quantity) 