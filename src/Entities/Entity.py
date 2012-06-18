'''
Created on 2012-5-29

@author: Sky
'''
maxentityvalue = 0x7FFFFFFF

class Entity:
    def __init__(self):
        self.m_name = "UNDEFINED"
        self.m_description = "UNDEFINED"
        self.m_id = "0"
        self.m_refcount = 0
        
    def GetName(self):
        return self.m_name
    
    def GetDescription(self):
        return self.m_description
    
    def GetId(self):
        return self.m_id
    
    def AddRef(self):
        self.m_refcount += 1
        
    def DelRef(self):
        self.m_refcount -= 1
        
    def GetRef(self):
        return self.m_refcount
    
    def SetName(self, p_name):
        self.m_name = p_name
        
    def SetDescription(self, p_desc):
        self.m_description = p_desc
        
    def SetId(self, p_id):
        self.m_id = p_id
        
class HasRegion:
    def __init__(self):
        self.m_region = "0"
        
    def GetRegion(self):
        return self.m_region
    
    def SetRegion(self, p_region):
        self.m_region = p_region
        
class HasRoom:
    def __init__(self):
        self.m_room = "0"
        
    def GetRoom(self):
        return self.m_room
    
    def SetRoom(self, p_room):
        self.m_room = p_room
        
class HasTemplateId:
    def __init__(self):
        self.m_templateid = "0"
        
    def GetTemplateId(self):
        return self.m_templateid
    
    def SetTemplateId(self, p_templateid):
        self.m_templateid = p_templateid
        
class HasCharacters:
    def __init__(self):
        self.m_characters = []
        
    def AddCharacter(self, p_character):
        for i in self.m_characters:
            if i == p_character:
                return
        self.m_characters.append(p_character)
        
    def DelCharacter(self, p_character):
        i = 0
        for character in self.m_characters:
            if character == p_character:
                break
            i += 1
        if i < len(self.m_characters):
            del self.m_characters[i]
            
    def Characters(self):
        return len(self.m_characters)
    
class HasItems:
    def __init__(self):
        self.m_items = []
        
    def AddItem(self, p_item):
        for i in self.m_items:
            if i == p_item:
                return        
        self.m_items.append(p_item)
        
    def DelItem(self, p_item):
        i = 0
        for item in self.m_items:
            if item == p_item:
                break
            i += 1
        if i < len(self.m_items):
            del self.m_items[i]
            
    def Items(self):
        return len(self.m_items)
    
class HasRooms:
    def __init__(self):
        self.m_rooms = []
        
    def AddRoom(self, p_room):
        for i in self.m_rooms:
            if i == p_room:
                return          
        self.m_rooms.append(p_room)
        
    def DelRoom(self, p_room):
        i = 0
        for item in self.m_rooms:
            if item == p_room:
                break
            i += 1
        if i < len(self.m_rooms):
            del self.m_rooms[i]
            
    def Rooms(self):
        return len(self.m_rooms)
    
class HasPortals:
    def __init__(self):
        self.m_portals = []
        
    def AddPortal(self, p_portal):
        for i in self.m_portals:
            if i == p_portal:
                return            
        self.m_portals.append(p_portal)
        
    def DelPortal(self, p_portal):
        i = 0
        for portal in self.m_portals:
            if portal == p_portal:
                break
            i += 1
        if i < len(self.m_portals):
            del self.m_portals[i]
            
    def Portals(self):
        return len(self.m_portals)