'''
Created on 2012-6-9

@author: Sky
'''
from Db.CharacterDatabase import CharacterDB
from Db.ItemDatabase import ItemDB
from Db.RoomDatabase import RoomDB
from Db.PortalDatabase import PortalDB
from Db.AccountDatabase import AccountDB
from Db.RegionDatabase import RegionDB
from Entities.Game import g_game
class GameWrap:
    def FindPlayerOnlinePart(self, p_name):
        return g_game.FindPlayerOnlinePart(p_name)
    
    def FindPlayerOnlineFull(self, p_name):
        return g_game.FindPlayerOnlineFull(p_name)
    
    def FindPlayerPart(self, p_name):
        return g_game.FindPlayerPart(p_name)
    
    def FindPlayerFull(self, p_name):
        return g_game.FindPlayerFull(p_name)
    
    def HasPlayer(self, p_id):
        return g_game.HasPlayer(p_id)
    
    def GetRunning(self):
        return g_game.GetRunning()
    
    def ShutDown(self):
        g_game.ShutDown()
        
    def GetTime(self):
        return g_game.GetTime()
    
    def ResetTime(self):
        g_game.ResetTime()
        
    def DoAction(self, p_act, p_data1, p_data2, p_data3, p_data4, p_data):
        g_game.DoAction(p_act, p_data1, p_data2, p_data3, p_data4, p_data)
        
    def AddActionRelative(self, p_time, p_act, p_data1, p_data2, p_data3, p_data4, p_data):
        g_game.AddActionRelative(p_time, p_act, p_data1, p_data2, p_data3, p_data4, p_data)
        
    def AddActionAbsolute(self, p_time, p_act, p_data1, p_data2, p_data3, p_data4, p_data):
        g_game.AddActionAbsolute(p_time, p_act, p_data1, p_data2, p_data3, p_data4, p_data)
        
    def Characters(self):
        return CharacterDB.Size()
    
    def Items(self):
        return ItemDB.Size()
    
    def ItemTemplates(self):
        return ItemDB.SizeTemplates()
    
    def Rooms(self):
        return RoomDB.Size()
    
    def Regions(self):
        return RegionDB.Size()
    
    def Portals(self):
        return PortalDB.Size()
    
    def Accounts(self):
        return AccountDB.Size()
