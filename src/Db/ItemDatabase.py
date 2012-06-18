'''
Created on 2012-5-31

@author: Sky
'''
from Entities.Item import ItemTemplate, Item
from Db.Databases import TemplateInstanceDatabase
class ItemDatabase(TemplateInstanceDatabase):
    def LoadTemplates(self, p_key = ""):
        sr = TemplateInstanceDatabase.Sr
        folder = "templates:items"
        if p_key == "":
            for i in range(sr.llen(folder)):
                key = sr.lindex(folder, i)
                subfolder = folder + ":" + key
                for j in range(sr.llen(subfolder)):
                    id1 = sr.lindex(subfolder, j)
                    data = ItemTemplate()
                    data.SetId(id1)
                    self.LoadEntityTemplate(data, subfolder + ":" + id1)
        else:
            subfolder = folder + ":" + p_key
            for j in sr.llen(subfolder):
                id1 = sr.lindex(subfolder, j)
                data = ItemTemplate()
                data.SetId(id1)
                self.LoadEntityTemplate(data, subfolder + ":" + id1)  

    def SaveDb(self, folder, m_items):
        sr = TemplateInstanceDatabase.Sr
        sr.ltrim(folder, 2, 1)
        for id1 in m_items:
            i = self.Get(id1)
            sr.rpush(folder, id1)
            self.SaveEntity(i, folder + ":" + id1) 
            
    def LoadDb(self, folder):
        sr = TemplateInstanceDatabase.Sr
        items = []
        for i in range(0, sr.llen(folder)):
            id1 = sr.lindex(folder, i)
            data = Item()
            data.SetId(id1)
            self.LoadEntity(data, folder + ":" + id1)
            items.append(id1)
        return items  
    
ItemDB = ItemDatabase()
