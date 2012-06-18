from accessors.GameAccessor import GameWrap
from accessors.ItemAccessor import item, itemtemplate
from accessors.CharacterAccessor import character, charactertemplate

def init():
    mud = GameWrap()

    # add arms to every item
    mud.BeginItem()
    while mud.IsValidItem():
        item = item( mud.CurrentItem() )
        template = itemtemplate( item.GetTemplateId() )
        if not item.HasAttribute( "arms" ):
            item.AddAttribute( "arms", template.GetAttribute( "arms" ) )
        mud.NextItem()

    # add defaultweapon and weapon to every character
    mud.BeginCharacter()
    while mud.IsValidCharacter():
        character = character( mud.CurrentCharacter() )
        template = charactertemplate( character.GetTemplateId() )
        if not character.HasAttribute( "defaultweapon" ):
            character.AddAttribute( "defaultweapon", template.GetAttribute( "defaultweapon" ) )
        if not character.HasAttribute( "weapon" ):
            character.AddAttribute( "weapon", template.GetAttribute( "weapon" ) )
        mud.NextCharacter()