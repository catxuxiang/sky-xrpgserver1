'''
Created on 2012-6-3

@author: Sky
'''
from Scripts.CPPCommand import CPPCommand
from Entities.Action import Action
from BasicLib.BasicLibString import ParseWord
from Scripts.Script import SCRIPTRELOADMODE_LEAVEEXISTING, SCRIPTRELOADMODE_RELOADFUNCTIONS
from accessors.RoomAccessor import room
from accessors.PortalAccessor import portal

class CPPCommandQuit(CPPCommand):
    def __init__(self, p_character):
        CPPCommand.__init__(self, p_character, "quit", "\"quit\"", "This removes your character from the game and takes you back to the Game Menu.")
        
    def Execute(self, p_parameters):
        self.m_character.DoAction(Action("leave"))
        
        
class CPPCommandChat(CPPCommand):
    def __init__(self, p_character):
        CPPCommand.__init__(self, p_character, "chat", "\"chat <message>\"", "This sends a message to every player who is currently logged into the game.")

    def Execute(self, p_parameters):
        if len(p_parameters) == 0:
            self.m_character.DoAction("error", "0", "0", "0", "0", "Usage: " + self.GetUsage())
            return
        CPPCommand.g_game.AddActionAbsolute(0, "chat", self.m_character.GetId(), "0", "0", "0", p_parameters)
            
class CPPCommandSay(CPPCommand):
    def __init__(self, p_character):
        CPPCommand.__init__(self, p_character, "say", "\"say <message>\"", "This sends a message to every character in the same room as you.")
    
    def Execute(self, p_parameters):
        if len(p_parameters) == 0:
            self.m_character.DoAction("error", "0", "0", "0", "0", "Usage: " + self.GetUsage())
            return
        CPPCommand.g_game.AddActionAbsolute(0, "attemptsay", self.m_character.GetId(), "0", "0", "0", p_parameters)
            
class CPPCommandKick(CPPCommand):
    def __init__(self, p_character):
        CPPCommand.__init__(p_character, "kick", "\"kick <user>\"", "This kicks a user from the realm.")
        
    def Execute(self, p_parameters):
        if len(p_parameters) == 0:
            self.m_character.DoAction("error", "0", "0", "0", "0", "Usage: " + self.GetUsage())
            return
        c = None
        for i in CPPCommand.g_game.m_players:
            if i.GetName().lower() == p_parameters.lower().strip():
                c = i
                break
        if c == None:
            self.m_character.DoAction("error", "0", "0", "0", "0", "Cannot find user " + p_parameters)
            return
        
        CPPCommand.g_game.AddActionAbsolute(0, "announce", "0", "0", "0", "0", c.GetName() + " has been kicked")
        c.DoAction("hangup")

class CPPCommandQuiet(CPPCommand):
    def __init__(self, p_character):
        CPPCommand.__init__(self, p_character, "quiet", "\"quiet <on|off>\"", "Sets your quiet mode. When not quiet, unrecognized commands will be said as room-speech.")
        
    def Execute(self, p_parameters):
        if p_parameters == "on":
            self.m_character.SetQuiet(True)
            self.m_character.DoAction("announce", "0", "0", "0", "0", "You are now in QUIET mode")
        elif p_parameters == "off":
            self.m_character.SetQuiet(False)
            self.m_character.DoAction("announce", "0", "0", "0", "0", "You are now in LOUD mode")
        else:
            self.m_character.DoAction("error", "0", "0", "0", "0", "Usage: " + self.GetUsage())
            
class CPPCommandShutdown(CPPCommand):
    def __init__(self, p_character):
        CPPCommand.__init__(self, p_character, "shutdown", "\"shutdown\"", "Shuts down the MUD")
        
    def Execute(self, p_parameters):
        if len(p_parameters) != 0:
            CPPCommand.g_game.DoAction("announce", "0", "0", "0", "0", "The Server is shutting down: " + p_parameters)
        else:
            CPPCommand.g_game.DoAction( "announce", "0", "0", "0", "0", "The Server is shutting down" )
        CPPCommand.g_game.ShutDown()
        
class CPPCommandLook(CPPCommand):
    def __init__(self, p_character):
        CPPCommand.__init__(self, p_character, "look", "\"look <|object>\"", "Looks at the room (default), or at an optional object within the room")
        
    def Execute(self, p_parameters):
        self.m_character.DoAction("seeroom", self.m_character.GetRoom())
        
class CPPCommandGo(CPPCommand):
    def __init__(self, p_character):
        CPPCommand.__init__(self, p_character, "go", "\"go <exit>\"", "Tries to move your character into a portal")
        
    def Execute(self, p_parameters):
        if len(p_parameters) == 0:
            self.m_character.DoAction("error", "0", "0", "0", "0", "Usage: " + self.GetUsage())
            return
        
        r = room(self.m_character.GetRoom())
        for i in r.m_room.m_portals:
            for j in portal(i).m_portal.m_portals:
                if j.directionname.lower() == p_parameters.lower().strip() and j.startroom == self.m_character.GetRoom():
                    CPPCommand.g_game.AddActionAbsolute(0, "attemptenterportal", self.m_character.GetId(), i)
                    return
        self.m_character.DoAction("error", "0", "0", "0", "0", "You don't see that exit here!")

class CPPCommandCommands(CPPCommand):
    def __init__(self, p_character):
        CPPCommand.__init__(self, p_character, "commands", "\"commands\"", "Lists your commands")
        
    def Execute(self, p_parameters):
        self.m_character.DoAction("announce", "0", "0", "0", "0", "<#FFFFFF>-------------------------------------------------------------------------------")
        self.m_character.DoAction("announce", "0", "0", "0", "0", "<#FFFFFF> Command                          | Usage" )
        self.m_character.DoAction("announce", "0", "0", "0", "0", "<#FFFFFF>-------------------------------------------------------------------------------")

        for i in self.m_character.m_character.m_commands:
            self.m_character.DoAction("announce", "0", "0", "0", "0", "<$reset> " + i.GetName() + "| " + i.GetUsage())

class CPPCommandReloadScript(CPPCommand):
    CommandDB = None    
    def __init__(self, p_character):
        CPPCommand.__init__(self, p_character, "reloadscript", "\"reloadscript <type> <file> <keepall|keepdata>\"", "Reloads a script")
        
    def Execute(self, p_parameters):
        if len(p_parameters.strip().split(" ")) < 3:
            self.m_character.DoAction("error", "0", "0", "0", "0", "Usage: " + self.GetUsage())
            return
                    
        type1 = ParseWord(p_parameters, 0)
        file = "../data/commands/" + ParseWord(p_parameters, 1) + ".py"
        flag = ParseWord(p_parameters, 2)
        
        if flag == "keepall":
            flagtype = SCRIPTRELOADMODE_LEAVEEXISTING
        elif flag == "keepdata":
            flagtype = SCRIPTRELOADMODE_RELOADFUNCTIONS
        else:
            self.m_character.DoAction("error", "0", "0", "0", "0", "Usage: " + self.GetUsage())
            return
        
        if type1 == "commands":
            CPPCommandReloadScript.CommandDB.Reload(file, flagtype)
            self.m_character.DoAction("announce", "0", "0", "0", "0", "Character Script " + file + " reloaded!")
            return

        self.m_character.DoAction("error", "0", "0", "0", "0", "Invalid Script Type")
