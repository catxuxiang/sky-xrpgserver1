'''
Created on 2012-5-30

@author: Sky
'''
from Entities.Entity import Entity
from Entities.Action import Action
from Scripts.LogicCollection import LogicCollection
from BasicLib.BasicLibString import ParseWord

class LogicEntity(Entity):
    def __init__(self):
        Entity.__init__(self)
        
        self.m_logic = LogicCollection()
        self.m_hooks = []
        
    def AddLogic(self, p_logic):
        try:
            self.m_logic.Add(p_logic, self.m_id)
            return True
        except Exception:
            return False
    
    def AddExistingLogic(self, p_logic):
        try:
            self.m_logic.AddExisting(p_logic)
            return True
        except Exception:
            return False

    def DelLogic(self, p_logic):
        try:
            self.ClearLogicHooks(p_logic)
            
            self.m_logic.Del(p_logic)
            return True
        except Exception:
            return False
    
    def GetLogic(self, p_logic):
        return self.m_logic.Get(p_logic)
    
    def HasLogic(self, p_logic):
        try:
            return self.m_logic.Has(p_logic)
        except Exception:
            return False
    
    def DoAction(self, p_action, p_data1 = "0", p_data2 = "0", p_data3 = "0", p_data4 = "0", p_data = ""):
        if type(p_action) != str:
            return self.m_logic.DoAction(p_action)
        else:
            return self.m_logic.DoAction(Action(p_action, p_data1, p_data2, p_data3, p_data4, p_data))
        
    def GetLogicAttribute(self, p_logic, p_attr):
        return self.m_logic.GetAttribute(p_logic, p_attr)
    
    def AddHook(self, p_hook):
        self.m_hooks.append(p_hook)
        
    def DelHook(self, p_hook):
        i = 0 
        for hook in self.m_hooks:
            if hook == p_hook:
                break
            i += 1
        if i < len(self.m_hooks):
            del self.m_hooks[i]
            
    def Hooks(self):
        return len(self.m_hooks)
    
    def KillHook(self, p_act, p_stringdata):
        for i in self.m_hooks:
            # unhook the event if it matches the parameters
            if i.actionevent.actiontype == p_act and ParseWord(i.actionevent.stringdata, 0) == p_stringdata:
                i.Unhook()
                
    def ClearHooks(self):
        for i in self.m_hooks:
            i.Unhook()
            
    def ClearLogicHooks(self, p_logic):
        for i in self.m_hooks:
            if i.actionevent.actiontype == "messagelogic" or i.actionevent.actiontype == "dellogic":
                if ParseWord(i.actionevent.stringdata, 0) == p_logic:
                    i.Unhook()

