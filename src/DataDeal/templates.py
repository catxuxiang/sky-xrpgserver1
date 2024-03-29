'''
Created on 2012-6-7

@author: Sky
'''
from BasicLib.Redis import sr
from BasicLib.BasicLibString import ParseWord, RemoveWord
def CreateCharactersList():
    sr.ltrim("templates:characters", 2, 1)
    sr.rpush("templates:characters", "easyenemies")
    sr.rpush("templates:characters", "playerraces")
    sr.rpush("templates:characters", "storekeepers")
    sr.ltrim("templates:characters:easyenemies", 2, 1)
    sr.rpush("templates:characters:easyenemies", "200")
    sr.ltrim("templates:characters:playerraces", 2, 1)
    sr.rpush("templates:characters:playerraces", "1")
    sr.rpush("templates:characters:playerraces", "2")
    sr.rpush("templates:characters:playerraces", "3")
    sr.rpush("templates:characters:playerraces", "4")
    sr.rpush("templates:characters:playerraces", "5")
    sr.ltrim("templates:characters:storekeepers", 2, 1)
    sr.rpush("templates:characters:storekeepers", "300")
    
def Get(file, id1= ""):
    if id1 != "":
        data = id1
    else:
        string = file.readline().strip()
        data = RemoveWord(string, 0)
    print(data)
    return data

def GetHash(file):
    string = file.readline().strip()
    keys = []
    values = []
    while string and string != "[/DATABANK]":
        if string != "[DATABANK]":
            key = RemoveWord(string, 1)
            keys.append(key)
            value = RemoveWord(string, 0)
            values.append(value)
            print(key + "," + value)
        string = file.readline().strip()
    return keys, values

def GetStrings(file):
    file.readline()
    value = file.readline().strip()
    if(value[0] == "["):
        value = ""
    else:
        file.readline()
    print(value)
    return value
        
    
def DealFile(file, prefix):
    id1 = ""
    while True:
        ID = Get(file, id1)
        NAME = Get(file)
        DESCRIPTION = Get(file)
        DATABANKKeys, DATABANKValues = GetHash(file)
        COMMANDS = GetStrings(file)
        LOGICS = GetStrings(file)
        sr.set(prefix + ":" + ID + ":NAME", NAME)
        sr.set(prefix + ":" + ID + ":DESCRIPTION", DESCRIPTION)
        sr.set(prefix + ":" + ID + ":COMMANDS", COMMANDS)
        sr.set(prefix + ":" + ID + ":LOGICS", LOGICS)
        for i in range(len(DATABANKKeys)):
            sr.hset(prefix + ":" + ID + ":DATABANK", DATABANKKeys[i], DATABANKValues[i])
        print("=====================================")
        line = file.readline()
        while line and line.strip() == "":
            line = file.readline()
        if not line:
            break
        id1 = RemoveWord(line, 0)
        
def AddCharactersDetail():
    file = open("../data/templates/characters/easyenemies.data")
    DealFile(file, "templates:characters:easyenemies")
    file.close()
    file = open("../data/templates/characters/storekeepers.data")
    DealFile(file, "templates:characters:storekeepers")
    file.close()
    file = open("../data/templates/characters/playerraces.data")
    DealFile(file, "templates:characters:playerraces")
    file.close()    
    
def CreateItemsList():
    sr.ltrim("templates:items", 2, 1)
    sr.rpush("templates:items", "basicitems")
    sr.rpush("templates:items", "funitems")
    sr.rpush("templates:items", "defaultweapons")
    sr.rpush("templates:items", "money")
    sr.rpush("templates:items", "weapons")    
    sr.ltrim("templates:items:basicitems", 2, 1)
    sr.rpush("templates:items:basicitems", "50")
    sr.rpush("templates:items:basicitems", "51")
    sr.rpush("templates:items:basicitems", "52")
    sr.rpush("templates:items:basicitems", "54")
    sr.rpush("templates:items:basicitems", "55")
    sr.rpush("templates:items:basicitems", "56")
    sr.ltrim("templates:items:funitems", 2, 1)
    sr.rpush("templates:items:funitems", "300")
    sr.ltrim("templates:items:defaultweapons", 2, 1)
    sr.rpush("templates:items:defaultweapons", "100")  
    sr.ltrim("templates:items:money", 2, 1)
    sr.rpush("templates:items:money", "1") 
    sr.rpush("templates:items:money", "2") 
    sr.ltrim("templates:items:weapons", 2, 1)
    sr.rpush("templates:items:weapons", "400") 
    sr.rpush("templates:items:weapons", "401") 
    sr.rpush("templates:items:weapons", "402")
    
