'''
Created on Feb 16, 2014

@author: Steven
'''

class NetDefs():
    '''
    Generic network connection class.  Allows for standard calls for both TCP and
    UDP.  Takes a server and port from the superclass, provides constructors for 
    both TCP and UDP (calling the superclass constructor) and then implements
    the standard inteface.  The connect and close are essentially no-op methods
    for UDP.
    '''

    def __init__(self, server='localhost', port=80):
        '''
        Constructor
        '''
        self.server = server
        self.port = port
        self.connection = ''
        
    def connect(self):
        pass
    
    def read(self):
        pass
    
    def write(self):
        pass
    
    def close(self):
        pass
    
    def listen(self):
        pass

class Tcp(NetDefs): 
    def __init__(self, server='localhost', port=80): 
        NetDefs.__init__(self, server, port)
        from socket import AF_INET 
        from socket import SOCK_STREAM
        from socket import socket
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
         
    def connect(self):
        self.connection = self.clientSocket.connect((self.server, self.port))
        return(self.clientSocket.recv(1024))
    
    def read(self):
        return(self.clientSocket.recv(1024))
    
    def write(self, message=''):
        self.clientSocket.send(message)
        return
    
    def close(self):
        self.clientSocket.close()
        
    def listen(self):
        self.clientSocket.bind(('',self.port))
        self.clientSocket.listen(1)
        return

class Udp(NetDefs):
    def __init__(self, server='localhost', port=80): 
        NetDefs.__init__(self, server, port)
        from socket import AF_INET, SOCK_DGRAM, socket
        self.clientSocket = socket(AF_INET, SOCK_DGRAM)
        self.serverAddress = ''
   
    def read(self, timeout=None):
        self.clientSocket.settimeout(timeout)
        message, self.serverAddress = self.clientSocket.recvfrom(2048)
        return(message)
    
    def write(self, message=''):
        self.clientSocket.sendto(message,(self.server, self.port))
        return
    
    def listen(self):       
        self.clientSocket.bind(('',self.port))
        return