'''
Created on 2012-6-4

@author: Sky
'''
from Scripts.Logic import Logic
from accessors.CharacterAccessor import character
from accessors.ItemAccessor import item
from accessors.PortalAccessor import portal
from accessors.RoomAccessor import room

class TelnetReporter(Logic):
    def __init__(self, p_id, p_conn):
        self.m_id = p_id
        self.m_conn = p_conn
        
    def GetName(self):
        return "telnetreporter"
    
    def CanSave(self):
        return False
    
    def DoAction(self, p_action):
        if p_action.actiontype == "enterroom":
            self.EnterRoom(p_action.data1, p_action.data2)
        elif p_action.actiontype == "leaveroom":
            self.LeaveRoom(p_action.data1, p_action.data2)
        elif p_action.actiontype == "say":
            c = character(p_action.data1)
            self.SendString("<$yellow>" + c.GetName() + " says: <$reset>" + p_action.stringdata)
        elif p_action.actiontype == "seeroom":
            self.SeeRoom(p_action.data1)
        elif p_action.actiontype == "seeroomname":
            self.SeeRoomName(p_action.data1)
        elif p_action.actiontype == "seeroomdescription":
            self.SeeRoomDesc(p_action.data1)
        elif p_action.actiontype == "seeroomexits":
            self.SeeRoomExits(p_action.data1)
        elif p_action.actiontype == "seeroomcharacters":
            self.SeeRoomCharacters(p_action.data1)
        elif p_action.actiontype == "seeroomitems":
            self.SeeRoomItems(p_action.data1)
        elif p_action.actiontype == "leave":
            self.m_conn.RemoveHandler()
        elif p_action.actiontype == "hangup":
            self.m_conn.Close()
            self.m_conn.ClearHandlers()
        elif p_action.actiontype == "error":
            self.SendString("<$bold><$red>" + p_action.stringdata)
        elif p_action.actiontype == "announce":
            self.SendString("<$bold><$cyan>" + p_action.stringdata)
        elif p_action.actiontype == "vision":
            self.SendString("<$bold><$green>" + p_action.stringdata)
        elif p_action.actiontype == "chat":
            c = character(p_action.data1)
            self.SendString("<$bold><$magenta>" + c.GetName() + " chats: <$reset>" + p_action.stringdata)
        elif p_action.actiontype == "whisper":
            c = character(p_action.data1)
            self.SendString("<$bold><$yellow>" + c.GetName() + " whispers to you: <$reset>" + p_action.stringdata)
        elif p_action.actiontype == "enterrealm":
            c = character(p_action.data1)
            self.SendString("<$bold><$white>" + c.GetName() + " enters the realm.")
        elif p_action.actiontype == "leaverealm":
            c = character(p_action.data1)
            self.SendString("<$bold><$white>" + c.GetName() + " leaves the realm.")
        elif p_action.actiontype == "die":
            self.Died(p_action.data1)
        elif p_action.actiontype == "giveitem":
            self.GaveItem(p_action.data1, p_action.data2, p_action.data3)
        elif p_action.actiontype == "dropitem":
            self.DropItem(p_action.data1, p_action.data2)
        elif p_action.actiontype == "getitem":
            self.GetItem(p_action.data1, p_action.data2)
    
        return 0
    
    def SeeRoom(self, p_id):
        c = character(self.m_id)
        
        self.SeeRoomName(p_id)
        if c.Verbose() == True:
            self.SeeRoomDesc(p_id)
        self.SeeRoomExits(p_id)
        self.SeeRoomCharacters(p_id)
        self.SeeRoomItems(p_id)
        
    def SeeRoomName(self, p_id):
        r = room(p_id)
        self.SendString("<#FFFFFF>" + r.GetName())
        
    def SeeRoomDesc(self, p_id):
        r = room(p_id)
        self.SendString("<$reset>" + r.GetDescription())
        
    def SeeRoomExits(self, p_id):
        r = room(p_id)
        
        if r.Portals() == 0:
            return
        
        string = "<#FF00FF>Exits: <$reset>"
        
        for i in r.m_room.m_portals:
            p = portal(i)
            for j in p.m_portal.m_portals:
                if j.startroom == p_id:
                    string += j.directionname
                    string += " - "
                    string += room(j.destinationroom).GetName()
                    string += "<#FF00FF>, <$reset>"

        string = string[0:len(string) - 19]
        self.SendString(string)
        
    def SeeRoomCharacters(self, p_id):
        r = room(p_id)
        if r.Characters() == 0:
            return
        
        string = "<#FFFF00>People: <$reset>"
        for i in r.m_room.m_characters:
            c = character(i)
            string += c.GetName()
            string += "<#FFFF00>, <$reset>"
        string = string[0:len(string) - 19]
        self.SendString(string)
        
    def SeeRoomItems(self, p_id):
        r = room(p_id)
        if r.Items() == 0:
            return
        
        string = "<#00FF00>Items: <$reset>"
        for data in r.m_room.m_items:
            i = item(data)
            string += i.GetName()
            string += "<#00FF00>, <$reset>"
        string = string[0:len(string) - 19]
        self.SendString(string)
        
    def EnterRoom(self, p_character, p_portal):
        c = character(p_character)
        if p_character == self.m_id:
            self.SeeRoom(c.GetRoom())
            return
        
        if p_portal == "0":
            self.SendString("<$bold><$white>" + c.GetName() + " appears from nowhere!")
            return
        
        p = portal(p_portal)
        self.SendString("<$bold><$white>" + c.GetName() + " enters from the " + p.GetName() + ".")
    
    def LeaveRoom(self, p_character, p_portal):
        c = character(p_character)
        if p_character == self.m_id:
            if p_portal == "0":
                self.SendString("<$bold><$white>You disappear!")
                return
            
            e = portal(p_portal)
            self.SendString("<$bold><$white>You enter the " + e.GetName())
            return
        
        if p_portal == "0":
            self.SendString("<$bold><$white>" + c.GetName() + " disappears!")
            return
        
        p = portal(p_portal)
        self.SendString("<$bold><$white>" + c.GetName() + " enters the " + p.GetName() + ".")
    
    def Died(self, p_character):
        string = "<$bold><$red>"
        c = character(p_character)
        if c.GetId() != self.m_id:
            string += c.GetName()
            string += " HAS DIED!!!"
        else:
            string += "YOU HAVE DIED!!!"
        self.SendString(string)
        
    def GetItem(self, p_character, p_item):
        string = "<$bold><$yellow>"
        if p_character == self.m_id:
            string += "You pick up "
        else:
            c = character(p_character)
            string += c.GetName()
            string += " picks up "
        i = item(p_item)
        string += i.GetName()
        self.SendString(string)
        
    def DropItem(self, p_character, p_item):
        string = "<$bold><$yellow>"
        if p_character == self.m_id:
            string += "You drop "
        else:
            c = character(p_character)
            string += c.GetName()
            string += " drops "
        i = item(p_item)
        string += i.GetName()
        self.SendString(string)
        
    def GaveItem(self, p_giver, p_receiver, p_item):
        string = "<$bold><$yellow>"
        if p_giver == self.m_id:
            string += "You give "
        else:
            g = character(p_giver)
            string += g.GetName()
            string += " gives "
        i = item(p_item)
        string += i.GetName()
        string += " to "
        
        if p_receiver == self.m_id:
            string += "you."
        else:
            r = character(p_receiver)
            string += r.GetName()
            string += "."
        self.SendString(string)
        
    def SendString(self, p_string):
        self.m_conn.Protocol().SendString(self.m_conn, p_string + "<$reset>\r\n")