def DealItems(file, prefix):
    id1 = ""
    while True:
        ID = Get(file, id1)
        NAME = Get(file)
        DESCRIPTION = Get(file)
        ISQUANTITY = Get(file)
        QUANTITY = Get(file)
        DATABANKKeys, DATABANKValues = GetHash(file)
        LOGICS = GetStrings(file)

        sr.set(prefix + ":" + ID + ":NAME", NAME)
        sr.set(prefix + ":" + ID + ":DESCRIPTION", DESCRIPTION)
        sr.set(prefix + ":" + ID + ":ISQUANTITY", ISQUANTITY)
        sr.set(prefix + ":" + ID + ":QUANTITY", QUANTITY)
        sr.set(prefix + ":" + ID + ":LOGICS", LOGICS)
        for i in range(len(DATABANKKeys)):
            sr.hset(prefix + ":" + ID + ":DATABANK", DATABANKKeys[i], DATABANKValues[i])
        print("=====================================")
        line = file.readline()
        while line and line.strip() == "":
            line = file.readline()
        if not line:
            break
        id1 = RemoveWord(line, 0)    
    
def AddItemsDetail():
    file = open("../data/templates/items/basicitems.data")
    DealItems(file, "templates:items:basicitems")
    file.close()
    file = open("../data/templates/items/defaultweapons.data")
    DealItems(file, "templates:items:defaultweapons")
    file.close()
    file = open("../data/templates/items/funitems.data")
    DealItems(file, "templates:items:funitems")
    file.close() 
    file = open("../data/templates/items/money.data")
    DealItems(file, "templates:items:money")
    file.close() 
    file = open("../data/templates/items/weapons.data")
    DealItems(file, "templates:items:weapons")
    file.close() 
    
def CreateRegionsList():
    sr.ltrim("regions", 2, 1)
    sr.rpush("regions", "Betterton")
    sr.rpush("regions", "DwarvenMine")
    sr.hset("regionsHash", "1", "Betterton")
    sr.hset("regionsHash", "2", "DwarvenMine")
    sr.ltrim("regions:1:characters", 2, 1)
    sr.rpush("regions:1:characters", "3")
    sr.ltrim("regions:1:items", 2, 1)
    sr.rpush("regions:1:items", "16")    
    sr.rpush("regions:1:items", "19")  
    sr.rpush("regions:1:items", "36")  
    sr.rpush("regions:1:items", "45")  
    sr.rpush("regions:1:items", "47")  
    sr.rpush("regions:1:items", "49")  
    sr.rpush("regions:1:items", "51")  
    sr.rpush("regions:1:items", "53")  
    sr.rpush("regions:1:items", "55")  
    sr.rpush("regions:1:items", "57")  
    sr.rpush("regions:1:items", "59")  
    sr.rpush("regions:1:items", "61")  
    sr.rpush("regions:1:items", "63")  
    sr.rpush("regions:1:items", "65")  
    sr.rpush("regions:1:items", "67")  
    sr.rpush("regions:1:items", "69")  
    sr.rpush("regions:1:items", "85")  

    sr.ltrim("regions:1:portals", 2, 1)
    sr.rpush("regions:1:portals", "1")
    sr.rpush("regions:1:portals", "2")
    sr.rpush("regions:1:portals", "3")
    sr.rpush("regions:1:portals", "4")
    sr.rpush("regions:1:portals", "5")
    sr.ltrim("regions:1:rooms", 2, 1)
    sr.rpush("regions:1:rooms", "1")  
    sr.rpush("regions:1:rooms", "2") 
    sr.rpush("regions:1:rooms", "3") 
    sr.rpush("regions:1:rooms", "4") 
    sr.rpush("regions:1:rooms", "5") 
    sr.rpush("regions:1:rooms", "6") 
    
    sr.ltrim("regions:2:items", 2, 1)
    sr.rpush("regions:2:items", "10")    

    sr.ltrim("regions:2:portals", 2, 1)
    sr.rpush("regions:2:portals", "100")

    sr.ltrim("regions:2:rooms", 2, 1)
    sr.rpush("regions:2:rooms", "100") 

