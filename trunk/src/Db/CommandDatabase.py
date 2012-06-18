'''
Created on 2012-6-3

@author: Sky
'''
from Scripts.PythonScript import PythonDatabase
from Scripts.CPPCommands import *
from Scripts.PythonCommand import PythonCommand

class CommandDatabase(PythonDatabase):
    def __init__(self):
        PythonDatabase.__init__(self, "commands")
        
    def Generate(self, p_str, p_character):
        if p_str == "quit":
            return CPPCommandQuit(p_character)
        elif p_str == "go":
            return CPPCommandGo(p_character)
        elif p_str == "chat":
            return CPPCommandChat(p_character)
        elif p_str == "say":
            return CPPCommandSay(p_character)
        elif p_str == "kick":
            return CPPCommandKick(p_character)
        elif p_str == "quiet":
            return CPPCommandQuiet(p_character)
        elif p_str == "shutdown":
            return CPPCommandShutdown(p_character)
        elif p_str == "look":
            return CPPCommandLook(p_character)
        elif p_str == "commands":
            return CPPCommandCommands(p_character)
        elif p_str == "reloadscript":
            return CPPCommandReloadScript(p_character)
        else:
            command = self.SpawnNew(p_str)
            return PythonCommand(p_character, command)
        raise Exception("Unknown Command Script")
    
CommandDB = CommandDatabase()
