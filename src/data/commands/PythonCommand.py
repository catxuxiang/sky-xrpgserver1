from data.bettermudscript import bettermudscript
from accessors.CharacterAccessor import character

class UsageError(Exception):
    pass

class TargetError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


def FindTarget( seekf, validf, getf, name ):
    seekf( name )
    if not validf(): raise TargetError( name )
    return getf()


class Command( bettermudscript ):

    # Usage
    def GetUsage( self ):
        return self.usage

    # description
    def GetDescription( self ):
        return self.description

    # the standard call method.
    def Execute( self, args ):
        try:
            self.Run( args )
        except UsageError:
            me = character( self.me )
            me.DoAction( "error", "0", "0", "0", "0", "Usage: " + self.GetUsage() )
        except TargetError as e:
            me = character( self.me )
            me.DoAction( "error", "0", "0", "0", "0", "Cannot find: " + e.value )



            