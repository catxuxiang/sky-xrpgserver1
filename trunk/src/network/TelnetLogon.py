'''
Created on 2012-6-4

@author: Sky
'''
from SocketLib.ConnectionHandler import ConnectionHandler
from BasicLib.Redis import sr
from SocketLib.Telnet import *
from Db.AccountDatabase import AccountDB
from Entities.Attributes import accesslevel_Admin
from network.TelnetMenu import TelnetMenu

LogonState_ENTERNAME = 0
LogonState_ENTERNEWNAME = 1
LogonState_ENTERNEWPASS = 2
LogonState_ENTERPASS = 3
LogonState_ENTERDEAD = 4

class TelnetLogon(ConnectionHandler):
    def __init__(self, p_conn):
        ConnectionHandler.__init__(self, p_conn)
        self.m_state = LogonState_ENTERNAME
        self.m_errors = 0
        self.m_name = ""
        self.m_pass = ""
        self.m_account = "0"
        
    def Leave(self):
        pass
    
    def Hungup(self):
        pass
    
    def Flooded(self):
        pass
    
    @staticmethod
    def NoRoom(p_connection):
        msg = "Sorry, there is no more room on this server.\r\n"
        try:
            p_connection.Send(msg)
        except Exception:
            pass
        
    def Handle(self, p_data):
        if self.m_errors == 5:
            self.m_connection.Protocol().SendString(self.m_connection, "<#FF0000>Too many incorrect responses, closing connection...\r\n")
            self.m_connection.Close()
            return
        
        if self.m_state == LogonState_ENTERNAME:
            if p_data.strip() == "new":
                string = " \
<#FFFFFF>BetterMUD uses the concept of 'Accounts' to manage your characters inside\r\n \
the game. You must first create an account, and then we can get started creating\r\n \
your characters after that.\r\n \
\r\n\
<#FF0000>Enter your desired account name: <#FFFFFF>"
                self.m_state = LogonState_ENTERNEWNAME
                self.m_connection.Protocol().SendString(self.m_connection, clearscreen + string)
            else:
                id1 = AccountDB.FindName(p_data)
                if id1 == "0":
                    self.m_errors += 1
                    self.m_connection.Protocol().SendString(self.m_connection, \
                    "<#FF0000>Sorry, the account \"<#FFFFFF>" + p_data + \
                    "<#FF0000>\" does not exist.\r\n" + \
                    "Please enter your name, or \"new\" if you are new: <#FFFFFF>")
                else:
                    self.m_state = LogonState_ENTERPASS
                    self.m_account = id1
                    a = AccountDB.Get(id1)
                    if a.GetBanned():
                        self.m_connection.Protocol().SendString(self.m_connection, "<#FF0000>SORRY! You are BANNED!")
                        self.m_connection.Close()
                        self.m_state = LogonState_ENTERDEAD
                        return
                    
                    self.m_name = a.GetName()
                    self.m_pass = a.GetPassword()
                    
                    self.m_connection.Protocol().SendString(self.m_connection, \
                    "<#00FF00>Welcome, <#FFFFFF>" + self.m_name + \
                    "\r\n<#00FF00>Please enter your password: <#FFFFFF>")
            return
        
        if self.m_state == LogonState_ENTERNEWNAME:
            id1 = AccountDB.FindName(p_data)
            if id1 != "0":
                self.m_errors += 1
                self.m_connection.Protocol().SendString(self.m_connection, \
                "<#FF0000>Sorry, the account name \"<#FFFFFF>" + p_data + \
                "<#FF0000>\" has already been taken.\r\n" + \
                "<#FFFF00>Please enter another name: <#FFFFFF>")
            else:
                if not AccountDB.AcceptibleName(p_data):
                    self.m_errors += 1
                    self.m_connection.Protocol().SendString(self.m_connection, \
                    "<#FF0000>Sorry, the account name \"<#FFFFFF>" + p_data + \
                    "<#FF0000>\" is unacceptible.\r\n" + \
                    "<#FFFF00>Please enter your desired name: <#FFFFFF>")
                else:
                    self.m_state = LogonState_ENTERNEWPASS
                    self.m_name = p_data
                    self.m_connection.Protocol().SendString(self.m_connection, \
                    "<#00FF00>Please enter your desired password: <#FFFFFF>")
            return
        
        if self.m_state == LogonState_ENTERNEWPASS:
            if p_data.find(" ") != -1:
                self.m_errors += 1
                self.m_connection.Protocol().SendString(self.m_connection, \
                    "<#FF0000>INVALID PASSWORD!\r\n" \
                    "<#00FF00>Please enter your desired password: <#FFFFFF>")
                return
            
            self.m_connection.Protocol().SendString(self.m_connection, "<#00FF00>Thank you! You are now entering the realm...\r\n")
            
            #create and get the new account.
            id1 = AccountDB.Create(self.m_name, p_data)
            self.m_account = id1
            newaccount = AccountDB.Get(id1)
            
            #if AccountDB.Size() == 0:
            #    newaccount.SetAccessLevel(accesslevel_Admin)
            newaccount.SetAccessLevel(accesslevel_Admin)
                
            self.GotoMenu()
            return
        
        if self.m_state == LogonState_ENTERPASS:
            if self.m_pass == p_data:
                self.m_connection.Protocol().SendString(self.m_connection, \
                    "<#00FF00>Thank you! You are now entering the realm...\r\n")
                self.GotoMenu()
            else:
                self.m_errors += 1
                self.m_connection.Protocol().SendString(self.m_connection, \
                    "<#FF0000>INVALID PASSWORD!\r\n" \
                    "<#FFFF00>Please enter your password: <#FFFFFF>")
            return
        
    def Enter(self):
        string = "1"
        self.m_connection.Protocol().SendString(self.m_connection, string)
        
    def GotoMenu(self):
        c = self.m_connection
        id1 = self.m_account
        c.RemoveHandler()
        c.AddHandler(TelnetMenu(c, id1))

