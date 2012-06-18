'''
Created on 2012-6-4

@author: Sky
'''
from SocketLib.ConnectionHandler import ConnectionHandler
from Db.AccountDatabase import AccountDB
from Entities.Action import Action
from Entities.Game import g_game
from network.TelnetReporter import TelnetReporter
from accessors.CharacterAccessor import character

class TelnetGame(ConnectionHandler):
    def __init__(self, p_conn, p_account, p_character):
        ConnectionHandler.__init__(self, p_conn)
        self.m_account = AccountDB.Get(p_account)
        self.m_character = character(p_character)
        
    def Handle(self, p_data):
        g_game.DoAction("command", self.m_character.GetId(), "0", "0", "0", p_data)
        
    def Enter(self):
        if self.m_character.IsLoggedIn():
            self.m_connection.Protocol().SendString(self.m_connection, "<#FF0000>Hanging up existing connection...\r\n")
            self.m_character.DoAction(Action("hangup"))
        
        self.m_character.AddExistingLogic(TelnetReporter(self.m_character.GetId(), self.m_connection))
        
        #show the news
        #g_game.DoAction("command", self.m_character.GetId(), "0", "0", "0", "/news")
        
        #log in the player
        g_game.DoAction("enterrealm", self.m_character.GetId())
        
    def Leave(self):
        g_game.DoAction("leaverealm", self.m_character.GetId())
        
    def Hungup(self):
        pass
    
    def Flooded(self):
        pass
