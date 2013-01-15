import socket
import struct

class Rcon:
    DEFAULT_ID      = 20
    RESPONSE_AUTH   = 2
    RESPONSE_VALUE  = 0
    REQUEST_AUTH    = 3
    REQUEST_COMMAND = 2
    
    def __init__( self, address, port, password ):
        self.address = address
        self.port = int(port)
        self.password = password
        self.socket = None
        self.authed = False
        
    def _Connect( self ):
        self.authed = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.address, self.port))
        
    def _Disconnect( self ):
        self.authed = False
        self.socket.shutdown(0)
        self.socket.close()
        
    def _Send( self, id, command, str1, str2 ):
        packedSize = struct.pack('I', 10 + len(str1) + len(str2))
        self.socket.send(packedSize)
        
        packedId = struct.pack('I', id)
        self.socket.send(packedId)
        
        packedCommand = struct.pack('I', command)
        self.socket.send(packedCommand)
        
        self.socket.send(str1.encode("ascii"))
        self.socket.send(struct.pack('B', 0))
        
        self.socket.send(str2.encode("ascii"))
        self.socket.send(struct.pack('B', 0))
        
    def _Receive( self ):
        packedSize = self.socket.recv(4)
        size = struct.unpack('I', packedSize)[0]
        
        packedId = self.socket.recv(4)
        id = struct.unpack('I', packedId)[0]
        
        packedCommand = self.socket.recv(4)
        command = struct.unpack('I', packedCommand)[0]
        
        response = self.socket.recv(size-8)
        
        return self._ProcessResponse(size, id, command, response.decode("ascii"))
        
    def _ProcessResponse( self, size, id, command, response ):
        if command == Rcon.RESPONSE_AUTH:
            if id == Rcon.DEFAULT_ID:
                self.authed = True
                return True
            elif id == -1:
                print("Rcon authentication refused")
                return False
        elif command == Rcon.RESPONSE_VALUE:
            self.response = response
            return True
        
        print("Unexpected response from rcon: ", command)
        return False
        
    def RunCommand( self, command ):
        # Connect to the server
        self._Connect()
        
        # Send the authentication request
        self._Send(Rcon.DEFAULT_ID, Rcon.REQUEST_AUTH, self.password, "")
        
        # Wait for the authentication reply
        while (not self.authed):
            if not self._Receive():
                return False
        
        # Send the command
        self._Send(Rcon.DEFAULT_ID, Rcon.REQUEST_COMMAND, command, "")
        self._Receive()
        
        # Finish up
        self._Disconnect()
        
        return True
