from data.commands.PythonCommand import Command, UsageError, FindTarget
from accessors.CharacterAccessor import character
from accessors.RoomAccessor import room
from accessors.ItemAccessor import itemtemplate, item
from accessors.CharacterAccessor import charactertemplate
from accessors.RegionAccessor import region

class visual( Command ):
    name = "visual"
    usage = "\"visual <vision>\""
    description = "shows some text in a room"

    def Run( self, args ):
        if not args: raise UsageError
        me = character( self.me )
        self.mud.AddActionAbsolute( 0, "vision", me.GetRoom(), "0", "0", "0", args )


class addcommand( Command ):
    name = "addcommand"
    usage = "\"addcommand <player> <commandname>\""
    description = "This gives a character the ability to use a new command."

    def Run( self, args ):
        if not args: raise UsageError
        parms = args.split( None, 1 )
        if len(parms) < 2: raise UsageError
        me = character( self.me )
        id1 = self.mud.FindPlayerPart( parms[0] )
        if not id1:
            me.DoAction( "error", "0", "0", "0", "0", "Cannot find player: " + parms[0] )
            return
        r = character( id1 )
        if not r.AddCommand( parms[1] ):
            me.DoAction( "error", "0", "0", "0", "0", "Could not add command: " + parms[1] )
            return
        me.DoAction( "announce", "0", "0", "0", "0", "Successfully gave " + r.GetName() + " command " + parms[1] + "." )
        r.DoAction( "announce", "0", "0", "0", "0", me.GetName() + " gave you a new command: " + parms[1] + "!" )


class delcommand( Command ):
    name = "delcommand"
    usage = "\"delcommand <player> <commandname>\""
    description = "This removes a command from a character."

    def Run( self, args ):
        if not args: raise UsageError
        parms = args.split( None, 1 )
        if len(parms) < 2: raise UsageError
        me = character( self.me )
        id1 = self.mud.FindPlayerPart( parms[0] )
        if not id1:
            me.DoAction( "error", "0", "0", "0", "0", "Cannot find player: " + parms[0] )
            return
        t = character( id1 )
        if not t.DelCommand( parms[1] ):
            me.DoAction( "error", "0", "0", "0", "0", "Could not delete command: " + parms[1] )
            return
        me.DoAction( "announce", "0", "0", "0", "0", "Successfully removed " + t.GetName() + "s command " + parms[1] + "." )
        t.DoAction( "announce", "0", "0", "0", "0", me.GetName() + " deleted your command: " + parms[1] + "!" )


class emulate( Command ):
    name = "emulate"
    usage = "\"emulate <player> <text>\""
    description = "This tells the game to pretend that <player> typed in <text>"

    def Run( self, args ):
        if not args: raise UsageError
        parms = args.split( None, 1 )
        if len(parms) < 2: raise UsageError
        me = character( self.me )
        id1 = self.mud.FindPlayerOnlinePart( parms[0] )
        if not id1:
            me.DoAction( "error", "0", "0", "0", "0", "Cannot find player: " + parms[0] )
            return
        c = character( id1 )
        self.mud.AddActionAbsolute( 0, "command", c.GetId(), "0", "0", "0", parms[1] )


class addplayerlogic( Command ):
    name = "addplayerlogic"
    usage = "\"addplayerlogic <character> <logicname>\""
    description = "This adds a logic module to a player."

    def Run( self, args ):
        if not args: raise UsageError
        parms = args.split( None, 1 )
        if len(parms) < 2: raise UsageError
        me = character( self.me )
        
        r = room( me.GetRoom() )
        c = character( FindTarget( r.SeekCharacter, r.IsValidCharacter, r.CurrentCharacter, parms[0] ) )        
        #id1 = self.mud.FindPlayerPart( parms[0] )
        if not c:
            me.DoAction( "error", "0", "0", "0", "0", "Cannot find character: " + parms[0] )
            return
        #c = character( m )
        if not c.AddLogic( parms[1] ):
            me.DoAction( "error", "0", "0", "0", "0", "Could not add logic: " + parms[1] )
            return
        me.DoAction( "announce", "0", "0", "0", "0", "Successfully gave " + c.GetName() + " logic module " + parms[1] + "." )
        c.DoAction( "announce", "0", "0", "0", "0", me.GetName() + " gave you a new logic module: " + parms[1] + "!" )