def GetDataStrings(file):
    keys = []
    values = []
    file.readline()
    value = file.readline().strip()
    
    while value != "[/LOGICS]":
        key = value
        keys.append(key)
        file.readline()
        value = file.readline().strip()
        val = ""
        while value != "[/DATA]":
            val += value + "\r\n"
            value = file.readline().strip()
        values.append(val)
        value = file.readline().strip()
        print(key + "|" + val)
    return keys, values 

def AddRegionsDetail():
    sr.set("regions:1:NAME", "Betterton")
    sr.set("regions:1:DESCRIPTION", "Betterton")
    sr.set("regions:1:ROOM", "Betterton")
    sr.set("regions:1:REGION", "Betterton")
    sr.set("regions:1:TEMPLATEID", "Betterton")
    sr.set("regions:1:ACCOUNT", "Betterton")
    sr.set("regions:1:QUIETMODE", "Betterton")
    sr.set("regions:1:VERBOSEMODE", "Betterton")
    sr.hset("regions:1:LOGICS", "bettertonmagicianshop", "")
    
    
    sr.set("regions:2:NAME", "DwarvenMine")
    sr.set("regions:2:DESCRIPTION", "You are in the Dwarven mines, a large and ancient collection of tunnels.")   
    sr.hset("regions:2:LOGICS", "noelves", "") 
    
def AddRegionCharactersDetail():
    sr.set("regions:1:characters:3:NAME", "Magician Keeper")
    sr.set("regions:1:characters:3:DESCRIPTION", "Blah blah blah")
    sr.set("regions:1:characters:3:ROOM", "6")
    sr.set("regions:1:characters:3:REGION", "1")
    sr.set("regions:1:characters:3:TEMPLATEID", "300")
    sr.set("regions:1:characters:3:ACCOUNT", "0")
    sr.set("regions:1:characters:3:QUIETMODE", "0")
    sr.set("regions:1:characters:3:VERBOSEMODE", "1")
    sr.hset("regions:1:characters:3:LOGICS", "bettertonmagicianshop", "")
    sr.delete("regions:1:characters:3:ITEMS")
    sr.rpush("regions:1:characters:3:ITEMS", "84")
    sr.set("regions:1:characters:3:ITEMS:84:NAME", "<#> Copper Coins")
    sr.set("regions:1:characters:3:ITEMS:84:DESCRIPTION", "These copper coins are small and dirty, they don't have much value.")
    sr.set("regions:1:characters:3:ITEMS:84:ROOM", "6")
    sr.set("regions:1:characters:3:ITEMS:84:REGION", "1")
    sr.set("regions:1:characters:3:ITEMS:84:ISQUANTITY", "True")
    sr.set("regions:1:characters:3:ITEMS:84:QUANTITY", "830")
    sr.set("regions:1:characters:3:ITEMS:84:TEMPLATEID", "1")
    sr.hset("regions:1:characters:3:ITEMS:84:DATABANK", "arms", "0")
    sr.hset("regions:1:characters:3:ITEMS:84:DATABANK", "currency", "1")
    sr.hset("regions:1:characters:3:ITEMS:84:DATABANK", "value", "1")
    sr.hset("regions:1:characters:3:ITEMS:84:DATABANK", "weight", "1")
    
