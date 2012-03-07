import Rcon
import re

class Server:
    def __init__( self, address, port, password ):
        self.address = address
        self.port = port
        self.password = password
        self._rcon = Rcon.Rcon(address, port, password)

    def HasPlayers( self ):
        statusText = self.Status()

        match = re.search("(\d+) humans?", statusText)

        if match == None:
            return True
        elif int(match.group(1)) == 0:
            return False

        return True

    def Status( self ):
        return self.Rcon("status")

    def Rcon( self, command ):
        self._rcon.RunCommand(command)
        return self._rcon.response
