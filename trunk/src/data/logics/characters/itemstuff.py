from accessors.CharacterAccessor import character
from accessors.ItemAccessor import item
from data.logics.logic import logic

class cantreceiveitems( logic ):
    def Run( self, action, arg1, arg2, arg3, arg4, data ):
        if action == "canreceiveitem":
            g = character( arg1 )
            if not g.IsPlayer(): return 0     # accept stuff from NPC's with the implcit promise that they aren't malicious
            i = item( arg3 )
            me = character( self.me )
            me.DoAction( "error", "0", "0", "0", "0", g.GetName() + " tried to give you " + i.GetName() + " but you have item receiving turned off. Type \"/receive on\" to turn receiving back on." )
            g.DoAction( "error", "0", "0", "0", "0", me.GetName() + " refuses to take " + i.GetName() + "!" )
            return 1

class encumbrance( logic ):
    def Weight( self, i, q ):
        item1 = item( i )
        if item1.IsQuantity():
            return int(q) * int(item1.GetAttribute( "weight" ))
        else:
            return int(item1.GetAttribute( "weight" ))

    def Run( self, action, arg1, arg2, arg3, arg4, data ):
        me = character( self.me )

        if action == "canleaveroom":
            if int(me.GetAttribute( "encumbrance" )) > int(me.GetAttribute( "maxencumbrance" )):
                me.DoAction( "error", "0", "0", "0", "0", "You cannot move! You're too heavy! Drop something first!" )
                return 1
            return 0

        if action == "getitem":
            if arg1 == self.me:
                item1 = item( arg2 )
                weight = self.Weight( arg2, arg3 )
                me.SetAttribute( "encumbrance", int(me.GetAttribute( "encumbrance" )) + weight )
            return 0

        if action == "dropitem":
            if arg1 == self.me:
                item1 = item( arg2 )
                weight = self.Weight( arg2, arg3 )
                me.SetAttribute( "encumbrance", int(me.GetAttribute( "encumbrance" )) - weight )
            return 0

        if action == "destroyitem":
            item1 = item( arg1 )
            weight = self.Weight( arg1, item1.GetQuantity() )
            me.SetAttribute( "encumbrance", int(me.GetAttribute( "encumbrance" )) - weight )
            return 0

        if action == "giveitem":
            if arg1 == self.me:
                item1 = item( arg3 )
                weight = self.Weight( arg3, arg4 )
                me.SetAttribute( "encumbrance", int(me.GetAttribute( "encumbrance" )) - weight )
            if arg2 == self.me:
                item1 = item( arg3 )
                weight = self.Weight( arg3, arg4 )
                me.SetAttribute( "encumbrance", int(me.GetAttribute( "encumbrance" )) + weight )
            return 0

        if action == "spawnitem":
            item1 = item( arg1 )
            weight = self.Weight( arg1, item1.GetQuantity() )
            me.SetAttribute( "encumbrance", int(me.GetAttribute( "encumbrance" )) + weight )
            return 0

        if action == "cangetitem":
            item1 = item( arg2 )
            weight = self.Weight( arg2, arg3 )
            if weight + int(me.GetAttribute( "encumbrance" )) > int(me.GetAttribute( "maxencumbrance" )):
                me.DoAction( "error", "0", "0", "0", "0", "You can't pick up " + item1.GetName() + " because it's too heavy for you to carry!" )
                return 1
            return 0

        if action == "canreceiveitem":
            g = character( arg1 )
            item1 = item( arg3 )
            weight = self.Weight( arg3, arg4 )
            if weight + int(me.GetAttribute( "encumbrance" )) > int(me.GetAttribute( "maxencumbrance" )):
                me.DoAction( "error", "0", "0", "0", "0", g.GetName() + " tried to give you " + item1.GetName() + " but it's too heavy for you to carry!" )
                g.DoAction( "error", "0", "0", "0", "0", "You can't give " + me.GetName() + " the " + item1.GetName() + " because it is too heavy!" )
                return 1
            return 0




class armaments( logic ):

    def Disarm( self, itemtype ):
        if itemtype == 1:
            me = character( self.me )
            if me.GetAttribute( "weapon" ) != "0":
                weapon = item( me.GetAttribute( "weapon" ) )
                me.SetAttribute( "weapon", "0" )
                self.mud.AddActionAbsolute( 0, "vision", me.GetRoom(), "0", "0", "0", me.GetName() + " disarms " + weapon.GetName() + "." )

    def Arm( self, item1 ):
        me = character( self.me )
        if item1.GetAttribute( "arms" ) == "1":
            me.SetAttribute( "weapon", item1.GetId() )
            self.mud.AddActionAbsolute( 0, "vision", me.GetRoom(), "0", "0", "0", me.GetName() + " arms " + item1.GetName() + "!" )

    def Lose( self, me, itemid ):
        if me.GetAttribute( "weapon" ) == itemid:
            self.Disarm( 1 )


    def Run( self, action, arg1, arg2, arg3, arg4, data ):
        me = character( self.me )
        if action == "query" and data == "canarm":
            item1 = item( arg1 )
            if item1.GetAttribute( "arms" ) == "1":
                return 1
            return 0

        if action == "do" and data == "arm":
            item1 = item( arg3 )
            self.Disarm( 1 )
            self.Arm( item1 )

        if action == "do" and data == "disarm":
            self.Disarm( arg3 )

        if action == "dropitem" and arg1 == me.GetId():
            self.Lose( me, arg2 )

        if action == "giveitem" and arg1 == me.GetId():
            self.Lose( me, arg3 )

        if action == "destroyitem":
            self.Lose( me, arg1 )
            