'''
Created on 2012-6-4

@author: Sky
'''
from SocketLib.ConnectionHandler import ConnectionHandler
from Db.AccountDatabase import AccountDB
from Scripts.PythonScript import PythonModule
from Scripts.Script import SCRIPTRELOADMODE_LEAVEEXISTING
from BasicLib.Redis import sr
from SocketLib.Telnet import *
from accessors.CharacterAccessor import character
from network.TelnetGame import TelnetGame
from Db.CharacterDatabase import CharacterDB
from Entities.Character import Character

class TelnetMenu(ConnectionHandler):
    def __init__(self, p_conn, p_account):
        ConnectionHandler.__init__(self, p_conn)
        self.m_account = AccountDB.Get(p_account)
        
    def Enter(self):
        self.PrintMenu()
        
    def Leave(self):
        pass
    
    def Hungup(self):
        pass
    
    def Flooded(self):
        pass
    
    def Handle(self, p_data):
        option = int(p_data)
        if option == 0:
            self.m_connection.Close()
        elif option == 1:
            self.m_connection.AddHandler(TelnetMenuEnter(self.m_connection, self.m_account.GetId()))
        elif option == 2:
            if self.m_account.Characters() >= self.m_account.GetAllowedCharacters():
                self.m_connection.Protocol().SendString(self.m_connection, "<#FF0000>Sorry, you are not allowed any more characters.\r\n")
                return
            self.m_connection.AddHandler(TelnetMenuNew(self.m_connection, self.m_account.GetId()))
        elif option == 3:
            self.m_connection.AddHandler(TelnetMenuDelete(self.m_connection, self.m_account.GetId()))
        elif option == 4:
            self.m_connection.AddHandler(TelnetMenuHelp(self.m_connection, self.m_account.GetId()))
            
    def PrintMenu(self):
        string = clearscreen + \
        "<#FFFFFF>-------------------------------------------------------------------------------\r\n" + \
        "<#FFFF00> BetterMUD v1.0 Main Menu\r\n" + \
        "<#FFFFFF>-------------------------------------------------------------------------------\r\n" + \
        " 0 - Quit\r\n" + \
        " 1 - Enter the Game\r\n" + \
        " 2 - Create a new Character\r\n" + \
        " 3 - Delete an existing Character\r\n" + \
        " 4 - View Help\r\n" + \
        "-------------------------------------------------------------------------------\r\n" + \
        "<#7F7F7F> Enter Choice: <#FFFFFF>";
        self.m_connection.Protocol().SendString(self.m_connection, string)
        
class TelnetMenuHelp(ConnectionHandler):
    def __init__(self, p_conn, p_account):
        ConnectionHandler.__init__(self, p_conn)
        self.m_account = AccountDB.Get(p_account)
        
    def Handle(self, p_data):
        self.m_connection.RemoveHandler()
        
    def Enter(self):
        self.PrintHelp()
        
    def Leave(self):
        pass
    
    def Hungup(self):
        pass
    
    def Flooded(self):
        pass
    
    def PrintHelp(self):
        string = \
"<#FFFFFF>BETTERMUD 1.0 HELP\r\n" + \
"<#7F7F7F>\r\n" + \
"Welcome to BetterMUD, the second MUD for the book MUD Game Programming, by\r\n" + \
"Ron Penton. There is no central theme due to the fact that this is a learning\r\n" + \
"MUD, where you are taught to code any number of things. As such, the realm\r\n" + \
"you are entering may be bizzarre, and full of strange non-serious items,\r\n" + \
"and people too. We're here to have fun and play around, and discuss MUD\r\n" + \
"technology here.\r\n" + \
"\r\n" + \
"The first thing you should do is <#FF0000>Create an account<#7f7f7f>, and then you can\r\n" + \
"<#FF0000>Create a character<#7f7f7f>, which you will use to play around with. Every account\r\n" + \
"is allowed to own two characters at the start, but you may gain the abilities\r\n" + \
"to have more than two by being a dedicated and helpful member of the community.\r\n" + \
"\r\n" + \
"Please do not abuse this server, it is here for your enjoyment. Thank you,\r\n" + \
"Ron Penton.\r\n" + \
"\r\n" + \
"<#0000FF>http://ronpenton.net/MUDBook/\r\n" + \
"<#FFFFFF>MUDBook@ronpenton.net\r\n" + \
"<#7f7f7f>(title all emails with 'MUDBOOK:' or else I may not see them, thank you.)"
        self.m_connection.Protocol().SendString(self.m_connection, clearscreen + string)
        
