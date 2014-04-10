'''
Created on Apr 7, 2014

@author: stnel
'''

class Generic:
    '''
    Class Generic - generally useful methods
    This class contains some generally useful methods that can be
    applied to other projects
    '''

    def __init__(self):
        '''
        Setup a static sequence number and initiate a message var.
        '''
        self.seqNumber = 0
        self.msg = ""
        return
        
    def timeStamp(self):
        '''
        timeStamp - create a standardized timestamp on demand with
        '''
        from time import localtime, time
        timeInSec = time()
        decTime = str((timeInSec - int(timeInSec)))
        mytime = localtime(timeInSec)
        timestamp = str(mytime.tm_year) + format(mytime.tm_mon,'02d') + format(mytime.tm_mday,'02d') + format(mytime.tm_hour,'02d') + format(mytime.tm_min, '02d') + format(mytime.tm_sec,'02d') + decTime
        return(timestamp)
    
    def stdMessage(self):
        '''
        stdMessage - create a standard message for the ping routine...
        '''
        self.msg = 'PING ' + str(self.seqNumber) + ' ' + self.timeStamp() + '\n'
        self.seqNumber += 1
        return(self.msg)
