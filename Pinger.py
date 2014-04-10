'''
Created on Apr 5, 2014

@author: stnel
'''

class Pinger:
    '''
    Defines the methods for both establishing the client and server side of 
    the UDP pinger test.  This allows for management of the methods in a single
    spot.
    '''
    
    def __init__(self, port=80):
        '''
        Constructor for Pinger
        Build out the settings to change if necessary.  Define the port to use
        for any operation that instantiates this class.  We also define
        a 'kill' string for the server to use so that it will shutdown 
        *relatively* gracefully.
        '''
        # Import the regex for the compile of the pattern to match for the
        # kill string
        from re import compile
        
        # Set the params...
        self.LOSS_RATE = 0.3
        self.AVERAGE_DELAY = 100
        
        # Set the connection port for this instantiation
        self.port = port
        
        # Define the kill string
        self.killerPattern = compile('KILL')
        return
    
    def PingServer(self):
        '''
        PingServer - start a UDP server to listen on a specified port for 'ping'
        messages. Assumes a message input standard of:
        
        PING <seq no.> <client orig time> CRLF
        
        Returns message in format of:
        
        PING <client seq no.> <client orig time> <server reply time> CRLF
        
        PingServer simulates pseudo-random packet loss (via LOSS_RATE) and 
        randomized process/transmit delay (via AVERAGE_DELAY) for the packet
        '''
        
        # Import the classes/modules
        from NetDefs import Udp
        from random import random
        from re import match
        from time import sleep
        from Generic import Generic

        # Loop forever...or there about...
        while(True):
            # Establish the listener locally
            connection = Udp(port = self.port)
            connection.listen()
            
            # Generate a random number to simulate packet loss
            simulate_loss = random()
            
            # Read the port
            recvStr = connection.read()
            print('Got message ' + recvStr.rstrip('\n') + ' from ' + connection.serverAddress[0])
            
            # if the message matches exactly the kill string stop the server
            if(match(self.killerPattern,recvStr)):
                break
            
            # If the simulated loss is below the LOSS_RATE, drop
            if(simulate_loss < self.LOSS_RATE):
                print('Dropping packet (on purpose)')
                print('\tDropped packet contained: ' + recvStr.rstrip('\n'))
                print('\tDropped packet was from: ' + connection.serverAddress[0] + '\n')
                continue
            
            # Sleep to simulate network delay
            print('Sleeping for ' + str(((2*simulate_loss)*self.AVERAGE_DELAY)/1000) + ' sec')
            sleep(((2*simulate_loss)*self.AVERAGE_DELAY)/1000)
            # Instantiate a generic instance for all methods
            g = Generic()
            
            # Strip off the CRLF from the inbound
            sndStr = recvStr.rstrip('\n')
            
            # Write the original data back to the pinger
            # Need to set up the connection information from the received 
            # packet
            connection.server = connection.serverAddress[0]
            connection.port = connection.serverAddress[1]
            connection.write(sndStr +  ' ' + g.timeStamp() + '\n')
            
            # Notify that message was sent back
            print('Reply sent to ' + connection.serverAddress[0] + '\n')
            
        # Return if the request to kill the server is received
        return
            
    def PingClient(self, server, message):
        '''
        PingClient - Client portion of PingServer
        Sends a standardized message to the PingServer and deals with 
        dropped packets as defined by the timeout value passed to NetDefs
        (my standard network connection module).
        
        Right now, the connection timeout is set to 1 second...
        
        '''
        # Import the required classes
        from NetDefs import Udp
        from socket import timeout
        
        # Build the connection and write the message passed
        connection = Udp(server = server, port = self.port)
        connection.write(message)
        
        # Try to read from the socket after we send a message
        # capture the timeout exception and handle.
        try:
            retMsg = connection.read(1.0)
        except timeout:
            retMsg = 'TIMEOUT: No return received'
        
        # Return any message received.  
        return(retMsg)