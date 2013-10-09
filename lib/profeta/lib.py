#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
lib.py
"""

import threading

from profeta.attitude import *
from profeta.inference import *
from profeta.main import *

class start(Reactor):
    pass


global start_event
start_event = +start()


# ------------------------------------------------------------------------------
def declare_episode(uEpisodeName):
    Engine.instance().set_declared_episode(uEpisodeName)

def context(uGoalName):
    declare_episode(uGoalName)

# ------------------------------------------------------------------------------
class start_episode(Action):

    def init(self):
        self.__e = Engine.instance()

    def execute(self):
        self.__e.set_current_episode(self[0])
        global start_event
        self.__e.generate_external_event (start_event)


# ------------------------------------------------------------------------------
class set_context(start_episode):
    pass


# ------------------------------------------------------------------------------
class nop(Action):

    def execute(self):
        pass


# ------------------------------------------------------------------------------
class OneShotPoller:

    def __init__ (self, uAutoRearm = False):
        self.__rearm = uAutoRearm
        self.__active = False
        self.__e = Engine.instance()
        self.init()

    def init(self):
        raise "NotImplemented"

    def activate(self):
        self.__active = True

    def suspend(self):
        self.__active = False

    def is_active(self):
        return self.__active

    def do_poll(self):
        if self.__active:
            bel = self.poll()
            if bel is not None:
                self.__e.generate_external_event(+bel)
                if not(self.__rearm):
                    self.__active = False

    def poll(self):
        raise "NotImplemented"



# ------------------------------------------------------------------------------
class RepetitivePoller(OneShotPoller):

    def __init__ (self):
        OneShotPoller.__init__ (self, True)


# ------------------------------------------------------------------------------
class Sensor:

    def __init__(self):
        self.__is_on = None

    def on(self):
        if self.__is_on is not None:
            self.__is_on = True
            self.resume()
        else:
            self.__is_on = True

    def off(self):
        if self.__is_on is not None:
            self.__is_on = False
            self.suspend()

    def is_on(self):
        return self.__is_on

    def prepare(self):
        self.on()
        self.start()

    def poll(self):
        if self.is_on():
            return self.sense()
        else:
            return None

    def start(self):
        pass

    def sense(self):
        raise "Not implemented"

    def suspend(self):
        pass

    def resume(self):
        pass


