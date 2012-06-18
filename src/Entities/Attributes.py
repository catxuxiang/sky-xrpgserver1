'''
Created on 2012-5-29

@author: Sky
'''
accesslevel_Peon = 0
accesslevel_Builder = 1
accesslevel_God = 2
accesslevel_Admin = 3

ACCESSLEVELSTRINGS = []
ACCESSLEVELSTRINGS.append("Peon")
ACCESSLEVELSTRINGS.append("Builder")
ACCESSLEVELSTRINGS.append("God")
ACCESSLEVELSTRINGS.append("Admin")

AccessLevels = 4

class Databank:
    def __init__(self):
        self.m_bank = {}
        
    def __iter__(self):
        for i in self.m_bank.keys():
            yield i
            
    def __getitem__(self, index):
        return self.m_bank[index]        
        
    def Has(self, p_name):
        for i in self.m_bank:
            if i == p_name:
                return True
        return False
    
    def Set(self, p_name, p_val):
        for i in self.m_bank:
            if i == p_name:
                self.m_bank[p_name] = p_val
                return
        raise Exception("INVALID DATABANK ATTRIBUTE: " + p_name)
    
    def Get(self, p_name):
        for i in self.m_bank:
            if i == p_name:
                return self.m_bank[p_name]
        raise Exception("INVALID DATABANK ATTRIBUTE: " + p_name)
    
    def Add(self, p_name, p_val):
        self.m_bank[p_name] = p_val
        
    def Del(self, p_name):
        isexist = False
        for i in self.m_bank:
            if i == p_name:
                isexist = True
                break
        if isexist:
            del self.m_bank[p_name]
            
    def Save(self, sr, prefix):
        key = prefix + ":DATABANK"
        for i in sr.hkeys(key):
            sr.hdel(key, i)
        for i in self.m_bank:
            sr.hset(key, i, self.m_bank[i])
            
    def Load(self, sr, prefix):
        key = prefix + ":DATABANK"
        self.m_bank = {}
        for i in sr.hkeys(key):
            self.m_bank[i] = sr.hget(key, i)
            
    def Clear(self):
        self.m_bank = {}

    def Size(self):
        return len(self.m_bank)
    
        