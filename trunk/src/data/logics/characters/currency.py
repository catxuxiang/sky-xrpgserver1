from accessors.CharacterAccessor import character
from accessors.ItemAccessor import item, itemtemplate
from accessors.GameAccessor import GameWrap
from data.logics.logic import logic

def HasEnoughCurrency( character1, amount ):
    total = 0
    character1.BeginItem()
    while character1.IsValidItem():
        item1 = item( character1.CurrentItem() )
        if item1.GetTemplateId() == "1":   # copper pieces
            total = total + item1.GetQuantity()
        character1.NextItem()

    if total >= amount:
        return True
    return False



def GiveCurrency( character1, recipient, amount ):
    character1.BeginItem()
    mud = GameWrap()
    while character1.IsValidItem():
        item = item( character1.CurrentItem() )
        if item.GetTemplateId() == "1":   # copper pieces
            mud.DoAction( "attemptgiveitem", character1.GetId(), recipient.GetId(), item.GetId(), amount, "" )
            return
        character1.NextItem()


def FindName( classtype, list1, search ):
    newsearch = search.lower()
    for x in list1:
        item = classtype( x )
        if item.GetName().lower() == newsearch:
            return x

    for x in list1:
        item = classtype( x )
        name = item.GetName().lower()
        if name.find( newsearch ) == 0 or name.find( " " + newsearch ) != -1:
            return x

    return False


class merchant( logic ):
    def Run( self, action, arg1, arg2, arg3, arg4, data ):
        me = character( self.me )

        if action == "do" and data == "list":
            character1 = character( arg3 )
            character1.DoAction( "announce", "0", "0", "0", "0", "<#7F7F7F>--------------------------------------------------------------------------------" )
            character1.DoAction( "announce", "0", "0", "0", "0", "<#FFFFFF> Item                                      | Cost" )
            character1.DoAction( "announce", "0", "0", "0", "0", "<#7F7F7F>--------------------------------------------------------------------------------" )
            for x in self.iteminventory:
                item = itemtemplate( x )
                character1.DoAction( "announce", "0", "0", "0", "0", "<#7F7F7F> " + item.GetName().ljust( 42 ) + "| " + str( item.GetAttribute( "value" ) ) )
            character1.DoAction( "announce", "0", "0", "0", "0", "<#7F7F7F>--------------------------------------------------------------------------------" )
            return

        if action == "do" and data[:3] == "buy":
            itemname = data.split( None, 1 )
            itemname = itemname[1]
            character1 = character( arg3 )
            id1 = FindName( itemtemplate, self.iteminventory, itemname )
            if id1 == "0":
                character1.DoAction( "announce", "0", "0", "0", "0", "Sorry, you can't buy " + itemname + "here!" )
                return

            t = itemtemplate( id1 )
            if not HasEnoughCurrency( character1, int(t.GetAttribute( "value" )) ):
                character1.DoAction( "announce", "0", "0", "0", "0", "Sorry, you don't have enough money to buy " + t.GetName() + "!" )
                return

            GiveCurrency( character1, me, t.GetAttribute( "value" ) )
            self.mud.DoAction( "spawnitem", id1, character1.GetId(), "1", "0", "" )
            self.mud.AddActionAbsolute( 0, "vision", character1.GetRoom(), "0", "0", "0", character1.GetName() + " buys " + t.GetName() + "." )



                