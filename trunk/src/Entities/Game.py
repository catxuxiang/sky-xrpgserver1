'''
Created on 2012-6-4

@author: Sky
'''
from Entities.Action import *
from Db.CharacterDatabase import CharacterDB
from BasicLib.BasicLibString import ParseWord, RemoveWord
from Db.ItemDatabase import ItemDB
from Db.RoomDatabase import RoomDB
from Db.AccountDatabase import AccountDB
from Db.RegionDatabase import RegionDB
from Db.CommandDatabase import CommandDB
from Db.LogicDatabase import LogicDB
from Db.PortalDatabase import PortalDB
from Db.AccountDatabase import AccountDatabase
from Entities.Character import Character
from Entities.Item import Item
from BasicLib.BasicLibTime import Timer
from BasicLib.Redis import sr
from accessors.CharacterAccessor import character
from accessors.ItemAccessor import item
from accessors.RoomAccessor import room
from accessors.PortalAccessor import portal
from accessors.RegionAccessor import region
from Scripts.CPPCommand import CPPCommand
from Scripts.CPPCommands import CPPCommandReloadScript


class Game:
    def __init__(self):
        self.m_running = True
        self.m_gametime = Timer()
        self.m_players = []
        self.m_characters = []
        self.m_timerregistry = []
        
    def DoJoinQuantities(self, p_e, p_id):
        keep = item(p_id)
        
        for i in p_e.m_items:
            if i != keep.GetId():
                check = item(i)
                if check.GetTemplateId() == keep.GetTemplateId():
                    keep.SetQuantity(keep.GetQuantity() + check.GetQuantity())
                    self.DeleteItem(i)
    
    def AddCharacter(self, p_id):
        self.m_characters.append(p_id)
        
    def AddPlayer(self, p_id):
        self.m_players.append(p_id)
        
    def RemoveCharacter(self, p_id):
        index = 0
        for i in self.m_characters:
            if i == p_id:
                break
            index += 1
        if index < len(self.m_characters):
            del self.m_characters[index]
            
    def RemovePlayer(self, p_id):
        index = 0
        for i in self.m_players:
            if i == p_id:
                break
            index += 1
        if index < len(self.m_players):
            del self.m_players[index]
            
    def GetRunning(self):
        return self.m_running
    
    def ShutDown(self):
        self.m_running = False
        
    def HasPlayer(self, p_id):
        return p_id in self.m_players
    
    def GetTime(self):
        return self.m_gametime.GetMS()
    
    def ResetTime(self):
        self.m_gametime.Reset()
        
    def DoAction(self, p_action, p_data1 = "0", p_data2 = "0", p_data3 = "0", p_data4 = "0", p_data = ""):
        if type(p_action) == str:
            self.DoAction(Action(p_action, p_data1, p_data2, p_data3, p_data4, p_data))
        else:
            if p_action.actiontype == "chat" or p_action.actiontype == "announce":
                self.ActionRealmPlayers(p_action)
            elif p_action.actiontype == "do":
                self.RouteAction(p_action)
            elif p_action.actiontype == "modifyattribute":
                self.ModifyAttribute(p_action)
            elif p_action.actiontype == "vision":
                self.ActionRoomCharacters(p_action, p_action.data1)
            elif p_action.actiontype == "enterrealm":
                self.Login(p_action.data1)
            elif p_action.actiontype == "leaverealm":
                self.Logout(p_action.data1)
            elif p_action.actiontype == "attemptsay":
                self.Say(p_action.data1, p_action.stringdata)
            elif p_action.actiontype == "command":
                self.DoCommand(p_action.data1, p_action.stringdata)
            elif p_action.actiontype == "attemptenterportal":
                self.EnterPortal(p_action.data1, p_action.data2)
            elif p_action.actiontype == "attempttransport":
                self.Transport(p_action.data1, p_action.data2)
            elif p_action.actiontype == "forcetransport":
                self.ForceTransport(p_action.data1, p_action.data2)
            elif p_action.actiontype == "attemptgetitem":
                self.GetItem(p_action.data1, p_action.data2, p_action.data3)
            elif p_action.actiontype == "attemptdropitem":
                self.DropItem(p_action.data1, p_action.data2, p_action.data3)
            elif p_action.actiontype == "attemptgiveitem":
                self.GiveItem(p_action.data1, p_action.data2, p_action.data3, p_action.data4)
            elif p_action.actiontype == "spawnitem":
                self.SpawnItem(p_action.data1, p_action.data2, p_action.data3, p_action.data4)
            elif p_action.actiontype == "spawncharacter":
                self.SpawnCharacter(p_action.data1, p_action.data2)
            elif p_action.actiontype == "destroyitem":
                self.DestroyItem(p_action.data1)
            elif p_action.actiontype == "destroycharacter":
                self.DestroyCharacter(p_action.data1)
            elif p_action.actiontype == "cleanup":
                self.Cleanup()
            elif p_action.actiontype == "savedatabases":
                self.SaveAll()
            elif p_action.actiontype == "saveregion":
                self.SaveRegion(p_action.data1)
            elif p_action.actiontype == "saveplayers":
                self.SavePlayers()
            elif p_action.actiontype == "reloaditems":
                self.ReloadItemTemplates(p_action.stringdata)
            elif p_action.actiontype == "reloadcharacters":
                self.ReloadCharacterTemplates(p_action.stringdata)
            elif p_action.actiontype == "reloadregion":
                self.ReloadRegion(p_action.stringdata)
            elif p_action.actiontype == "reloadcommandscript":
                self.ReloadCommandScript(p_action.stringdata, p_action.data1)
            elif p_action.actiontype == "reloadlogicscript":
                self.ReloadLogicScript(p_action.stringdata, p_action.data1)
            elif p_action.actiontype == "messagelogic":
                self.LogicAction(p_action)
            elif p_action.actiontype == "addlogic":
                self.AddLogic(p_action)
            elif p_action.actiontype == "dellogic":
                self.DelLogic(p_action) 
        
    def ActionRealmPlayers(self, p_action):
        for i in self.m_players:
            p = character(i)
            p.DoAction(p_action)
            
    def ActionRealmCharacters(self, p_action):
        for i in self.m_characters:
            c = character(i)
            c.DoAction(p_action)
            
    def ActionRoomCharacters(self, p_action, p_room):
        r = room(p_room)
        for i in r.m_room.m_characters:
            c = character(i)
            c.DoAction(p_action)        
    
    def ActionRoomItems(self, p_action, p_room):
        r = room(p_room)
        for data in r.m_room.m_items:
            i = item(data)
            i.DoAction(p_action)
            
    def RouteAction(self, p_action):
        if p_action.data1 == str(ENTITYTYPE_CHARACTER):
            character(p_action.data2).DoAction(p_action)
        elif p_action.data1 == str(ENTITYTYPE_ITEM):
            item(p_action.data2).DoAction(p_action)
        elif p_action.data1 == str(ENTITYTYPE_ROOM):
            room(p_action.data2).DoAction(p_action)
        elif p_action.data1 == str(ENTITYTYPE_PORTAL):
            portal(p_action.data2).DoAction(p_action)
        elif p_action.data1 == str(ENTITYTYPE_REGION):
            region(p_action.data2).DoAction(p_action)
            
    def ModifyAttribute(self, p_action):
        if p_action.data1 == str(ENTITYTYPE_CHARACTER):
            c = character(p_action.data2)
            c.SetAttribute(p_action.stringdata, p_action.data3)
            c.DoAction(p_action)
        elif p_action.data1 == str(ENTITYTYPE_ITEM):
            i = item(p_action.data2)
            i.SetAttribute(p_action.stringdata, p_action.data3)
            i.DoAction(p_action)
        elif p_action.data1 == str(ENTITYTYPE_ROOM):
            r = room(p_action.data2)
            r.SetAttribute(p_action.stringdata, p_action.data3)
            r.DoAction(p_action)
        elif p_action.data1 == str(ENTITYTYPE_PORTAL):
            p = portal(p_action.data2)
            p.SetAttribute(p_action.stringdata, p_action.data3)
            p.DoAction(p_action)
        elif p_action.data1 == str(ENTITYTYPE_REGION):
            reg = region(p_action.data2)
            reg.SetAttribute(p_action.stringdata, p_action.data3)
            reg.DoAction(p_action)
    
    def DoCommand(self, p_player, p_command):
        c = CharacterDB.Get(p_player)
        
        full = p_command
        if full == "/":
            full = c.GetLastCommand()
        else:
            c.SetLastCommand(full)
            
        command = ParseWord(full, 0)
        args = RemoveWord(full, 0)
        
        if (not c.GetQuiet()) and command[0] != '/':
            self.DoAction("attemptsay", p_player, "0", "0", "0", full)
            return
        
        if command[0] == '/':
            command = command[1:len(command)]
            
        data = c.FindCommand(command)
        if data == None:
            c.DoAction("error", "0", "0", "0", "0", "Unrecognized Command: " + command)
            return
        
        data.Execute(args)
        
    def Say(self, p_player, p_text):
        c = character(p_player)
        r = room(c.GetRoom())
        reg = region(c.GetRegion())
        
        if c.DoAction("cansay", p_player, "0", "0", "0", p_text) == 1:
            return
        if r.DoAction("cansay", p_player, "0", "0", "0", p_text) == 1:
            return
        if reg.DoAction("cansay", p_player, "0", "0", "0", p_text ) == 1:
            return
        
        self.ActionRoomCharacters(Action("say", p_player, "0", "0", "0", p_text), c.GetRoom())
        r.DoAction("say", p_player, "0", "0", "0", p_text)
        reg.DoAction("say", p_player, "0", "0", "0", p_text)
        
    def Login(self, p_id):
        c = character(p_id)
        r = room(c.GetRoom())
        reg = region(r.GetRegion())
        
        c.SetLoggedIn(True)
        self.AddCharacter(p_id)
        self.AddPlayer(p_id)
        reg.AddCharacter(p_id)
        r.AddCharacter(p_id)

        self.ActionRealmPlayers(Action("enterrealm", p_id))
        reg.DoAction(Action("enterregion", p_id))
        c.DoAction(Action("enterregion", p_id))
        r.DoAction(Action("enterroom", p_id, "0"))
        self.ActionRoomCharacters(Action("enterroom", p_id, "0"), r.GetId())
        self.ActionRoomItems(Action("enterroom", p_id, "0"), r.GetId())
    
    def Logout(self, p_id):
        c = character(p_id)
        r = room(c.GetRoom())
        reg = region(r.GetRegion())
    
        #tell everyone about it
        self.ActionRoomItems(Action("leaveroom", p_id, "0"), c.GetRoom())
        self.ActionRoomCharacters(Action("leaveroom", p_id, "0"), c.GetRoom())
        r.DoAction(Action("leaveroom", p_id, "0"))
        c.DoAction(Action("leaveregion", p_id))
        reg.DoAction(Action("leaveregion", p_id))
        self.ActionRealmPlayers(Action("leaverealm", p_id))
    
        #remove him from the game
        r.DelCharacter(p_id)
        reg.DelCharacter(p_id)
        self.RemovePlayer(p_id)
        self.RemoveCharacter(p_id)
        c.SetLoggedIn(False)
        
    def EnterPortal(self, p_character, p_portal):
        c= character(p_character)
        p = portal(p_portal)
        oldroom = room(c.GetRoom())
    
        # make sure that character can enter portal from current room
        exist = False
        for i in p.m_portal.m_portals:
            if i.startroom == c.GetRoom():
                exist = True
                break
        if exist == False:
            raise Exception("Character " + c.GetName() + " tried entering portal " + p.GetName() + " but has no exit from room " + c.GetRoom().GetName())
    
        # get the destination room
        newroom = room(i.destinationroom)
        changeregion = oldroom.GetRegion() != newroom.GetRegion()
        oldreg = region(oldroom.GetRegion())
        newreg = region(newroom.GetRegion())
    
        # "ask permission" of everyone to leave the room:
        if changeregion:
            if oldreg.DoAction("canleaveregion", p_character, oldreg.GetId()) == 1:
                return
            if newreg.DoAction("canenterregion", p_character, newreg.GetId()) == 1:
                return
            if c.DoAction("canleaveregion", p_character, oldreg.GetId()) == 1:
                return
            if c.DoAction("canenterregion", p_character, newreg.GetId()) == 1:
                return

        if oldroom.DoAction("canleaveroom", p_character) == 1:
            return
        if newroom.DoAction("canenterroom", p_character) == 1:
            return
        if c.DoAction("canleaveroom", p_character) == 1:
            return
        if p.DoAction("canenterportal", p_character) == 1:
            return
    
        # tell the room that the player is leaving
        if changeregion:
            oldreg.DoAction("leaveregion", p_character, oldreg.GetId())
            c.DoAction("leaveregion", p_character, oldreg.GetId())
    
        self.ActionRoomCharacters(Action("leaveroom", p_character, p_portal), c.GetRoom())
        self.ActionRoomItems(Action("leaveroom", p_character, p_portal), c.GetRoom())
        oldroom.DoAction("leaveroom", p_character, p_portal)
    
        # now tell the portal that the player has actually entered
        p.DoAction("enterportal", p_character, p.GetId())
        c.DoAction("enterportal", p_character, p.GetId())
    
        # now move the character
        if changeregion:
            oldreg.DelCharacter(p_character)
            c.SetRegion(newreg.GetId())
            newreg.AddCharacter(p_character)
        
        oldroom.DelCharacter(p_character)
        c.SetRoom(newroom.GetId())
        newroom.AddCharacter(p_character)
    
        # tell everyone in the room that the player has entered
        if changeregion:
            newreg.DoAction("enterregion", p_character, newreg.GetId())
            c.DoAction("enterregion", p_character, newreg.GetId())
    
        newroom.DoAction("enterroom", p_character, p_portal)
        self.ActionRoomCharacters(Action("enterroom", p_character, p_portal), c.GetRoom())
        self.ActionRoomItems(Action("enterroom", p_character, p_portal), c.GetRoom())
        
    def Transport(self, p_character, p_room):
        c = character(p_character)
        oldroom = room(c.GetRoom())
        newroom = room(p_room)
        changeregion = oldroom.GetRegion() != newroom.GetRegion()
        oldreg = region(oldroom.GetRegion())
        newreg = region(newroom.GetRegion())
    
        if changeregion:
            if oldreg.DoAction("canleaveregion", p_character, oldreg.GetId()) == 1:
                return
            if newreg.DoAction("canenterregion", p_character, newreg.GetId()) == 1:
                return
            if c.DoAction("canleaveregion", p_character, oldreg.GetId()) == 1:
                return
            if c.DoAction("canenterregion", p_character, newreg.GetId()) == 1:
                return
    
        if oldroom.DoAction("canleaveroom", p_character, oldroom.GetId()) == 1:
            return
        if newroom.DoAction("canenterroom", p_character, newroom.GetId()) == 1:
            return
        if c.DoAction("canleaveroom", p_character, oldroom.GetId()) == 1:
            return
        if c.DoAction("canenterroom", p_character, newroom.GetId()) == 1:
            return
    
        if changeregion:
            oldreg.DelCharacter(p_character)
            c.SetRegion(newreg.GetId())
            newreg.AddCharacter(p_character)
    
        oldroom.DelCharacter(p_character)
        c.SetRoom(newroom.GetId())
        newroom.AddCharacter(p_character)
    
        if changeregion:
            oldreg.DoAction("leaveregion", p_character, oldreg.GetId())
            c.DoAction("leaveregion", p_character, oldreg.GetId())
    
        oldroom.DoAction("leaveroom", p_character, "0")
        c.DoAction("leaveroom", p_character, "0")
        self.ActionRoomCharacters(Action("leaveroom", p_character, "0"), c.GetRoom())
        self.ActionRoomItems(Action("leaveroom", p_character, "0"), c.GetRoom())
    
        # tell everyone in the room that the player has entered
        if changeregion:
            newreg.DoAction("enterregion", p_character, newreg.GetId())
            c.DoAction("enterregion", p_character, newreg.GetId())
    
        newroom.DoAction("enterroom", p_character, "0")
        self.ActionRoomCharacters(Action("enterroom", p_character, "0"), c.GetRoom())
        self.ActionRoomItems(Action( "enterroom", p_character, "0"), c.GetRoom())
        
    def ForceTransport(self, p_character, p_room):
        c = character(p_character)
        oldroom = room(c.GetRoom())
        newroom = room(p_room)
        changeregion = oldroom.GetRegion() != newroom.GetRegion()
        oldreg = region(oldroom.GetRegion())
        newreg = region(newroom.GetRegion())
    
        if changeregion:
            oldreg.DelCharacter(p_character)
            c.SetRegion(newreg.GetId())
            newreg.AddCharacter(p_character)
    
        oldroom.DelCharacter(p_character)
        c.SetRoom(newroom.GetId())
        newroom.AddCharacter(p_character)
    
        if changeregion:
            oldreg.DoAction("leaveregion", p_character, oldreg.GetId())
            c.DoAction("leaveregion", p_character, oldreg.GetId())
    
        oldroom.DoAction("leaveroom", p_character, "0")
        c.DoAction("leaveroom", p_character, "0")
        self.ActionRoomCharacters(Action("leaveroom", p_character, "0"), c.GetRoom())
        self.ActionRoomItems(Action("leaveroom", p_character, "0"), c.GetRoom())
    
        # tell everyone in the room that the player has entered
        if changeregion:
            newreg.DoAction("enterregion", p_character, newreg.GetId())
            c.DoAction("enterregion", p_character, newreg.GetId())
    
        newroom.DoAction("enterroom", p_character, "0")
        self.ActionRoomCharacters(Action("enterroom", p_character, "0"), c.GetRoom())
        self.ActionRoomItems(Action("enterroom", p_character, "0"), c.GetRoom())
        
    def GetItem(self, p_character, p_item, p_quantity):
        c = character(p_character)
        i = item(p_item)
        r = room(c.GetRoom())
        reg = region(r.GetRegion())
    
        if i.GetRoom() != c.GetRoom() and i.GetRegion() == "0":
            raise Exception( \
                "Character " + c.GetName() + " tried picking up item " + i.GetName() + \
                " but they are not in the same room.")
    
        if i.IsQuantity() and p_quantity < 1:
            c.DoAction("error", "0", "0", "0", "0", \
                "You can't get " + str(p_quantity) + \
                " of those, it's just not physically possible! FOOL!")
            return
    
        if i.IsQuantity() and p_quantity > i.GetQuantity():
            c.DoAction( "error", "0", "0", "0", "0", \
                "You can't get " + str(p_quantity) + \
                ", there are only " + str(i.GetQuantity()) + "!")
            return
    
        if i.DoAction("cangetitem", p_character, p_item, p_quantity) == 1:
            return
        if r.DoAction("cangetitem", p_character, p_item, p_quantity) == 1:
            return
        if reg.DoAction("cangetitem", p_character, p_item, p_quantity) == 1:
            return
        if c.DoAction("cangetitem", p_character, p_item, p_quantity) == 1:
            return
    
        newitemid = 0;
        if i.IsQuantity() and p_quantity != i.GetQuantity():
            item1 = Item()
            item1.m_isquantity = True
            newitemid = ItemDB.Generate(i.GetTemplateId(), item1)
            item(newitemid).SetQuantity(p_quantity)
            i.SetQuantity(i.GetQuantity() - p_quantity)
        else:
            # normal transfer, delete from old room
            r.DelItem(p_item)
            reg.DelItem(p_item)
            newitemid = i.GetId()

        # now move the item to the player
        newitem = item(newitemid)
        newitem.SetRoom(c.GetId())
        newitem.SetRegion("0")
        c.AddItem(newitem.GetId())
    
        r.DoAction("getitem", p_character, newitemid, p_quantity)
        newitem.DoAction("getitem", p_character, newitemid, p_quantity)
        self.ActionRoomCharacters(Action("getitem", p_character, newitemid, p_quantity), c.GetRoom())
        self.ActionRoomItems(Action("getitem", p_character, newitemid, p_quantity), c.GetRoom())
    
        if newitem.IsQuantity():
            self.DoJoinQuantities(CharacterDB.Get(c.GetId()), newitemid)
            
    def DropItem(self, p_character, p_item, p_quantity):
        c = character(p_character)
        i = item(p_item)
        r = room(c.GetRoom())
        reg = region(r.GetRegion())
        
        if i.GetRoom() != c.GetId() or i.GetRegion() != "0":
            raise Exception( \
            "Character " + c.GetName() + " tried dropping item " + i.GetName() + \
            " but he does not own it.")

        if i.IsQuantity() and p_quantity < 1:
            c.DoAction("error", "0", "0", "0", "0", \
                "You can't drop " + str(p_quantity) + \
                " of those, it's just not physically possible! FOOL!")
            return
    
        if i.IsQuantity() and p_quantity > i.GetQuantity():
            c.DoAction( "error", "0", "0", "0", "0", \
                "You can't drop " + str(p_quantity) + \
                ", there are only " + str(i.GetQuantity()) + "!")
            return
    
        if i.DoAction("candropitem", p_character, p_item) == 1:
            return
        if r.DoAction("candropitem", p_character, p_item) == 1:
            return
        if c.DoAction("candropitem", p_character, p_item) == 1:
            return
    
        newitemid = 0
        if i.IsQuantity() and p_quantity != i.GetQuantity():
            newitemid = ItemDB.Generate(i.GetTemplateId(), Item())
            item(newitemid).SetQuantity(p_quantity)
            i.SetQuantity(i.GetQuantity() - p_quantity)
        else:
            # normal transfer, delete from old player
            c.DelItem(p_item)
            newitemid = i.GetId()
    
        # now move the item to the room
        newitem = item(newitemid)
        newitem.SetRoom(r.GetId())
        newitem.SetRegion(reg.GetId())
        r.AddItem(newitemid)
        reg.AddItem(newitemid)
    
        r.DoAction("dropitem", p_character, newitemid, p_quantity)
        self.ActionRoomCharacters(Action("dropitem", p_character, newitemid, p_quantity), c.GetRoom())
        self.ActionRoomItems(Action("dropitem", p_character, newitemid, p_quantity), c.GetRoom())
    
        if newitem.IsQuantity():
            self.DoJoinQuantities(RoomDB.Get(r.GetId()), newitem.GetId())

    def GiveItem(self, p_giver, p_receiver, p_item, p_quantity):
        g = character(p_giver)
        r = character(p_receiver)
        i = item(p_item)
    
        if g.GetRoom() != r.GetRoom():
            raise Exception( \
                "Character " + g.GetName() + " tried giving item " + i.GetName() + \
                " to " + r.GetName() + " but they are not in the same room.")
    
        if i.IsQuantity() and p_quantity < 1:
            g.DoAction("error", "0", "0", "0", "0", \
                "You can't give away " + str(p_quantity) + \
                " of those, it's just not physically possible! FOOL!")
            return
    
        if i.IsQuantity() and p_quantity > i.GetQuantity():
            g.DoAction("error", "0", "0", "0", "0", \
                "You can't give away " + str(p_quantity) + \
                ", you only have " + str(i.GetQuantity()) + "!")
            return
    
        if i.DoAction("candropitem", p_giver, p_item, p_quantity) == 1 or \
            g.DoAction("candropitem", p_giver, p_item, p_quantity) == 1  or \
            i.DoAction("canreceiveitem", p_giver, p_receiver, p_item, p_quantity) == 1 or \
            r.DoAction("canreceiveitem", p_giver, p_receiver, p_item, p_quantity) == 1:
            return
    
        newitemid = 0
        if i.IsQuantity() and p_quantity != i.GetQuantity():
            newitemid = ItemDB.Generate(i.GetTemplateId(), Item())
            item(newitemid).SetQuantity(p_quantity)
            i.SetQuantity(i.GetQuantity() - p_quantity)
        else:
            g.DelItem(p_item)
            newitemid = i.GetId()
    
        # now move the item to the other player
        newitem = item (newitemid)
        newitem.SetRoom(r.GetId())
        r.AddItem(newitemid)
    
        self.ActionRoomCharacters(Action("giveitem", p_giver, p_receiver, newitemid, p_quantity), g.GetRoom())
    
        if newitem.IsQuantity():
            self.DoJoinQuantities(CharacterDB.Get(r.GetId()), newitemid)

    def SpawnItem(self, p_itemtemplate, p_location, p_player, p_quantity):
        newitem = ItemDB.Generate(p_itemtemplate, Item())
        i = item(newitem)
    
        if p_player == "0":
            # load up the room and region
            r = room(p_location)
            reg = region(r.GetRegion())
            
            # physically place it into the realm
            i.SetRoom(p_location)
            i.SetRegion(r.GetRegion())
            r.AddItem(i.GetId())
            reg.AddItem(i.GetId())
    
            # tell the room and the region about the new item
            r.DoAction("spawnitem", newitem)
            reg.DoAction("spawnitem", newitem)
        else:
            # load up the character
            c = character(p_location)
            
            # physically place it into the player
            i.SetRoom(p_location)
            i.SetRegion("0")
            c.AddItem(i.GetId())
    
            # tell the characterabout the new item
            c.DoAction("spawnitem", newitem)

    def SpawnCharacter(self, p_chartemplate, p_location):
        newchar = CharacterDB.Generate(p_chartemplate, Character())
        c = character(newchar)
        r = room(p_location)
        reg = region(r.GetRegion())
    
        # physically place it into the realm
        c.SetRoom(r.GetId())
        c.SetRegion(reg.GetId())
        r.AddCharacter(c.GetId())
        reg.AddCharacter(c.GetId())
    
        # tell the room and the region about the new item
        r.DoAction("spawncharacter", newchar)
        reg.DoAction("spawncharacter", newchar)
    
    def DestroyItem(self, p_item):
        i = item(p_item)
    
        if i.GetRegion() == "0":
            c = character(i.GetRoom())
            c.DoAction("destroyitem", p_item)
            i.DoAction("destroyitem", p_item)
        else:
            r = room(i.GetRoom())
            reg = region(i.GetRegion())
            reg.DoAction("destroyitem", p_item)
            r.DoAction("destroyitem", p_item)
            i.DoAction("destroyitem", p_item)
    
        self.DeleteItem(p_item)

    def DestroyCharacter(self, p_character):
        c = character(p_character)
        r = room(c.GetRoom())
        reg = region(c.GetRegion())
    
        if c.IsPlayer():
            raise Exception("Trying to delete a player")
    
        reg.DoAction("destroycharacter", p_character)
        r.DoAction("destroycharacter", p_character)
        c.DoAction("destroycharacter", p_character)
    
        # force the items into the room
        for data in c.m_character.m_items:
            i = item(data)
            r.AddItem(i.GetId())
            reg.AddItem(i.GetId())
            i.SetRoom(r.GetId())
            i.SetRegion(reg.GetId())
            r.DoAction("dropitem", p_character, i.GetId(), i.GetQuantity())
            reg.DoAction("dropitem", p_character, i.GetId(), i.GetQuantity())
    
        r.DelCharacter(p_character)
        reg.DelCharacter(p_character)
    
        c.ClearHooks()
        c.SetRoom("0")
        c.SetRegion("0")
        
        key = ""
        for i in CharacterDB.m_instances.m_container.keys():
            if CharacterDB.m_instances.m_container[i] == p_character:
                key = i
                break
        if key != "":
            del CharacterDB.m_instances.m_container[key]

    def LogicAction(self, p_act):
        modname = ParseWord(p_act.stringdata, 0)
        l = None
        if p_act.data1 == str(ENTITYTYPE_CHARACTER):
            l = character(p_act.data2).GetLogic(modname)
        elif p_act.data1 == str(ENTITYTYPE_ITEM):
            l = item(p_act.data2).GetLogic(modname)
        elif p_act.data1 == str(ENTITYTYPE_ROOM):
            l = room(p_act.data2).GetLogic(modname)
        elif p_act.data1 == str(ENTITYTYPE_PORTAL):
            l = portal(p_act.data2).GetLogic(modname)
        elif p_act.data1 == str(ENTITYTYPE_REGION):
            l = region(p_act.data2).GetLogic(modname)

        if l == None:
            raise Exception("Game::LogicAction: Cannot load logic " + modname)
        l.DoAction(p_act)
    
    def AddLogic(self, p_act):
        if p_act.data1 == str(ENTITYTYPE_CHARACTER):
            character(p_act.data2).AddLogic(p_act.stringdata)
        elif p_act.data1 == str(ENTITYTYPE_ITEM):
            item(p_act.data2).AddLogic(p_act.stringdata)
        elif p_act.data1 == str(ENTITYTYPE_ROOM):
            room(p_act.data2).AddLogic(p_act.stringdata)
        elif p_act.data1 == str(ENTITYTYPE_PORTAL):
            portal(p_act.data2).AddLogic(p_act.stringdata)
        elif p_act.data1 == str(ENTITYTYPE_REGION):
            region(p_act.data2).AddLogic(p_act.stringdata)

    def DelLogic(self, p_act):
        if p_act.data1 == str(ENTITYTYPE_CHARACTER):
            character(p_act.data2).DelLogic(p_act.stringdata)
        elif p_act.data1 == str(ENTITYTYPE_ITEM):
            item(p_act.data2).DelLogic(p_act.stringdata)
        elif p_act.data1 == str(ENTITYTYPE_ROOM):
            room(p_act.data2).DelLogic(p_act.stringdata)
        elif p_act.data1 == str(ENTITYTYPE_PORTAL):
            portal(p_act.data2).DelLogic(p_act.stringdata)
        elif p_act.data1 == str(ENTITYTYPE_REGION):
            region(p_act.data2).DelLogic(p_act.stringdata)

    def DeleteItem(self, p_item):
        i = item(p_item)
        if i.GetRegion() != "0":
            reg =region(i.GetRegion())
            reg.DelItem(p_item)
            r = room(i.GetRoom())
            r.DelItem(p_item)
        else:
            c = character(i.GetRoom())
            c.DelItem(p_item)
    
        i.SetRoom("0")
        i.SetRegion("0")
        i.ClearHooks()
        key = ""
        for i in ItemDB.m_instances.m_container.keys():
            if ItemDB.m_instances.m_container[i] == p_item:
                key = i
                break
        if key != "":
            del ItemDB.m_instances.m_container[key]
    
    def Cleanup(self):
        ItemDB.Cleanup()
        CharacterDB.Cleanup()

    def SaveAll(self):
        AccountDB.Save()
        CharacterDB.SavePlayers()
        RegionDB.SaveAll()
        self.SaveTimers()
    
    def SavePlayers(self):
        AccountDB.Save()
        CharacterDB.SavePlayers()
    
    def SaveRegion(self, p_region):
        RegionDB.SaveRegion(p_region)
    
    def LoadAll(self):
        # load the templates and accounts first; they depend on nothing else
        AccountDB.Load()
        CharacterDB.LoadTemplates()
        ItemDB.LoadTemplates()
    
        # load the scripts now
        CommandDB.Load()
        LogicDB.Load()
    
        # load the regions
        Character.ItemDB = ItemDB
        Character.CommandDB = CommandDB        
        RegionDB.LoadAll() 
        CharacterDB.LoadPlayers() 
        
        CPPCommandReloadScript.CommandDB = CommandDB
        TimedAction.region = region 
        TimedAction.character = character
        TimedAction.item = item
        TimedAction.room = room
        TimedAction.portal = portal

        for i in RoomDB.m_container.values():
            i.Add(region)
        for i in PortalDB.m_container.values():
            i.Add(region, room)
        for i in CharacterDB.m_instances.m_container.values():
            i.Add(region, room)
        for i in ItemDB.m_instances.m_container.values():
            i.Add(character, region, room)
    
        self.LoadTimers()
    
    def ReloadItemTemplates(self, prefix):
        ItemDB.LoadTemplates(sr, prefix)
    
    def ReloadCharacterTemplates(self, prefix):
        CharacterDB.LoadTemplates(sr, prefix)
    
    def ReloadRegion(self, p_name):
        RegionDB.LoadRegion(p_name)

    def ReloadCommandScript(self, p_name, p_mode):
        CommandDB.Reload("../data/commands/" + p_name + ".py", p_mode)

    def ReloadLogicScript(self, p_name, p_mode):
        LogicDB.Reload("../data/logics/" + p_name + ".py", p_mode)
    
    def SaveTimers(self):
        sr.set("timers:GAMETIME", self.GetTime())
        sr.ltrim("timers:GAMETIME:REGISTRY", 2, 1)
        index = 0
        for i in self.m_timerregistry:
            if i.valid:
                sr.rpush("timers:GAMETIME:REGISTRY", index)
                i.Save(sr, "timers:GAMETIME:REGISTRY:" + str(index))
            index += 1
    
    def LoadTimers(self):
        t = sr.get("timers:GAMETIME")
        if t != None:
            self.m_gametime.Reset(int(t))
            
            for i in range(sr.llen("timers:GAMETIME:REGISTRY")):
                id1 = sr.lindex("timers:GAMETIME:REGISTRY", i)
                a = TimedAction()
                a.Load(sr, "timers:GAMETIME:REGISTRY:" + id1)
                self.AddTimedAction(a)
    
    def FindPlayerOnlinePart(self, p_name):
        for i in self.m_players:
            if character(i).GetName().lower().find(p_name.lower().strip()) == 0:
                return i
        return None
    
    def FindPlayerOnlineFull(self, p_name):
        for i in self.m_players:
            if character(i).GetName().lower() == p_name.lower().strip():
                return i
        return None     
    
    def FindPlayerPart(self, p_name):
        return CharacterDB.FindPlayerPart(p_name)
    
    def FindPlayerFull(self, p_name):
        return CharacterDB.FindPlayerFull(p_name)
    
    def AddActionRelative(self, p_time, p_act, p_data1 = "0", p_data2 = "0", p_data3 = "0", p_data4 = "0", p_data = ""):
        if type(p_act) == str:
            self.AddTimedAction(TimedAction(p_time + self.GetTime(), Action(p_act, p_data1, p_data2, p_data3, p_data4, p_data)))
        else:
            self.AddTimedAction(TimedAction(p_time + self.GetTime(), p_act))
        
    def AddActionAbsolute(self, p_time, p_act, p_data1 = "0", p_data2 = "0", p_data3 = "0", p_data4 = "0", p_data = ""):
        if type(p_act) == str:
            self.AddTimedAction(TimedAction(p_time, Action(p_act, p_data1, p_data2, p_data3, p_data4, p_data)))
        else:
            self.AddTimedAction(TimedAction(p_time, p_act))
        
    def ExecuteLoop(self):
        t = self.GetTime()
    
        index = 0
        while index < len(self.m_timerregistry):
            a = self.m_timerregistry[index]
            if a.executiontime <= t:
                if a.valid:
                    a.Unhook()
                    self.DoAction(a.actionevent)
                del self.m_timerregistry[index]
            else:
                index += 1
                
    def AddTimedAction(self, p_action):
        self.m_timerregistry.append(p_action)
        p_action.Hook()
                
g_game = Game()
CPPCommand.g_game = g_game
AccountDatabase.g_game = g_game
