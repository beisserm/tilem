import wx

theEVT_PALETTE_POSITION = wx.NewEventType()
EVT_PALETTE_POSITION = wx.PyEventBinder(theEVT_PALETTE_POSITION, 1)

#-----------------------------------------------------------------------------
class PalettePosEvt(wx.PyCommandEvent):
    def __init__(self, evtType, id, pos):
        wx.PyCommandEvent.__init__(self, evtType, id)
        
        self.currentPos = pos

    def SetPalettePos(self, pos):
        self.currentPos = pos

    def GetPalettePos(self):
        return self.currentPos
    
    #def __del__(self):
    #    print '__del__'
    #    wx.PyCommandEvent.__del__(self)    