def AddRegionItemsDetail():
    sr.set("regions:1:items:16:NAME", "Fountain")
    sr.set("regions:1:items:16:DESCRIPTION", "This is a large bubbling fountain, made of granite and marble.")
    sr.set("regions:1:items:16:ROOM", "1")
    sr.set("regions:1:items:16:REGION", "1")
    sr.set("regions:1:items:16:ISQUANTITY", "False")
    sr.set("regions:1:items:16:QUANTITY", "1")
    sr.set("regions:1:items:16:TEMPLATEID", "50")
    sr.hset("regions:1:items:16:DATABANK", "arms", "0")
    sr.hset("regions:1:items:16:DATABANK", "weight", "1000000")
    sr.hset("regions:1:items:16:LOGICS", "cantget", "")

    sr.set("regions:1:items:19:NAME", "<#> Copper Coins")
    sr.set("regions:1:items:19:DESCRIPTION", "These copper coins are small and dirty, they don't have much value.")
    sr.set("regions:1:items:19:ROOM", "1")
    sr.set("regions:1:items:19:REGION", "1")
    sr.set("regions:1:items:19:ISQUANTITY", "True")
    sr.set("regions:1:items:19:QUANTITY", "8281")
    sr.set("regions:1:items:19:TEMPLATEID", "1")
    sr.hset("regions:1:items:19:DATABANK", "arms", "0")
    sr.hset("regions:1:items:19:DATABANK", "currency", "1")
    sr.hset("regions:1:items:19:DATABANK", "value", "1")
    sr.hset("regions:1:items:19:DATABANK", "weight", "1")
    
    sr.set("regions:1:items:36:NAME", "<#> Copper Coins")
    sr.set("regions:1:items:36:DESCRIPTION", "These copper coins are small and dirty, they don't have much value.")
    sr.set("regions:1:items:36:ROOM", "6")
    sr.set("regions:1:items:36:REGION", "1")
    sr.set("regions:1:items:36:ISQUANTITY", "True")
    sr.set("regions:1:items:36:QUANTITY", "110")
    sr.set("regions:1:items:36:TEMPLATEID", "1")
    sr.hset("regions:1:items:36:DATABANK", "arms", "0")
    sr.hset("regions:1:items:36:DATABANK", "currency", "1")
    sr.hset("regions:1:items:36:DATABANK", "value", "1")
    sr.hset("regions:1:items:36:DATABANK", "weight", "1")   
    
    sr.set("regions:1:items:45:NAME", "Small Healing Potion")
    sr.set("regions:1:items:45:DESCRIPTION", "This is a small healing potion.")
    sr.set("regions:1:items:45:ROOM", "6")
    sr.set("regions:1:items:45:REGION", "1")
    sr.set("regions:1:items:45:ISQUANTITY", "False")
    sr.set("regions:1:items:45:QUANTITY", "1")
    sr.set("regions:1:items:45:TEMPLATEID", "55")
    sr.hset("regions:1:items:45:DATABANK", "arms", "0")
    sr.hset("regions:1:items:45:DATABANK", "value", "10")
    sr.hset("regions:1:items:45:DATABANK", "weight", "50")
    
    sr.set("regions:1:items:47:NAME", "Small Healing Potion")
    sr.set("regions:1:items:47:DESCRIPTION", "This is a small healing potion.")
    sr.set("regions:1:items:47:ROOM", "6")
    sr.set("regions:1:items:47:REGION", "1")
    sr.set("regions:1:items:47:ISQUANTITY", "False")
    sr.set("regions:1:items:47:QUANTITY", "1")
    sr.set("regions:1:items:47:TEMPLATEID", "55")
    sr.hset("regions:1:items:47:DATABANK", "arms", "0")
    sr.hset("regions:1:items:47:DATABANK", "value", "10")
    sr.hset("regions:1:items:47:DATABANK", "weight", "50")    
    
    sr.set("regions:1:items:49:NAME", "Small Healing Potion")
    sr.set("regions:1:items:49:DESCRIPTION", "This is a small healing potion.")
    sr.set("regions:1:items:49:ROOM", "6")
    sr.set("regions:1:items:49:REGION", "1")
    sr.set("regions:1:items:49:ISQUANTITY", "False")
    sr.set("regions:1:items:49:QUANTITY", "1")
    sr.set("regions:1:items:49:TEMPLATEID", "55")
    sr.hset("regions:1:items:49:DATABANK", "arms", "0")
    sr.hset("regions:1:items:49:DATABANK", "value", "10")
    sr.hset("regions:1:items:49:DATABANK", "weight", "50")    
    
    sr.set("regions:1:items:51:NAME", "Small Healing Potion")
    sr.set("regions:1:items:51:DESCRIPTION", "This is a small healing potion.")
    sr.set("regions:1:items:51:ROOM", "6")
    sr.set("regions:1:items:51:REGION", "1")
    sr.set("regions:1:items:51:ISQUANTITY", "False")
    sr.set("regions:1:items:51:QUANTITY", "1")
    sr.set("regions:1:items:51:TEMPLATEID", "55")
    sr.hset("regions:1:items:51:DATABANK", "arms", "0")
    sr.hset("regions:1:items:51:DATABANK", "value", "10")
    sr.hset("regions:1:items:51:DATABANK", "weight", "50") 
    
    sr.set("regions:1:items:53:NAME", "Small Healing Potion")
    sr.set("regions:1:items:53:DESCRIPTION", "This is a small healing potion.")
    sr.set("regions:1:items:53:ROOM", "6")
    sr.set("regions:1:items:53:REGION", "1")
    sr.set("regions:1:items:53:ISQUANTITY", "False")
    sr.set("regions:1:items:53:QUANTITY", "1")
    sr.set("regions:1:items:53:TEMPLATEID", "55")
    sr.hset("regions:1:items:53:DATABANK", "arms", "0")
    sr.hset("regions:1:items:53:DATABANK", "value", "10")
    sr.hset("regions:1:items:53:DATABANK", "weight", "50") 
    
    sr.set("regions:1:items:55:NAME", "Small Healing Potion")
    sr.set("regions:1:items:55:DESCRIPTION", "This is a small healing potion.")
    sr.set("regions:1:items:55:ROOM", "6")
    sr.set("regions:1:items:55:REGION", "1")
    sr.set("regions:1:items:55:ISQUANTITY", "False")
    sr.set("regions:1:items:55:QUANTITY", "1")
    sr.set("regions:1:items:55:TEMPLATEID", "55")
    sr.hset("regions:1:items:55:DATABANK", "arms", "0")
    sr.hset("regions:1:items:55:DATABANK", "value", "10")
    sr.hset("regions:1:items:55:DATABANK", "weight", "50") 
    
    sr.set("regions:1:items:57:NAME", "Small Healing Potion")
    sr.set("regions:1:items:57:DESCRIPTION", "This is a small healing potion.")
    sr.set("regions:1:items:57:ROOM", "6")
    sr.set("regions:1:items:57:REGION", "1")
    sr.set("regions:1:items:57:ISQUANTITY", "False")
    sr.set("regions:1:items:57:QUANTITY", "1")
    sr.set("regions:1:items:57:TEMPLATEID", "55")
    sr.hset("regions:1:items:57:DATABANK", "arms", "0")
    sr.hset("regions:1:items:57:DATABANK", "value", "10")
    sr.hset("regions:1:items:57:DATABANK", "weight", "50") 
    
    sr.set("regions:1:items:59:NAME", "Small Healing Potion")
    sr.set("regions:1:items:59:DESCRIPTION", "This is a small healing potion.")
    sr.set("regions:1:items:59:ROOM", "6")
    sr.set("regions:1:items:59:REGION", "1")
    sr.set("regions:1:items:59:ISQUANTITY", "False")
    sr.set("regions:1:items:59:QUANTITY", "1")
    sr.set("regions:1:items:59:TEMPLATEID", "55")
    sr.hset("regions:1:items:59:DATABANK", "arms", "0")
    sr.hset("regions:1:items:59:DATABANK", "value", "10")
    sr.hset("regions:1:items:59:DATABANK", "weight", "50") 
    
    sr.set("regions:1:items:61:NAME", "Small Healing Potion")
    sr.set("regions:1:items:61:DESCRIPTION", "This is a small healing potion.")
    sr.set("regions:1:items:61:ROOM", "6")
    sr.set("regions:1:items:61:REGION", "1")
    sr.set("regions:1:items:61:ISQUANTITY", "False")
    sr.set("regions:1:items:61:QUANTITY", "1")
    sr.set("regions:1:items:61:TEMPLATEID", "55")
    sr.hset("regions:1:items:61:DATABANK", "arms", "0")
    sr.hset("regions:1:items:61:DATABANK", "value", "10")
    sr.hset("regions:1:items:61:DATABANK", "weight", "50") 
    
    sr.set("regions:1:items:63:NAME", "Small Healing Potion")
    sr.set("regions:1:items:63:DESCRIPTION", "This is a small healing potion.")
    sr.set("regions:1:items:63:ROOM", "6")
    sr.set("regions:1:items:63:REGION", "1")
    sr.set("regions:1:items:63:ISQUANTITY", "False")
    sr.set("regions:1:items:63:QUANTITY", "1")
    sr.set("regions:1:items:63:TEMPLATEID", "55")
    sr.hset("regions:1:items:63:DATABANK", "arms", "0")
    sr.hset("regions:1:items:63:DATABANK", "value", "10")
    sr.hset("regions:1:items:63:DATABANK", "weight", "50") 
    
    sr.set("regions:1:items:65:NAME", "Small Healing Potion")
    sr.set("regions:1:items:65:DESCRIPTION", "This is a small healing potion.")
    sr.set("regions:1:items:65:ROOM", "6")
    sr.set("regions:1:items:65:REGION", "1")
    sr.set("regions:1:items:65:ISQUANTITY", "False")
    sr.set("regions:1:items:65:QUANTITY", "1")
    sr.set("regions:1:items:65:TEMPLATEID", "55")
    sr.hset("regions:1:items:65:DATABANK", "arms", "0")
    sr.hset("regions:1:items:65:DATABANK", "value", "10")
    sr.hset("regions:1:items:65:DATABANK", "weight", "50") 
    
    sr.set("regions:1:items:67:NAME", "Small Healing Potion")
    sr.set("regions:1:items:67:DESCRIPTION", "This is a small healing potion.")
    sr.set("regions:1:items:67:ROOM", "6")
    sr.set("regions:1:items:67:REGION", "1")
    sr.set("regions:1:items:67:ISQUANTITY", "False")
    sr.set("regions:1:items:67:QUANTITY", "1")
    sr.set("regions:1:items:67:TEMPLATEID", "55")
    sr.hset("regions:1:items:67:DATABANK", "arms", "0")
    sr.hset("regions:1:items:67:DATABANK", "value", "10")
    sr.hset("regions:1:items:67:DATABANK", "weight", "50") 
    
    sr.set("regions:1:items:69:NAME", "Small Healing Potion")
    sr.set("regions:1:items:69:DESCRIPTION", "This is a small healing potion.")
    sr.set("regions:1:items:69:ROOM", "6")
    sr.set("regions:1:items:69:REGION", "1")
    sr.set("regions:1:items:69:ISQUANTITY", "False")
    sr.set("regions:1:items:69:QUANTITY", "1")
    sr.set("regions:1:items:69:TEMPLATEID", "55")
    sr.hset("regions:1:items:69:DATABANK", "arms", "0")
    sr.hset("regions:1:items:69:DATABANK", "value", "10")
    sr.hset("regions:1:items:69:DATABANK", "weight", "50")                         
    
    sr.set("regions:1:items:85:NAME", "Scroll of Uberweight")
    sr.set("regions:1:items:85:DESCRIPTION", "This scroll contains the spell of Uberweight on it.")
    sr.set("regions:1:items:85:ROOM", "1")
    sr.set("regions:1:items:85:REGION", "1")
    sr.set("regions:1:items:85:ISQUANTITY", "False")
    sr.set("regions:1:items:85:QUANTITY", "1")
    sr.set("regions:1:items:85:TEMPLATEID", "54")
    sr.hset("regions:1:items:85:DATABANK", "arms", "0")
    sr.hset("regions:1:items:85:DATABANK", "value", "100")
    sr.hset("regions:1:items:85:DATABANK", "weight", "50")
    sr.hset("regions:1:items:85:LOGICS", "canread", "")   
    sr.hset("regions:1:items:85:LOGICS", "uberweightscroll", "")  
    
    sr.set("regions:2:items:10:NAME", "Dwarven Mine Pass")
    sr.set("regions:2:items:10:DESCRIPTION", "This allows entrance to the Dwarven Mines.")
    sr.set("regions:2:items:10:ROOM", "100")
    sr.set("regions:2:items:10:REGION", "2")
    sr.set("regions:2:items:10:ISQUANTITY", "False")
    sr.set("regions:2:items:10:QUANTITY", "1")
    sr.set("regions:2:items:10:TEMPLATEID", "56")
    sr.hset("regions:2:items:10:DATABANK", "arms", "0")
    sr.hset("regions:2:items:10:DATABANK", "value", "100")
    sr.hset("regions:2:items:10:DATABANK", "weight", "50")  

