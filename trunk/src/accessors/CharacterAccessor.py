'''
Created on 2012-5-30

@author: Sky
'''
from Db.CharacterDatabase import CharacterDB
from Entities.Action import Action
from Db.ItemDatabase import ItemDB

class charactertemplate:
    def __init__(self, p_data):
        if type(p_data) == str:
            self.m_character = CharacterDB.GetTemplate(p_data)
            self.m_character.AddRef()
        else:
            self.m_character.DelRef()
            self.m_character = p_data.m_character
            self.m_character.AddRef()
            
    def __del__(self):
        self.m_character.DelRef()
        
    def GetId(self):
        return self.m_character.GetId()
    
    def GetName(self):
        return self.m_character.GetName()
    
    def GetDescription(self):
        return self.m_character.GetDescription()
    
    def GetAttribute(self, p_name):
        return self.m_character.GetAttribute(p_name)
    
    def SetAttribute(self, p_name, p_val):
        self.m_character.SetAttribute(p_name, p_val)
        
    def HasAttribute(self, p_name):
        return self.m_character.HasAttribute(p_name)
    
    def AddAttribute(self, p_name, p_initialval):
        self.m_character.AddAttribute(p_name, p_initialval)
        
    def DelAttribute(self, p_name):
        self.m_character.DelAttribute(p_name)    
    
class character:
    def __init__(self, p_data):
        if type(p_data) == str:
            self.m_character = CharacterDB.Get(p_data)
            self.m_character.AddRef()
        else:
            self.m_character.DelRef()
            self.m_character = p_data.m_character
            self.m_character.AddRef()
            
    #def __del__(self):
    #    self.m_character.DelRef()
        
    def GetId(self):
        return self.m_character.GetId()
    
    def GetName(self):
        return self.m_character.GetName()
    
    def GetDescription(self):
        return self.m_character.GetDescription()
    
    def SetId(self, p_id):
        self.m_character.SetId(p_id)
        
    def SetName(self, p_name):
        self.m_character.SetName(p_name)
        
    def SetDescription(self, p_desc):
        self.m_character.SetDescription(p_desc)
        
    def GetRoom(self):
        return self.m_character.GetRoom()
    
    def SetRoom(self, p_room):
        self.m_character.SetRoom(p_room)
        
    def GetRegion(self):
        return self.m_character.GetRegion()
    
    def SetRegion(self, p_region):
        self.m_character.SetRegion(p_region)
        
    def GetTemplateId(self):
        return self.m_character.GetTemplateId()
    
    def SetTemplateId(self, p_templateid):
        self.m_character.SetTemplateId(p_templateid)
        
    def AddItem(self, p_id):
        self.m_character.AddItem(p_id)
        
    def DelItem(self, p_id):
        self.m_character.DelItem(p_id)
        
    def Items(self):
        return self.m_character.m_items

    def BeginItem(self):
        self.m_itemIter = 0
        
    def CurrentItem(self):
        if self.m_itemIter < len(self.m_character.m_items) and self.m_itemIter >= 0:
            return self.m_character.m_items[self.m_itemIter]
        else:
            return None
        
    def NextItem(self):
        self.m_itemIter += 1
        
    def IsValidItem(self):      
        if self.m_itemIter < len(self.m_character.m_items) and self.m_itemIter >= 0:
            return True
        else:
            return False
        
    def SeekItem(self, p_name):
        index = 0
        for i in self.m_character.m_items:
            if ItemDB.Get(i).GetName().lower() == p_name.lower().strip():
                self.m_itemIter = index
                return
            index += 1
        
        index = 0    
        for i in self.m_character.m_items:
            if ItemDB.Get(i).GetName().lower().find(p_name.lower().strip()) != -1:
                self.m_itemIter = index
                return    
            index += 1
            
        self.m_itemIter = -1  
    
    def AddLogic(self, p_logic):
        return self.m_character.AddLogic(p_logic)
    
    def AddExistingLogic(self, p_logic):
        return self.m_character.AddExistingLogic(p_logic)
    
    def DelLogic(self, p_logic):
        return self.m_character.DelLogic(p_logic)
    
    def GetLogic(self, p_logic):
        return self.m_character.GetLogic(p_logic)
    
    def HasLogic(self, p_logic):
        return self.m_character.HasLogic(p_logic)
    
    def DoAction(self, p_act, p_data1 = "0", p_data2 = "0", p_data3 = "0", p_data4 = "0", p_data = ""):
        if type(p_act) != str:
            return self.m_character.DoAction(p_act)
        else:
            return self.m_character.DoAction(Action(p_act, p_data1, p_data2, p_data3, p_data4, p_data))
        
    def GetLogicAttribute(self, p_logic, p_attr):
        return self.m_character.GetLogicAttribute(p_logic, p_attr)
    
    def AddHook(self, p_hook):
        self.m_character.AddHook(p_hook)
        
    def DelHook(self, p_hook):
        self.m_character.DelHook(p_hook)
        
    def GetHooks(self):
        return self.m_character.m_hooks
    
    def KillHook(self, p_act, p_stringdata):
        self.m_character.KillHook(p_act, p_stringdata)
        
    def ClearHooks(self):
        self.m_character.ClearHooks()
        
    def ClearLogicHooks(self, p_logic):
        self.m_character.ClearLogicHooks(p_logic)
        
    def GetAttribute(self, p_name):
        return self.m_character.GetAttribute(p_name)
    
    def SetAttribute(self, p_name, p_val):
        self.m_character.SetAttribute(p_name, p_val)
        
    def HasAttribute(self, p_name):
        return self.m_character.HasAttribute(p_name)
    
    def AddAttribute(self, p_name, p_initialval):
        self.m_character.AddAttribute(p_name, p_initialval)
        
    def DelAttribute(self, p_name):
        self.m_character.DelAttribute(p_name)
        
    def AddCommand(self, p_command):
        return self.m_character.AddCommand(p_command)
    
    def DelCommand(self, p_command):
        return self.m_character.DelCommand(p_command)
    
    def HasCommand(self, p_command):
        return self.m_character.HasCommand(p_command)
    
    def SeekCommand(self, p_name):
        return self.m_character.FindCommand(p_name)
    
    def GetQuiet(self):
        return self.m_character.GetQuiet()
    
    def IsPlayer(self):
        return self.m_character.IsPlayer()
    
    def Verbose(self):
        return self.m_character.GetVerbose()
    
    def GetAccount(self):
        return self.m_character.GetAccount()
    
    def SetQuiet(self, p_quiet):
        self.m_character.SetQuiet(p_quiet)
        
    def SetAccount(self, p_account):
        self.m_character.SetAccount(p_account)
        
    def IsLoggedIn(self):
        return self.m_character.IsLoggedIn()
    
    def SetLoggedIn(self, p_loggedin):
        self.m_character.SetLoggedIn(p_loggedin)
        
    def LastCommand(self):
        return self.m_character.LastCommand()
    
