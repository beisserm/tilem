import wx

theEVT_PALETTE_POSITION = wx.NewEventType()
EVT_PALETTE_POSITION = wx.PyEventBinder(theEVT_PALETTE_POSITION, 1)

theEVT_TOOL_DRAW = wx.NewEventType()
EVT_TOOL_DRAW = wx.PyEventBinder(theEVT_TOOL_DRAW, 1)

theEVT_TOOL_MOVE = wx.NewEventType()
EVT_TOOL_MOVE = wx.PyEventBinder(theEVT_TOOL_MOVE, 1)

theEVT_TOOL = wx.NewEventType()
EVT_TOOL = wx.PyEventBinder(theEVT_TOOL, 1)

#---------------------------------------------------------------------------
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
    
#---------------------------------------------------------------------------
class ToolEvt(wx.PyCommandEvent):
    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)
        
        #self.actionType = actionType

    #def SetAction(self, actionType):
        #self.actionType = actionType

    #def GetAction(self):
        #return self.actionType    
    
#---------------------------------------------------------------------------
class ToolDrawEvt(wx.PyCommandEvent):
    def __init__(self, evtType, id, tool):
        wx.PyCommandEvent.__init__(self, evtType, id)
        
        self.tool = tool

    def SetTool(self, tool):
        self.tool = tool

    def GetTool(self):
        return self.tool

#---------------------------------------------------------------------------    
class ToolMoveEvt(wx.PyCommandEvent):
    def __init__(self, evtType, id, action):
        wx.PyCommandEvent.__init__(self, evtType, id)
        
        self.action = action

    def SetAction(self, action):
        self.action = action

    def GetAction(self):
        return self.action    