"""A `wx.Timer` subclass that invokes a specified callback
periodically.
"""
# Author: Prabhu Ramachandran <prabhu@aero.iitb.ac.in>
# Copyright (c) 2006-2007,  Enthought, Inc.
# License: BSD Style.

# Standard library imports.
import wx

######################################################################
# `Timer` class.
class Timer(wx.Timer):
    """Simple subclass of wx.Timer that allows the user to have a
    function called periodically.

    Any exceptions raised in the callable are caught.  If
    `StopIteration` is raised the timer stops.  If other exceptions are
    encountered the timer is stopped and the exception re-raised.
    """
    
    def __init__(self, millisecs, callable, *args, **kw_args):
        """Initialize instance to invoke the given `callable` with
        given arguments and keyword args after every `millisecs`
        (milliseconds).
        """
        wx.Timer.__init__(self, id=wx.NewId())
        self.callable = callable
        self.args = args
        self.kw_args = kw_args
        self.Start(millisecs)

    def Notify(self):
        """Overridden to call the given callable.  Exceptions raised
        in the callable are caught.  If `StopIteration` is raised the
        timer stops.  If other exceptions are encountered the timer is
        stopped and the exception re-raised.
        """
        try:
            self.callable(*self.args, **self.kw_args)
        except StopIteration:
            self.Stop()
        except:
            self.Stop()
            raise

#-------------------------------------------------------------------------------
#  
#  Provides a simple function for scheduling some code to run at some time in 
#  the future (assumes application is wxPython based).
#  Written by: David C. Morrill
#  Date: 05/18/2005
#  (c) Copyright 2005 by Enthought, Inc.
#  
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:  
#-------------------------------------------------------------------------------

import wx

#-------------------------------------------------------------------------------
#  Does something 100 milliseconds from now:  
#-------------------------------------------------------------------------------

def do_later ( callable, *args, **kw_args ):
    """ Does something 50 milliseconds from now.
    """
    DoLaterTimer( 50, callable, args, kw_args )
    
#-------------------------------------------------------------------------------
#  Does something after some specified time interval:  
#-------------------------------------------------------------------------------
        
def do_after ( interval, callable, *args, **kw_args ):
    """ Does something after some specified time interval.
    """
    DoLaterTimer( interval, callable, args, kw_args )
                
#-------------------------------------------------------------------------------
#  'DoLaterTimer' class:  
#-------------------------------------------------------------------------------

class DoLaterTimer ( wx.Timer ):

    # List of currently active timers:
    active_timers = []
    
    #---------------------------------------------------------------------------
    #  Initializes the object: 
    #---------------------------------------------------------------------------
        
    def __init__ ( self, interval, callable, args, kw_args ):
        global active_timers
        wx.Timer.__init__( self )
        for timer in self.active_timers:
            if ((timer.callable == callable) and
                (timer.args     == args)     and
                (timer.kw_args  == kw_args)):
                timer.Start( interval, True )
                return
        self.active_timers.append( self )
        self.callable = callable
        self.args     = args
        self.kw_args  = kw_args
        self.Start( interval, True )
        
    #---------------------------------------------------------------------------
    #  Handles the timer pop event:  
    #---------------------------------------------------------------------------
        
    def Notify ( self ):
        global active_timers
        
        self.active_timers.remove( self )
        self.callable( *self.args, **self.kw_args )
        