class delplayerlogic( Command ):
    name = "delplayerlogic"
    usage = "\"delplayerlogic <player> <logicname>\""
    description = "This removes a logic module from a player"

    def Run( self, args ):
        if not args: raise UsageError
        parms = args.split( None, 1 )
        if len(parms) < 2: raise UsageError
        id1 = self.mud.FindPlayerPart( parms[0] )
        me = character( self.me )

        if not id1:
            me.DoAction( "error", "0", "0", "0", "0", "Cannot find player: " + parms[0] )
            return
        c = character( id1 )
        if not c.DelLogic( parms[1] ):
            me.DoAction( "error", "0", "0", "0", "0", "Could not delete logic: " + parms[1] )
            return
        me.DoAction( "announce", "0", "0", "0", "0", "Successfully removed " + c.GetName() + "s logic module " + parms[1] + "." )
        c.DoAction( "announce", "0", "0", "0", "0", me.GetName() + " deleted your logic module: " + parms[1] + "!" )


class pythonexec( Command ):
    name = "pythonexec"
    usage = "\"pythonexec <code>\""
    description = "Executes some Python code"

    def Run( self, args ):
        if not args: raise UsageError
        me = character( self.me )
        s = args.replace( "<br>", "\n" )
        me.DoAction( "announce", "0", "0", "0", "0", "Executing Python Code, check your console window." )
        exec( s )


class spawnitem( Command ):
    name = "spawnitem"
    usage = "\"spawnitem <item template id>\""
    description = "Spawns a new item in your inventory"

    def Run( self, args ):
        if not args: raise UsageError

        me = character( self.me )
        t = itemtemplate( args )
        #print(t.GetId())
        me.DoAction( "announce", "0", "0", "0", "0", "Spawning Item..." )
        self.mud.DoAction( "spawnitem", t.GetId(), me.GetId(), "1", "0", "" )
        me.DoAction( "announce", "0", "0", "0", "0", "Success." )


class spawncharacter( Command ):
    name = "spawncharacter"
    usage = "\"spawncharacter <character template id>\""
    description = "Spawns a new character in your room"

    def Run( self, args ):
        if not args: raise UsageError
        me = character( self.me )
        t = charactertemplate( args )
        me.DoAction( "announce", "0", "0", "0", "0", "Spawning Character..." )
        self.mud.DoAction( "spawncharacter", t.GetId(), me.GetRoom(), "0", "0", "" )
        me.DoAction( "announce", "0", "0", "0", "0", "Success." )


class teleport( Command ):
    name = "teleport"
    usage = "\"teleport <room id>\""
    description = "Attempts to teleport you to a room"

    def Run( self, args ):
        if not args: raise UsageError
        me = character( self.me )
        #oldroom = me.GetRoom()
        self.mud.DoAction( "attempttransport", me.GetId(), args, "0", "0", "" )


class destroyitem( Command ):
    name = "destroyitem"
    usage = "\"destroyitem <item>\""
    description = "This destroys an item, searching your inventory first, then the room."

    def Run( self, args ):
        if not args: raise UsageError

        me = character( self.me )
        me.SeekItem( args )

        if me.IsValidItem():
            item1 = me.CurrentItem()
        else:
            room1 = room( me.GetRoom() )
            room1.SeekItem( args )
            if room1.IsValidItem():
                item1 = room1.CurrentItem()
            else:
                me.DoAction( "error", "0", "0", "0", "0", "Cannot find item: " + args )
                return

        i = item( item1 )
        me.DoAction( "announce", "0", "0", "0", "0", "Destroying Item: " + i.GetName() )
        self.mud.AddActionAbsolute( 0, "destroyitem", item1, "0", "0", "0", "" )


class destroycharacter( Command ):
    name = "destroycharacter"
    usage = "\"destroycharacter <item>\""
    description = "This destroys a character."

    def Run( self, args ):
        if not args: raise UsageError

        me = character( self.me )
        room1 = room( me.GetRoom() )
        room1.SeekCharacter( args )
        if room1.IsValidCharacter():
            character1 = room1.CurrentCharacter()
        else:
            me.DoAction( "error", "0", "0", "0", "0", "Cannot find character: " + args )
            return

        c = character( character1 )
        me.DoAction( "announce", "0", "0", "0", "0", "Destroying Character: " + c.GetName() )
        self.mud.AddActionAbsolute( 0, "destroycharacter", character1, "0", "0", "0", "" )


