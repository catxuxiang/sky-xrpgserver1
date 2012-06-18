from accessors.GameAccessor import GameWrap

class bettermudscript:

    # Initialize the script with an ID
    def Init( self, id1 ):
        self.me = id1
        self.mud = GameWrap()
        self.ScriptInit()

    def ScriptInit( self ):
        pass

    def GetName( self ):
        return self.name

    def LoadScript( self, s ):
        pass

    def SaveScript( self ):
        return ""