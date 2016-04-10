"""

    Copyright Ryan Kirkbride 2015

    This is the module that combines all the other modules as if it were the live
    environment. The main.py application execute() method sends the string over to
    this module, which is analysed and sent back as the raw python code to execute.

    This module also handles the time keeping aspect. There is a constant tempo
    clock running that has a queue and plays the items accordingly

    Note: The code below IS executed in the Environment and can be accessed by the user!

"""
from random import choice as choose

from TempoClock import *
from ServerManager import *
from Players import *
from Patterns import *
from Code import *
from TimeVar import *
import Scale

"""
    These define 'global' defaults:

        - Tempo Clock

        - Server Connection

        - Sample Buffers

        - Default Scale (loaded from Scale)

"""
        
Server = ServerManager()
Clock = TempoClock()
Buffers = BufferManager(Server)
Buffers.load()

"""
    Below are the classes for the three main aspects of FoxDot:

        - Player Objects

        - Sample Player Objects

        - Time-Dependant Variables        

"""


class Player(SYNTH_PLAYER):

    def __init__(self, SynthDef, degree=[0], **kwargs):

        SYNTH_PLAYER.__init__(self, SynthDef, degree)

        # Set defaults
        
        self.metro = Clock
        self.server = Server
        self.scale = kwargs.get( "scale", Scale.default() )
        self.dur = self.attr['dur'] = 1
        self.sus = self.attr['sus'] = 1
        
        # Add to clock and update with keyword arguments
        
        self.metro.playing.append(self)
        self.update_clock()
        self._INIT = True

        # Update attributes
        
        self.update(SynthDef, degree, **kwargs)
        
class SamplePlayer(SAMPLE_PLAYER):

    def __init__(self, string, **kwargs):
        
        SAMPLE_PLAYER.__init__(self, string, **kwargs)
        
        # Set defaults
        self.metro   = Clock
        self.server  = Server
        self.dur     = self.attr['dur']     = 0.5
        self.dur_val = self.attr['dur_val'] = 0.5

        # Add to clock and update
        self.metro.playing.append(self)
        self.update_clock()
        self._INIT = True

        # Update attributes
        
        self.update(self.degree)

class Var(TimeVar):

    """

        Time-Dependant Variable Class
        =============================

        Var(Values, Durations) -> TimeVar

        Creates a time-dependant variable that uses the default clock implicitly.
        Durations has a value of 4 by default and can be a single number or list
        of ints or floats.
        

    """

    def __init__(self, values=[0], dur=4):

        TimeVar.__init__(self, values, dur, Clock)

var = Var





