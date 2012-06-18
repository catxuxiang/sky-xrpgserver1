from accessors.CharacterAccessor import character
from accessors.ItemAccessor import item
from data.logics.logic import logic

class cantget( logic ):

    def Run( self, action, arg1, arg2, arg3, arg4, data ):
        if action == "cangetitem":
            c = character( arg1 )
            me = item( arg2 )
            self.mud.AddActionAbsolute( 0, "vision", c.GetRoom(), "0", "0", "0", c.GetName() + " almost has a hernia, trying to pull " + me.GetName() + " out of the ground!" )
            return 1




class uberweight( logic ):

    def Run( self, action, arg1, arg2, arg3, arg4, data ):
        if action == "cangetitem":
            c = character( arg1 )
            me = item( arg2 )
            self.mud.AddActionAbsolute( 0, "vision", c.GetRoom(), "0", "0", "0", c.GetName() + " struggles like a madman trying to pull " + me.GetName() + " off the ground, but it's stuck!" )
            return 1

        if action == "messagelogic":
            if data == "uberweight remove":
                self.mud.AddActionAbsolute( 0, "dellogic", 1, self.me, "0", "0", "uberweight" )
                me = item( self.me )
                self.mud.AddActionAbsolute( 0, "vision", me.GetRoom(), "0", "0", "0", "The uberweight on " + me.GetName() + " wears off!" )



class canread( logic ):
    def Run( self, action, arg1, arg2, arg3, arg4, data ):
        if action == "query" and data == "canread":
            return 1