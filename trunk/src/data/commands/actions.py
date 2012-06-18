from data.commands.PythonCommand import Command, UsageError
from accessors.CharacterAccessor import character
from accessors.RoomAccessor import room

class action( Command ):
    name = "action"
    usage = "\"action <verb phrase>\""
    description = "This executes a superflous action that doesn't affect game logic."

    def Run( self, args ):
        if not args: raise UsageError
        c = character( self.me )
        self.mud.AddActionAbsolute( 0, "announce", "0", "0", "0", "0", "<#FFFF00>" + c.GetName() + " " + args )


class pies( Command ):
    name = "pies"
    usage = "\"pies <|character>\""
    description = "Silly action"
    def Run( self, args ):
        me = character( self.me )
        r = room( me.GetRoom() )

        # find the name:
        if not args:
            name = "himself"
        else:
            r.SeekCharacter( args )
            if not r.IsValidCharacter():
                me.DoAction( "error", "0", "0", "0", "0", "Cannot find character: " + args )
                return
            id1 = r.CurrentCharacter()
            c = character( id1 )
            name = c.GetName()

        self.mud.AddActionAbsolute( 0, "vision", r.GetId(), "0", "0", "0", "<#00FF00>OMG!!! " + me.GetName() + " just threw a huge <#FFFF00>CUSTARD PIE<#00FF00> at " + name + "!!!!" )



