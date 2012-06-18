'''
Created on 2012-5-31

@author: Sky
'''
from Db.Databases import MapDatabase
from BasicLib.Redis import sr
from Entities.Room import Room

class RoomDatabase(MapDatabase):
    def SaveDb(self, folder, p_rooms):
        sr.ltrim(folder, 2, 1)
        for id1 in p_rooms:
            i = self.Get(id1)
            sr.rpush(folder, id1)
            self.SaveEntity(i, folder + ":" + id1)
            
    def LoadDb(self, folder):
        rooms = []
        for i in range(0, sr.llen(folder)):
            id1 = sr.lindex(folder, i)
            data = Room()
            data.SetId(id1)
            self.LoadEntity(data, folder + ":" + id1)
            rooms.append(id1)
        return rooms

RoomDB = RoomDatabase()
