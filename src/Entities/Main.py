'''
Created on 2012-6-5

@author: Sky
'''
from SocketLib.ListeningManager import ListeningManager
from SocketLib.ConnectionManager import ConnectionManager
from Entities.Game import g_game
from time import sleep
from Db.CharacterDatabase import CharacterDB
from Db.ItemDatabase import ItemDB
from Db.AccountDatabase import AccountDB
from Db.RoomDatabase import RoomDB
from Db.PortalDatabase import PortalDB
from Db.RegionDatabase import RegionDB

telnetlistener = ListeningManager()
telnetconnectionmanager = ConnectionManager(128, 60, 65536)

telnetlistener.SetConnectionManager(telnetconnectionmanager)
telnetlistener.AddPort(5098)
telnetlistener.AddPort(5099)

g_game.LoadAll()

while g_game.GetRunning():
    telnetlistener.Listen()
    telnetconnectionmanager.Manage()
    g_game.ExecuteLoop()
    sleep(1)

g_game.SaveAll()

CharacterDB.Purge()
ItemDB.Purge()
AccountDB.Purge()
RoomDB.Purge()
PortalDB.Purge()
RegionDB.Purge()
