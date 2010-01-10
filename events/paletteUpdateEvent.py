import wx

myEVT_PALETTE_UPDATE = wx.NewEventType()
EVT_PALETTE_UPDATE = wx.PyEventBinder(myEVT_PALETTE_UPDATE, 1)

class PaletteUpdateEvent(wx.PyCommandEvent):
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