def AddRegionPortalsDetail():
    sr.set("regions:1:portals:1:REGION", "1")
    sr.set("regions:1:portals:1:NAME", "Garden Path")
    sr.set("regions:1:portals:1:DESCRIPTION", "This is a plain garden pathway.")
    sr.rpush("regions:1:portals:1:ENTRY", 1)
    sr.rpush("regions:1:portals:1:ENTRY", 2)
    sr.set("regions:1:portals:1:ENTRY:1:STARTROOM", "1")
    sr.set("regions:1:portals:1:ENTRY:1:DIRECTION", "North")
    sr.set("regions:1:portals:1:ENTRY:1:DESTROOM", "2")
    sr.set("regions:1:portals:1:ENTRY:2:STARTROOM", "2")
    sr.set("regions:1:portals:1:ENTRY:2:DIRECTION", "South")
    sr.set("regions:1:portals:1:ENTRY:2:DESTROOM", "1")
    
    sr.set("regions:1:portals:2:REGION", "1")
    sr.set("regions:1:portals:2:NAME", "Stone Path")
    sr.set("regions:1:portals:2:DESCRIPTION", "This is a plain stone pathway.")
    sr.rpush("regions:1:portals:2:ENTRY", 1)
    sr.rpush("regions:1:portals:2:ENTRY", 2)
    sr.set("regions:1:portals:2:ENTRY:1:STARTROOM", "1")
    sr.set("regions:1:portals:2:ENTRY:1:DIRECTION", "South")
    sr.set("regions:1:portals:2:ENTRY:1:DESTROOM", "3")
    sr.set("regions:1:portals:2:ENTRY:2:STARTROOM", "3")
    sr.set("regions:1:portals:2:ENTRY:2:DIRECTION", "North")
    sr.set("regions:1:portals:2:ENTRY:2:DESTROOM", "1")    
    
    sr.set("regions:1:portals:3:REGION", "1")
    sr.set("regions:1:portals:3:NAME", "Bakery Door")
    sr.set("regions:1:portals:3:DESCRIPTION", "This is doorway leading to the bakery")
    sr.rpush("regions:1:portals:3:ENTRY", 1)
    sr.rpush("regions:1:portals:3:ENTRY", 2)
    sr.set("regions:1:portals:3:ENTRY:1:STARTROOM", "1")
    sr.set("regions:1:portals:3:ENTRY:1:DIRECTION", "East")
    sr.set("regions:1:portals:3:ENTRY:1:DESTROOM", "4")
    sr.set("regions:1:portals:3:ENTRY:2:STARTROOM", "4")
    sr.set("regions:1:portals:3:ENTRY:2:DIRECTION", "West")
    sr.set("regions:1:portals:3:ENTRY:2:DESTROOM", "1")     
    
    sr.set("regions:1:portals:4:REGION", "1")
    sr.set("regions:1:portals:4:NAME", "Avenue")
    sr.set("regions:1:portals:4:DESCRIPTION", "This is a cobbled stone pathway.")
    sr.rpush("regions:1:portals:4:ENTRY", 1)
    sr.rpush("regions:1:portals:4:ENTRY", 2)
    sr.set("regions:1:portals:4:ENTRY:1:STARTROOM", "1")
    sr.set("regions:1:portals:4:ENTRY:1:DIRECTION", "West")
    sr.set("regions:1:portals:4:ENTRY:1:DESTROOM", "5")
    sr.set("regions:1:portals:4:ENTRY:2:STARTROOM", "5")
    sr.set("regions:1:portals:4:ENTRY:2:DIRECTION", "East")
    sr.set("regions:1:portals:4:ENTRY:2:DESTROOM", "1")  
    
    sr.set("regions:1:portals:5:REGION", "1")
    sr.set("regions:1:portals:5:NAME", "Magicians Door")
    sr.set("regions:1:portals:5:DESCRIPTION", "A simple wooden doorway.")
    sr.rpush("regions:1:portals:5:ENTRY", 1)
    sr.rpush("regions:1:portals:5:ENTRY", 2)
    sr.set("regions:1:portals:5:ENTRY:1:STARTROOM", "5")
    sr.set("regions:1:portals:5:ENTRY:1:DIRECTION", "South")
    sr.set("regions:1:portals:5:ENTRY:1:DESTROOM", "6")
    sr.set("regions:1:portals:5:ENTRY:2:STARTROOM", "6")
    sr.set("regions:1:portals:5:ENTRY:2:DIRECTION", "North")
    sr.set("regions:1:portals:5:ENTRY:2:DESTROOM", "5")     
    
    sr.set("regions:2:portals:100:REGION", "2")
    sr.set("regions:2:portals:100:NAME", "Mine Entrance")
    sr.set("regions:2:portals:100:DESCRIPTION", "Entrance to the Dwarven Mines")
    sr.rpush("regions:2:portals:100:ENTRY", 1)
    sr.rpush("regions:2:portals:100:ENTRY", 2)
    sr.set("regions:2:portals:100:ENTRY:1:STARTROOM", "2")
    sr.set("regions:2:portals:100:ENTRY:1:DIRECTION", "North")
    sr.set("regions:2:portals:100:ENTRY:1:DESTROOM", "100")
    sr.set("regions:2:portals:100:ENTRY:2:STARTROOM", "100")
    sr.set("regions:2:portals:100:ENTRY:2:DIRECTION", "South")
    sr.set("regions:2:portals:100:ENTRY:2:DESTROOM", "2")      
    
