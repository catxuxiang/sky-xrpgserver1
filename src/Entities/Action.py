'''
Created on 2012-5-30

@author: Sky
'''
ENTITYTYPE_CHARACTER = 0
ENTITYTYPE_ITEM = 1
ENTITYTYPE_ROOM = 2
ENTITYTYPE_PORTAL = 3
ENTITYTYPE_REGION = 4

class Action:
    def __init__(self, p_action, p_data1 = "0", p_data2 = "0", p_data3 = "0", p_data4 = "0", p_data = ""):
        self.actiontype = p_action
        self.data1 = p_data1
        self.data2 = p_data2
        self.data3 = p_data3
        self.data4 = p_data4
        self.stringdata = p_data
        
class TimedAction:
    character = None
    item = None
    room = None
    portal = None
    region = None  
    def __init__(self, time = 0, act = "", p_data1 = "0", p_data2 = "0", p_data3 = "0", p_data4 = "0", p_data = ""):
        self.valid = True
        self.executiontime = time
        if type(act) != str:
            self.actionevent = act
        else:
            if act != "":
                self.actionevent = Action(act, p_data1, p_data2, p_data3, p_data4, p_data)
        
    def Hook(self):
        if self.actionevent.actiontype == "attemptsay" or self.actionevent.actiontype == "command" or self.actionevent.actiontype == "attemptenterportal" or self.actionevent.actiontype == "attempttransport" or self.actionevent.actiontype == "transport" or self.actionevent.actiontype == "destroycharacter":
            TimedAction.character(self.actionevent.data1).AddHook(self)
        elif self.actionevent.actiontype == "attemptgetitem" or self.actionevent.actiontype == "attemptdropitem":
            TimedAction.character(self.actionevent.data1).AddHook(self)
            TimedAction.item(self.actionevent.data2).AddHook(self)
        elif self.actionevent.actiontype == "attemptgiveitem":
            TimedAction.character(self.actionevent.data1).AddHook(self)
            TimedAction.character(self.actionevent.data2).AddHook(self)
            TimedAction.item(self.actionevent.data3).AddHook(self)
        elif self.actionevent.actiontype == "destroyitem":
            TimedAction.item(self.actionevent.data1).AddHook(self)
        elif self.actionevent.actiontype == "messagelogic" or self.actionevent.actiontype == "dellogic" or self.actionevent.actiontype == "do" or self.actionevent.actiontype == "modifyattribute":
            if self.actionevent.data1 == str(ENTITYTYPE_CHARACTER):
                TimedAction.character(self.actionevent.data2).AddHook(self)
            elif self.actionevent.data1 == str(ENTITYTYPE_ITEM):
                TimedAction.item(self.actionevent.data2).AddHook(self)
            elif self.actionevent.data1 == str(ENTITYTYPE_ROOM):
                TimedAction.room(self.actionevent.data2).AddHook(self)
            elif self.actionevent.data1 == str(ENTITYTYPE_PORTAL):
                TimedAction.portal(self.actionevent.data2).AddHook(self)
            elif self.actionevent.data1 == str(ENTITYTYPE_REGION):
                TimedAction.region(self.actionevent.data2).AddHook(self)
                
    def Unhook(self):
        self.valid = False
        if self.actionevent.actiontype == "attemptsay" or \
        self.actionevent.actiontype == "command" or \
        self.actionevent.actiontype == "attemptenterportal" or \
        self.actionevent.actiontype == "attempttransport" or \
        self.actionevent.actiontype == "transport" or \
        self.actionevent.actiontype == "destroycharacter":
            TimedAction.character(self.actionevent.data1).DelHook(self)
        elif self.actionevent.actiontype == "attemptgetitem" or self.actionevent.actiontype == "attemptdropitem":
            TimedAction.character(self.actionevent.data1).DelHook(self)
            TimedAction.item(self.actionevent.data2).DelHook(self)
        elif self.actionevent.actiontype == "attemptgiveitem":
            TimedAction.character(self.actionevent.data1).DelHook(self)
            TimedAction.character(self.actionevent.data2).DelHook(self)
            TimedAction.item(self.actionevent.data3).DelHook(self)
        elif self.actionevent.actiontype == "destroyitem":
            TimedAction.item(self.actionevent.data1).DelHook(self)
        elif self.actionevent.actiontype == "messagelogic" or self.actionevent.actiontype == "dellogic" or self.actionevent.actiontype == "do" or self.actionevent.actiontype == "modifyattribute":
            if self.actionevent.data1 == str(ENTITYTYPE_CHARACTER):
                TimedAction.character(self.actionevent.data2).DelHook(self)
            elif self.actionevent.data1 == str(ENTITYTYPE_ITEM):
                TimedAction.item(self.actionevent.data2).DelHook(self)
            elif self.actionevent.data1 == str(ENTITYTYPE_ROOM):
                TimedAction.room(self.actionevent.data2).DelHook(self)
            elif self.actionevent.data1 == str(ENTITYTYPE_PORTAL):
                TimedAction.portal(self.actionevent.data2).DelHook(self)
            elif self.actionevent.data1 == str(ENTITYTYPE_REGION):
                TimedAction.region(self.actionevent.data2).DelHook(self)
                
    def Save(self, sr, prefix):
        if not self.valid:
            return
        
        sr.set(prefix + ":TIMER:TIME", str(self.executiontime))
        sr.set(prefix + ":TIMER:NAME", self.actionevent.actiontype)
        sr.set(prefix + ":TIMER:DATA1", self.actionevent.data1)
        sr.set(prefix + ":TIMER:DATA2", self.actionevent.data2)
        sr.set(prefix + ":TIMER:DATA3", self.actionevent.data3)
        sr.set(prefix + ":TIMER:DATA4", self.actionevent.data4)
        
        if self.actionevent.stringdata == "":
            self.actionevent.stringdata = "0"
        sr.set(prefix + ":TIMER:STRING", self.actionevent.stringdata)
        
    def Load(self, sr, prefix):
        self.executiontime = int(sr.get(prefix + ":TIMER:TIME"))
        self.actionevent.actiontype = sr.get(prefix + ":TIMER:NAME")
        self.actionevent.data1 = sr.get(prefix + ":TIMER:DATA1")
        self.actionevent.data2 = sr.get(prefix + ":TIMER:DATA2")
        self.actionevent.data3 = sr.get(prefix + ":TIMER:DATA3")
        self.actionevent.data4 = sr.get(prefix + ":TIMER:DATA4")
        self.actionevent.stringdata = sr.get(prefix + ":TIMER:STRING")