class TelnetMenuNew(ConnectionHandler):
    def __init__(self, p_conn, p_account):
        ConnectionHandler.__init__(self, p_conn)
        self.m_account = AccountDB.Get(p_account)
        self.m_char = "0"
        self.m_creationmod = PythonModule()
        self.m_creationmod.Load("../data/logon/logon.py")
        self.m_creationmod.Reload(SCRIPTRELOADMODE_LEAVEEXISTING)
        
    def Enter(self):
        self.PrintRaces()
        
    def Leave(self):
        pass
    
    def Hungup(self):
        pass
    
    def Flooded(self):
        pass   
    
    def Handle(self, p_data):
        if self.m_char != "0":
            if not AccountDB.AcceptibleName(p_data):
                self.m_connection.Protocol().SendString(self.m_connection, \
                "<#FF0000>Sorry, that name is not acceptible\r\n" \
                "<#00FF00>Please enter your desired name: <#FFFFFF>")
                return
            
            if CharacterDB.FindName(p_data) != "0":
                self.m_connection.Protocol().SendString(self.m_connection, \
                "<#FF0000>Sorry, that name is already taken\r\n" \
                "<#00FF00>Please enter your desired name: <#FFFFFF>")
                return
            
            c = character(self.m_char)
            c.SetName(p_data)
            self.m_connection.RemoveHandler()
            return
        
        option = int(p_data)
        
        if option == 0:
            self.m_connection.RemoveHandler()
            return
        
        if self.m_account.Characters() >= self.m_account.GetAllowedCharacters():
            self.m_connection.Protocol().SendString(self.m_connection, "<#FF0000>Haha, nice try. You're not allowed any more characters!\r\n")
            return
        
        self.m_char = self.m_creationmod.Call("gettemplateid", option)
        
        if self.m_char == "0":
            self.m_connection.Protocol().SendString(self.m_connection, "<#FF0000>Invalid option, please try again: <#FFFFFF>")
            return
        
        self.m_char = CharacterDB.Generate(self.m_char, Character())
        character(self.m_char).SetAccount(self.m_account.GetId())
        self.m_account.AddCharacter(self.m_char)
        
        self.m_creationmod.Call("setup", self.m_char)
        
        self.m_connection.Protocol().SendString(self.m_connection, "<#00FF00>Please enter your desired name: <#FFFFFF>")
        
    def PrintRaces(self):
        string = self.m_creationmod.Call("listchars")
        self.m_connection.Protocol().SendString(self.m_connection, string)
    
class TelnetMenuDelete(ConnectionHandler):
    def __init__(self, p_conn, p_account):
        ConnectionHandler.__init__(self, p_conn)
        self.m_account = AccountDB.Get(p_account)
        self.m_char = "0"
        
    def Enter(self):
        self.PrintCharacters()
        
    def Leave(self):
        pass
    
    def Hungup(self):
        pass
    
    def Flooded(self):
        pass
    
    def Handle(self, p_data):
        if self.m_char != "0":
            if p_data != "Y" and p_data != "y":
                self.m_connection.RemoveHandler()
                return
            
            self.m_account.DelCharacter(self.m_char)
            self.m_connection.RemoveHandler()
            return
        
        option = int(p_data)
        
        if option == 0:
            self.m_connection.RemoveHandler()
            return
        
        if option > self.m_account.Characters():
            self.m_connection.Protocol().SendString(self.m_connection, \
            "<#FF0000>INVALID CHARACTER NUMBER\r\n" \
            "<#FFFFFF>Enter Number of Character to delete: ")
            return
        
        c = self.m_account.m_characters[option - 1]
        self.m_char = c
        
        self.m_connection.Protocol().SendString(self.m_connection, "<#FF0000>Really Delete Character? (Y/N) ")
        
    def GetCharacters(self):
        chars = ""
        for i in range(len(self.m_account.m_characters)):
            chars += " " + str(i + 1) + " - "
            c = character(self.m_account.m_characters[i])
            chars += c.GetName() + "\r\n"
        return chars
            
    def PrintCharacters(self):
        string = \
        "<#7F7F7F>-------------------------------------------------------------------------------\r\n" \
        "<#FFFF00> Your Characters\r\n" \
        "<#7F7F7F>-------------------------------------------------------------------------------\r\n"
        
        chars = " 0   - Go Back\r\n"
        chars += self.GetCharacters()
        chars += \
        "<#7F7F7F>-------------------------------------------------------------------------------\r\n" \
        "Enter number of character to delete: "
        
        self.m_connection.Protocol().SendString(self.m_connection, string + chars)
    
class TelnetMenuEnter(ConnectionHandler):
    def __init__(self, p_conn, p_account):
        ConnectionHandler.__init__(self, p_conn)
        self.m_account = AccountDB.Get(p_account)
        
    def Enter(self):
        self.PrintCharacters()
        
    def Leave(self):
        pass
    
    def Hungup(self):
        pass
    
    def Flooded(self):
        pass
    
    def Handle(self, p_data):
        option = int(p_data)
        
        if option == 0:
            self.m_connection.RemoveHandler()
            return
        
        if option > self.m_account.Characters():
            self.m_connection.Protocol().SendString( \
            self.m_connection, \
            "<#FF0000>INVALID CHARACTER NUMBER\r\n" \
            "<#FFFFFF>Enter Number of Character to use: ")
            return
        
        c = self.m_account.m_characters[option - 1]
        self.m_connection.SwitchHandler(TelnetGame(self.m_connection, self.m_account.GetId(), c))
        
    def GetCharacters(self):
        chars = ""
        for i in range(len(self.m_account.m_characters)):
            chars += " " + str(i + 1) + " - "
            c = character(self.m_account.m_characters[i])
            chars += c.GetName() + "\r\n"
        return chars
    
    def PrintCharacters(self):
        string = \
        "<#7F7F7F>-------------------------------------------------------------------------------\r\n" \
        "<#FFFF00> Your Characters\r\n" \
        "<#7F7F7F>-------------------------------------------------------------------------------\r\n"
        chars = " 0 - Go Back\r\n"
        
        chars += self.GetCharacters()
            
        chars += \
        "<#7F7F7F>-------------------------------------------------------------------------------\r\n" \
        "Enter number of character to use: "
        
        self.m_connection.Protocol().SendString(self.m_connection, string + chars)