def AddRegionRoomsDetail():
    sr.set("regions:1:rooms:1:REGION", "1")
    sr.set("regions:1:rooms:1:NAME", "Betterton Town Square")
    sr.set("regions:1:rooms:1:DESCRIPTION", "You are in the town square of Betterton, a small city in the realm of BetterMUD.")   
    
    sr.set("regions:1:rooms:2:REGION", "1")
    sr.set("regions:1:rooms:2:NAME", "Betterton Town Gardens")
    sr.set("regions:1:rooms:2:DESCRIPTION", "You are in the gardens of Betterton, where you can see much <#FFFF00>flora<$reset> and <#00FF00>fauna<$reset> all around.")   
    
    sr.set("regions:1:rooms:3:REGION", "1")
    sr.set("regions:1:rooms:3:NAME", "Betterton Town Hall")
    sr.set("regions:1:rooms:3:DESCRIPTION", "You are in the Town Hall of Betterton, where the business of the city is conducted.")   
    
    sr.set("regions:1:rooms:4:REGION", "1")
    sr.set("regions:1:rooms:4:NAME", "Bakery")
    sr.set("regions:1:rooms:4:DESCRIPTION", "You are in the Bakery of Betterton, where you can see <#FFFF00>PIES<$reset> being made!")   
    
    sr.set("regions:1:rooms:5:REGION", "1")
    sr.set("regions:1:rooms:5:NAME", "Avenue")
    sr.set("regions:1:rooms:5:DESCRIPTION", "You are on the main Avenue of Betterton. You can see the street stretching off to the distance in an east-west direction.")   
    
    sr.set("regions:1:rooms:6:REGION", "1")
    sr.set("regions:1:rooms:6:NAME", "Magicians Shop")
    sr.set("regions:1:rooms:6:DESCRIPTION", "This is the Magicians Shop of Betterton, where you can buy all sorts of magical potions, baubles, and artifacts.")
    
    sr.set("regions:2:rooms:100:REGION", "2")
    sr.set("regions:2:rooms:100:NAME", "Dwarven Mine Entrance")
    sr.set("regions:2:rooms:100:DESCRIPTION", "You are at the entrance of the <#FFFFFF>Dwarven Mines<$reset>, an ancient collection of tunnels leading throughout Mount Worthington.") 

