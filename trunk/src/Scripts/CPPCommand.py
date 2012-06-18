'''
Created on 2012-6-3

@author: Sky
'''
from accessors.CharacterAccessor import character
from Scripts.Command import Command
class CPPCommand(Command):
    g_game = None
    def __init__(self, p_character, p_name, p_usage, p_description):
        self.m_character = character(p_character)
        self.m_name = p_name
        self.m_usage = p_usage
        self.m_description = p_description
        
    def GetName(self):
        return self.m_name
    
    def GetUsage(self):
        return self.m_usage
    
    def GetDescription(self):
        return self.m_description