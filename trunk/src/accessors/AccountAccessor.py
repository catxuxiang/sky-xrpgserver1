'''
Created on 2012-5-31

@author: Sky
'''
from Db.AccountDatabase import AccountDB
from Db.CharacterDatabase import CharacterDB

class account:
    def __init__(self, p_data):
        if type(p_data) == str:
            self.m_account = AccountDB.Get(p_data)
            self.m_account.AddRef()
        else:
            self.m_account.DelRef()
            self.m_account = p_data.m_account
            self.m_account.AddRef()
            
    def __del__(self):
        self.m_account.DelRef()
        
    def GetId(self):
        return self.m_account.GetId()
    
    def GetName(self):
        return self.m_account.GetName()
    
    def GetDescription(self):
        return self.m_account.GetDescription()
    
    def SetId(self, p_id):
        self.m_account.SetId(p_id)
        
    def SetName(self, p_name):
        self.m_account.SetName(p_name)
        
    def SetDescription(self, p_desc):
        self.m_account.SetDescription(p_desc)
        
    def AddCharacter(self, p_id):
        self.m_account.AddCharacter(p_id)
        
    def DelCharacter(self, p_id):
        self.m_account.DelCharacter(p_id)
        
    def Characters(self):
        return self.m_account.Characters()
    
    def BeginCharacter(self):
        self.m_characterIter = 0
        
    def CurrentCharacter(self):
        if self.m_characterIter < len(self.m_account.m_characters) and self.m_characterIter >= 0:
            return self.m_account.m_characters[self.m_characterIter]
        else:
            return None
        
    def NextCharacter(self):
        self.m_characterIter += 1
        
    def IsValidCharacter(self):      
        if self.m_characterIter < len(self.m_account.m_characters) and self.m_characterIter >= 0:
            return True
        else:
            return False
        
    def SeekCharacter(self, p_name):
        index = 0
        for i in self.m_account.m_characters:
            if CharacterDB.Get(i).GetName().lower() == p_name.lower().strip():
                self.m_characterIter = index
                return
            index += 1
        
        index = 0    
        for i in self.m_account.m_characters:
            if CharacterDB.Get(i).GetName().lower().find(p_name.lower().strip()) == 0:
                self.m_characterIter = index
                return
            index += 1    
            
        self.m_characterIter = -1  
    
    def GetPassword(self):
        return self.m_account.GetPassword()
    
    def LoginTime(self):
        return self.m_account.GetLoginTime()
    
    def GetAccessLevel(self):
        return self.m_account.GetAccessLevel()
    
    def GetBanned(self):
        return self.m_account.GetBanned()
    
    def AllowedCharacters(self):
        return self.m_account.AllowedCharacters()
    
    def SetPass(self, p_pass):
        self.m_account.SetPass(p_pass)
        
    def SetLoginTime(self, p_time):
        self.m_account.SetLoginTime(p_time)
        
    def SetAccessLevel(self, p_level):
        self.m_account.SetAccessLevel(p_level)
        
    def SetBanned(self, p_banned):
        self.m_account.SetBanned(p_banned)
        
    def SetAllowedCharacters(self, p_num):
        self.m_account.SetAllowedCharacters(p_num)
