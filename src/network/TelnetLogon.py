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

def GetReturnJsonString(issuccess, errormsg = "", arg0 = "", arg1 = "", arg2 = "", arg3 = "", arg4 = "", arg5 = ""):
    obj = {}
    obj["IsSuccess"] = str(issuccess)
    obj["ErrorMsg"] = errormsg
    obj["Arg0"] = arg0
    obj["Arg1"] = arg1
    obj["Arg2"] = arg2
    obj["Arg3"] = arg3
    obj["Arg4"] = arg4
    obj["Arg5"] = arg5
    return str(obj).replace("'", "\"")

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
            self.m_connection.Protocol().SendString(self.m_connection, GetReturnJsonString(True, "Too many incorrect responses, closing connection!"))
            self.m_connection.Close()
            return
        
        p_data = eval(p_data[p_data.find("{"):])
        
        if p_data["Command"] == "Register":
            id1 = AccountDB.FindName(p_data["Arg0"])
            if id1 != "0":
                self.m_errors += 1
                self.m_connection.Protocol().SendString(self.m_connection, GetReturnJsonString(False, "The account name has already been taken."))
            elif not AccountDB.AcceptibleName(p_data["Arg0"]):
                    self.m_errors += 1
                    self.m_connection.Protocol().SendString(self.m_connection, GetReturnJsonString(False, "The account name is unacceptible."))
            else:
                self.m_state = LogonState_ENTERNEWPASS
                self.m_name = p_data["Arg0"]
                if p_data["Arg1"].find(" ") != -1:
                    self.m_errors += 1
                    self.m_connection.Protocol().SendString(self.m_connection, GetReturnJsonString(False, "Password invalid."))
                else:
                    self.m_connection.Protocol().SendString(self.m_connection, GetReturnJsonString(False, "System can not create new account."))
                    '''
                    #create and get the new account.
                    id1 = AccountDB.Create(self.m_name, p_data["Arg1"])
                    self.m_account = id1
                    newaccount = AccountDB.Get(id1)
                    
                    #if AccountDB.Size() == 0:
                    #    newaccount.SetAccessLevel(accesslevel_Admin)
                    newaccount.SetAccessLevel(accesslevel_Admin)
                    self.m_connection.Protocol().SendString(self.m_connection, GetReturnJsonString(True, "", id1))    
                    self.GotoMenu()
                    '''
            return            
            
        if p_data["Command"] == "LogIn":
            id1 = AccountDB.FindName(p_data["Arg0"])
            if id1 == "0":
                self.m_errors += 1
                self.m_connection.Protocol().SendString(self.m_connection, GetReturnJsonString(False, "Account is not exist."))
            else:
                self.m_account = id1
                a = AccountDB.Get(id1)
                if a.GetBanned():
                    self.m_connection.Protocol().SendString(self.m_connection, GetReturnJsonString(False, "Account banned."))
                else:
                    self.m_name = a.GetName()
                    self.m_pass = a.GetPassword()
                    if self.m_pass != p_data["Arg1"]:
                        self.m_connection.Protocol().SendString(self.m_connection, GetReturnJsonString(False, "Password error."))
                    else:
                        self.m_connection.Protocol().SendString(self.m_connection, GetReturnJsonString(True, "", id1))
            return
        
    def Enter(self):
        self.m_connection.Protocol().SendString(self.m_connection, GetReturnJsonString(True))
        
    def GotoMenu(self):
        c = self.m_connection
        id1 = self.m_account
        c.RemoveHandler()
        c.AddHandler(TelnetMenu(c, id1))

