from accessors.CharacterAccessor import character
from accessors.ItemAccessor import item
from data.logics.logic import logic

class pies( logic ):
    def Run( self, action, arg1, arg2, arg3, arg4, data ):
        me = character( self.me )
        if action == "say" and data.find( "pies" ) != -1 and arg1 != me.GetId():
            c = character( arg1 )
            self.mud.AddActionAbsolute( 0, "attemptsay", me.GetId(), "0", "0", "0", c.GetName() + ": YES!!! PIES!!!!!" )

        return 0


class glarepie( logic ):
    def Run( self, action, arg1, arg2, arg3, arg4, data ):
        if action == "getitem":
            item1 = item( arg2 )
            if item1.GetTemplateId() == "2":
                self.mud.AddActionAbsolute( 0, "attemptsay", self.me, "0", "0", "0", "Hey!!!! Thos-a Pies aren't-a FREE!" )

        return 0
