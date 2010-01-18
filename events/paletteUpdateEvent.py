import wx

myEVT_BUTTON_CLICKPOS = wx.NewEventType()
EVT_BUTTON_CLICKPOS = wx.PyEventBinder(myEVT_BUTTON_CLICKPOS, 1)

#----------------------------------------------------------------------


class MyEvent(wx.PyCommandEvent):
    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)
        self.myVal = None

    #def __del__(self):
    #    print '__del__'
    #    wx.PyCommandEvent.__del__(self)

    def SetMyVal(self, val):
        self.myVal = val

    def GetMyVal(self):
        return self.myVal