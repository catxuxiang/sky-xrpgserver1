'''
Created on 2012-5-30

@author: Sky
'''
from Entities.Entity import Entity, HasCharacters
from Entities.Attributes import accesslevel_Peon
class Account(Entity, HasCharacters):
    def __init__(self):
        Entity.__init__(self)
        HasCharacters.__init__(self)
        self.m_password = "UNDEFINED"
        self.m_logintime = 0
        self.m_accesslevel = accesslevel_Peon
        self.m_allowedcharacters = 2
        self.m_banned = False
        
    def GetPassword(self):
        return self.m_password
    
    def GetLoginTime(self):
        return self.m_logintime
    
    def GetAccessLevel(self):
        return self.m_accesslevel
    
    def GetBanned(self):
        return self.m_banned
    
    def GetAllowedCharacters(self):
        return self.m_allowedcharacters
    
    def SetPass(self, p_pass):
        self.m_password = p_pass
        
    def SetLoginTime(self, p_time):
        self.m_logintime = p_time
        
    def SetAccessLevel(self, p_level):
        self.m_accesslevel = p_level
        
    def SetBanned(self, p_banned):
        self.m_banned = p_banned
        
    def SetAllowedCharacters(self, p_num):
        self.m_allowedcharacters = p_num
        
    def Load(self, sr, prefix):
        self.m_name = sr.get(prefix + ":NAME")
        self.m_password = sr.get(prefix + ":PASS")
        self.m_logintime = int(sr.get(prefix + ":FIRSTLOGINTIME"))
        self.m_accesslevel = int(sr.get(prefix + ":ACCESSLEVEL"))
        self.m_allowedcharacters = int(sr.get(prefix + ":ALLOWEDCHARS"))
        self.m_banned = sr.get(prefix + ":BANNED")
        if (self.m_banned == "False"):
            self.m_banned = False
        else:
            self.m_banned = True
            
        characters = sr.get(prefix + ":CHARACTERS").split(" ")
        self.m_characters = []
        for i in characters:
            if i != "0":
                self.m_characters.append(i)
                
    def Save(self, sr, prefix):
        sr.set(prefix + ":NAME", self.m_name)
        sr.set(prefix + ":PASS", self.m_password)
        sr.set(prefix + ":FIRSTLOGINTIME", str(self.m_logintime))
        sr.set(prefix + ":ACCESSLEVEL", str(self.m_accesslevel))
        sr.set(prefix + ":ALLOWEDCHARS", str(self.m_allowedcharacters))
        sr.set(prefix + ":BANNED", str(self.m_banned))
        
        string = ""
        for i in self.m_characters:
            string += i + " "
        string += "0"
        sr.set(prefix + ":CHARACTERS", string)



