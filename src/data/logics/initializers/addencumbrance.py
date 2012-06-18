from accessors.GameAccessor import GameWrap
from accessors.ItemAccessor import item, itemtemplate
from accessors.CharacterAccessor import character, charactertemplate

def init():
    mud = GameWrap()

    # add weight to every item
    mud.BeginItem()
    while mud.IsValidItem():
        item = item( mud.CurrentItem() )
        template = itemtemplate( item.GetTemplateId() )
        if not item.HasAttribute( "weight" ):
            item.AddAttribute( "weight", template.GetAttribute( "weight" ) )
        mud.NextItem()

    # add encumbrance to every character
    mud.BeginCharacter()
    while mud.IsValidCharacter():
        character = character( mud.CurrentCharacter() )
        template = charactertemplate( character.GetTemplateId() )
        if not character.HasAttribute( "encumbrance" ):
            character.AddAttribute( "encumbrance", template.GetAttribute( "encumbrance" ) )
        if not character.HasAttribute( "maxencumbrance" ):
            character.AddAttribute( "maxencumbrance", template.GetAttribute( "maxencumbrance" ) )

        # now calculate encumbrance of carried items
        character.BeginItem()
        encumbrance = 0
        while character.IsValidItem():
            item = item( character.CurrentItem() )
            if item.IsQuantity():
                encumbrance = encumbrance + item.GetAttribute( "weight" ) * item.GetQuantity()
            else:
                encumbrance = encumbrance + item.GetAttribute( "weight" )
            character.NextItem()
        character.SetAttribute( "encumbrance", encumbrance )
        if not character.HasLogic( "encumbrance" ):
            character.AddLogic( "encumbrance" )
        mud.NextCharacter()