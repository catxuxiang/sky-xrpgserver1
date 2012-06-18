from data.logics.logic import logic
from accessors.CharacterAccessor import character
from accessors.ItemAccessor import item



class spellscroll( logic ):
    def DoRead( self, character1, item1, name ):
        c = character( character1 )
        i = item( item1 )
        if c.HasCommand( name ):
            c.DoAction( "error", "0", "0", "0", "0", "You already know this spell!" )
            return

        c.AddCommand( name )
        self.mud.AddActionAbsolute( 0, "vision", c.GetRoom(), "0", "0", "0", c.GetName() + " reads " + i.GetName() + "!" )
        self.mud.AddActionAbsolute( 1, "destroyitem", i.GetId(), "0", "0", "0", "" )
        c.DoAction( "announce", "0", "0", "0", "0", "You now know the spell " + name + "!" )
        c.DoAction( "announce", "0", "0", "0", "0", "The " + i.GetName() + " disappears in a bright flash of flame!" )


class uberweightscroll( spellscroll ):
    def Run( self, action, arg1, arg2, arg3, arg4, data ):
        if action == "do" and data == "read":
            self.DoRead( arg3, self.me, "uberweight" )
            return
