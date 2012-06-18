from accessors.CharacterAccessor import character
from data.logics.logic import logic

class noelves( logic ):
    def Run( self, action, arg1, arg2, arg3, arg4, data ):
        if action == "canenterregion":
            character1 = character( arg1 )
            if character1.GetTemplateId() == "2":
                character1.SeekItem( "Dwarven Mine Pass" )
                if character1.IsValidItem():
                    return 0
                character1.DoAction( "error", "0", "0", "0", "0", "As an elf, you are morally obligated to not enter these mines!" )
                return 1