'''
Created on 2012-5-30

@author: Sky
'''
from Db.Databases import TemplateInstanceDatabase
from Entities.Character import Character, CharacterTemplate

class CharacterDatabase(TemplateInstanceDatabase):
    def SavePlayers(self):
        sr = TemplateInstanceDatabase.Sr
        sr.ltrim("players", 2, 1)
        for i in self.m_instances.m_container.values():
            if i.IsPlayer():
                sr.rpush("players", i.GetId())
                self.SaveEntity(i, "players:" + i.GetId())
                
    def LoadPlayer(self, p_id):
        p = Character()
        p.SetId(p_id)
        self.LoadEntity(p, "players:" + p_id) 
        
    def LoadPlayers(self):
        sr = TemplateInstanceDatabase.Sr
        for i in range(sr.llen("players")):
            id1 = sr.lindex("players", i)
            self.LoadPlayer(id1)
            
    def LoadTemplates(self, p_key = ""):
        sr = TemplateInstanceDatabase.Sr
        folder = "templates:characters"
        if p_key == "":
            for i in range(sr.llen(folder)):
                key = sr.lindex(folder, i)
                subfolder = folder + ":" + key
                for j in range(sr.llen(subfolder)):
                    id1 = sr.lindex(subfolder, j)
                    ct = CharacterTemplate()
                    ct.SetId(id1)
                    self.LoadEntityTemplate(ct, subfolder + ":" + id1)
        else:
            subfolder = folder + ":" + p_key
            for j in sr.llen(subfolder):
                id1 = sr.lindex(subfolder, j)
                ct = CharacterTemplate()
                ct.SetId(id1)
                self.LoadEntityTemplate(ct, subfolder + ":" + id1)
                
    def FindPlayerFull(self, p_name):
        for i in self.m_instances.m_container.values():
            if i.GetName().lower() == p_name.lower().strip():
                return i.GetId()
        return None
    
    def FindPlayerPart(self, p_name):
        player = self.FindPlayerFull(p_name)
        if player != "0":
            return player
        
        for i in self.m_instances.m_container.values():
            if i.GetName().lower().find(p_name.lower().strip()) == 0:
                return i.GetId()
        return None

    def SaveDb(self, folder, m_characters):
        sr = TemplateInstanceDatabase.Sr
        sr.ltrim(folder, 2, 1)
        for id1 in m_characters:
            i = self.Get(id1)
            sr.rpush(folder, id1)
            self.SaveEntity(i, folder + ":" + id1) 
            
    def LoadDb(self, folder):
        sr = TemplateInstanceDatabase.Sr
        characters = []
        for i in range(0, sr.llen(folder)):
            id1 = sr.lindex(folder, i)
            data = Character()
            data.SetId(id1)
            self.LoadEntity(data, folder + ":" + id1)
            characters.append(id1)
        return characters  
    
CharacterDB = CharacterDatabase()
    
     
