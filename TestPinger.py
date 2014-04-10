#!/usr/bin/python
'''
Created on Apr 7, 2014

@author: stnel

TestPinger - Test the server/client UDP pinger.  
This will query to see if the user would like to start either a client or 
server process and ask for the port to listen/transmit on.  If a client is 
specified, then a target host is required as well as a number of pings to 
transmit.
'''

if __name__ == '__main__':
    pass

# Import the Pinger and Generic classes *my classes*
# and the provided ones
from Pinger import Pinger
from Generic import Generic
from re import compile, match
from time import sleep

# Compile some patterns we are going to use
pingerTypes = compile('[SsCc]')
alpha = compile('[a-zA-Z]')

# Instantiate our classes.
g = Generic()
p = Pinger()

# This loop is simply to get either a C, c, s, or S.  We want to control
# what is inputted so we start the right thing
while(True):
    # Get what you want to start
    startType = raw_input("Start a Pinger Server (S) or Pinger Client (C): ")
    if not match(pingerTypes, startType):
        continue
    
    # Get what port to use
    port = raw_input("Enter port number to use for ping: ")
    p.port = int(port)
    
    # Optionally, get the server to ping and how many 
    # (for client only)
    if match('[Cc]', startType):
        server = raw_input("Enter server to ping: ")
        numPings = raw_input("How many pings: ")
        numPings = int(numPings)        
    break

# If we selected to start the server start it.  We will block here
# until the PingServer is killed via the kill string
if match('[Ss]', startType):
    p.PingServer()
else:
# Otherwise, start a client.  Loop through the number of iterations and
# sleep for 1 second between loops.
    for x in range(numPings):
        retMsg = p.PingClient(server, g.stdMessage())
        print(retMsg.rstrip('\n'))
        sleep(1)
    # Send the kill string to stop the server process
    p.PingClient(server, 'KILL')

exit

        
        




