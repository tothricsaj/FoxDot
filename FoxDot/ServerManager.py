"""
    ServerManager.py

    Handles OSC messages being sent to SuperCollider. Will try and
    read data from Settings/server.txt which should contain the IP
    address and port separated by a single space. If not it defaults
    to SuperCollider's defaults.

"""

from OSC import *
client = OSCClient()

try:

    with open("Settings/server_address.txt") as f:
        info = f.readlines()[0].split()
        
    ADDRESS, PORT = (str(info[0]), int(info[1]))
    
except:
    
    ADDRESS, PORT = "localhost", 57110


client.connect( (ADDRESS, PORT) )

class ServerManager:

    def __init__(self):
        
        self.node = 1000

    def nextnodeID(self):
        self.node += 1
        return self.node

    def sendOSC(self, packet):
        """ Compiles and sends an OSC message for SuperCollider """
        message = OSCMessage("/s_new")
        packet[1] = self.nextnodeID()
        message.append(packet)
        client.send( message )
        return

    def send(self, message):
        client.send(OSCMessage(message))
        return

    def free_node(self, node):
        message = OSCMessage("/n_free")
        message.append(node)
        client.send( message )
        return

    def bufferRead(self, bufnum, path):
        message = OSCMessage("/b_allocRead")
        message.append([bufnum, path])
        client.send( message )
        return

#####

##class SuperColliderSynthDefs:
##
##    with open('startup.scd') as f:
##        sc = f.readlines()    
##    patt = r'SynthDef.*?\\(.*?)'
##
##    names = [match(patt, line).group(1) for line in sc if "SynthDef" in line and not line.startswith("/")]
##
##    def __init__(self):
##        pass
##    def __str__(self):
##        return str(self.names)
##    def __repr__(self):
##        return str(self.names)
##    def __len__(self):
##        return len(self.names)
##    def __iter__(self):
##        for x in self.names:
##            yield x
##    def __getitem__(self, key):
##        return self.names[key]
##    def __setitem__(self, name, value):
##        raise AttributeError("SynthDefs cannot be altered using FoxDot code")
##    def __call__(self):
##        return self.names
##    def choose(self):
##        return choose(self.names)
##
##SynthDefs = SuperColliderSynthDefs() 