def AddCommandsDetail():
    sr.rpush("commands", "../data/commands/usercommands.py")
    sr.rpush("commands", "../data/commands/actions.py")
    sr.rpush("commands", "../data/commands/directions.py")
    sr.rpush("commands", "../data/commands/admincommands.py")
    sr.rpush("commands", "../data/commands/spells.py")
    
def AddLogicsDetail():
    sr.rpush("logics", "../data/logics/characters/pielogic.py")
    sr.rpush("logics", "../data/logics/characters/testing.py")
    sr.rpush("logics", "../data/logics/characters/itemstuff.py")
    sr.rpush("logics", "../data/logics/characters/bettertonstores.py")
    sr.rpush("logics", "../data/logics/characters/currency.py")
    sr.rpush("logics", "../data/logics/characters/combat.py")
    sr.rpush("logics", "../data/logics/items/basicitems.py")
    sr.rpush("logics", "../data/logics/items/spellitems.py")
    sr.rpush("logics", "../data/logics/regions/noelves.py")
    sr.rpush("logics", "../data/logics/rooms/pieroom.py")


#CreateCharactersList()
#AddCharactersDetail()
#CreateItemsList()
#AddItemsDetail()
#CreateRegionsList()
#AddRegionsDetail()
#AddRegionCharactersDetail()
#AddRegionItemsDetail()
#AddRegionPortalsDetail()
#AddRegionRoomsDetail()
#AddCommandsDetail()
AddLogicsDetail()