class cleanup( Command ):
    name = "cleanup"
    usage = "\"cleanup\""
    description = "Performs a manual database cleanup"

    def Run( self, args ):
        me = character( self.me )
        me.DoAction( "announce", "0", "0", "0", "0", "Beginning Cleanup" )
        self.mud.AddActionAbsolute( 0, "cleanup", "0", "0", "0", "0", "" )



class savedatabase( Command ):
    name = "savedatabase"
    usage = "\"savedatabase <all|region|players> <|regionid>\""
    description = "Performs a manual database save"

    def Run( self, args ):
        if not args: raise UsageError

        me = character( self.me )
        parms = args.split( None, 1 )
        if parms[0] == "all":
            me.DoAction( "announce", "0", "0", "0", "0", "Beginning Complete Database Save" )
            self.mud.AddActionAbsolute( 0, "savedatabases", "0", "0", "0", "0", "" )
            return
        if parms[0] == "region":
            if len(parms) < 2: raise UsageError
            region1 = region( parms[1] )
            me.DoAction( "announce", "0", "0", "0", "0", "Beginning Region Database Save: " + region1.GetName() )
            self.mud.AddActionAbsolute( 0, "saveregion", parms[1], "0", "0", "0", "" )
            return
        if parms[0] == "players":
            me.DoAction( "announce", "0", "0", "0", "0", "Beginning Player Database Save" )
            self.mud.AddActionAbsolute( 0, "saveplayers", "0", "0", "0", "0", "" )
            return
        raise UsageError



class loaddatabase( Command ):
    name = "loaddatabase"
    usage = "\"loaddatabase <items|characters|regions|commands|logics> <file name> <|keepdata|keepall>\""
    description = "Performs a manual database save"

    def Run( self, args ):
        if not args: raise UsageError

        me = character( self.me )
        parms = args.split( None )
        if len(parms) < 2: raise UsageError

        if parms[0] == "items":
            me.DoAction( "announce", "0", "0", "0", "0", "Beginning Item Template Database Load: " + parms[1] )
            self.mud.DoAction( "reloaditems", "0", "0", "0", "0", parms[1] )
            return
        if parms[0] == "characters":
            me.DoAction( "announce", "0", "0", "0", "0", "Beginning Character Template Database Load: " + parms[1] )
            self.mud.DoAction( "reloadcharacters", "0", "0", "0", "0", parms[1] )
            return
        if parms[0] == "regions":
            me.DoAction( "announce", "0", "0", "0", "0", "Beginning Region Database Load: " + parms[1] )
            self.mud.DoAction( "reloadregion", "0", "0", "0", "0", parms[1] )
            return
        if parms[0] == "commands":
            if len(parms) < 3: raise UsageError
            if parms[2] == "keepdata" : mode = 1
            elif parms[2] == "keepall" : mode = 0
            else : raise UsageError
            me.DoAction( "announce", mode, "0", "0", "0", "Beginning Command Database Load: " + parms[1] )
            self.mud.DoAction( "reloadcommandscript", mode, "0", "0", "0", parms[1] )
            return
        if parms[0] == "logics":
            if len(parms) < 3: raise UsageError
            if parms[2] == "keepdata" : mode = 1
            elif parms[2] == "keepall" : mode = 0
            else : raise UsageError
            me.DoAction( "announce", "0", "0", "0", "0", "Beginning Logic Database Load: " + parms[1] )
            self.mud.DoAction( "reloadlogicscript", mode, "0", "0", "0", parms[1] )
            return


        raise UsageError



class initialize( Command ):
    name = "initialize"
    usage = "\"initialize <script>\""
    description = "Performs an initialization using a script"

    def Run( self, args ):
        if not args: raise UsageError
        exec( "import data.logics.initializers." + args + "\nreload( data.logics.initializers." + args + " )\ndata.logics.initializers." + args + ".init()" )