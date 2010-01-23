#Boa:Frame:SidePanel

import wx
import wx.lib.buttons as buttons

import events.customEvent as ce

[wxID_SidePanel, ID_Selection, ID_ShiftRight,
 ID_ShiftUp, ID_ShiftDown,
 ID_ScrollUp, ID_ScrollDown,
 ID_RowBack, ID_RowForward,
 ID_TileBack, ID_TileForward,
 ID_ByteBack, ID_MoveSelection,
 ID_ByteForward, ID_Zoom,
 ID_ColorPicker, ID_PencilDraw, ID_DrawLine,
 ID_FloodFill, ID_Recolor, ID_ShiftLeft,
 wxID_SidePanelSIDEPANEL,
] = [wx.NewId() for _init_ctrls in range(22)]

FRAME_SIZE = wx.Size(72, 296)

class ToolPanel(wx.MiniFrame):
    def __init__(self, prnt):
        wx.MiniFrame.__init__(self, id=-1, name='', parent=prnt,
                              pos=wx.DefaultPosition , size=FRAME_SIZE,
                              style=wx.FRAME_TOOL_WINDOW | wx.CLOSE_BOX | wx.DEFAULT_FRAME_STYLE,
                              title='Tools')

        self.pane = wx.Panel(id=-1, name='panel1', parent=self, pos=wx.Point(0, 0),
                                    size=FRAME_SIZE, style=wx.TAB_TRAVERSAL)
    
        self.SetSizeHintsSz(FRAME_SIZE, FRAME_SIZE)
        
        def ButtonMaker(bitmapString, id, pos, toolTip):
            button = wx.BitmapButton(
                bitmap=wx.Bitmap(bitmapString, wx.BITMAP_TYPE_PNG),
                id=id, parent=self.pane, pos=pos, size=wx.Size(28, 28),
                style=wx.BU_AUTODRAW)
            button.SetToolTipString(toolTip)
            self.Bind(wx.EVT_BUTTON, self.OnToolEvt, button)
	    return button

        self._makeSelectionButton = ButtonMaker(u'./icons/select-16.png', ID_Selection,
                                         wx.Point(4, 4), u'Make Selection ()')
    
        self._moveSelectionButton = ButtonMaker(u'./icons/moveSelection-16.png', ID_MoveSelection,
                                         wx.Point(32, 4), u'Move Selection (M)')        
        
        self._drawPencilButton = ButtonMaker(u'./icons/pencil-16.png', ID_PencilDraw,
                                         wx.Point(4, 32), u'Pencil (P)')
        
        self._colorPickerButton = ButtonMaker(u'./icons/dropper-16.png', ID_ColorPicker,
                                         wx.Point(32, 32), u'Color Picker (K)')
    
        self._floodFillButton = ButtonMaker(u'./icons/fill-16.png', ID_FloodFill,
                                         wx.Point(4, 60), u'Flood Fill (F)')
    
        self._reColorButton = ButtonMaker(u'./icons/color-replace-16.png', ID_Recolor,
                                         wx.Point(32, 60), u'Recolor (R)')
    
        self._shiftLeftButton = ButtonMaker(u'./icons/shift-left-16.png', ID_ShiftLeft,
                                         wx.Point(4, 92), u'Shift Left (Left)')
    
        self._shiftRightButton = ButtonMaker(u'./icons/shift-right-16.png', ID_ShiftRight,
                                         wx.Point(32, 92), u'Shift Right (Right)')
    
        self._shiftUpButton = ButtonMaker(u'./icons/shift-up-16.png', ID_ShiftUp,
                                         wx.Point(4, 120), u'Shift Up (Up)')
        
        self._shiftDownButton = ButtonMaker(u'./icons/shift-down-16.png', ID_ShiftDown,
                                         wx.Point(32, 120), u'Shift Down (Down)')

        self._scrollUpButton = ButtonMaker(u'./icons/page-up-16.png', ID_ScrollUp,
                                         wx.Point(4, 152), u'Scroll Up (PgUp)')
    
        self._scrollDownButton = ButtonMaker(u'./icons/page-down-16.png', ID_ScrollDown,
                                         wx.Point(32, 152), u'Scroll Down (PgDn)') 
        
        self._rowBackwardButton = ButtonMaker(u'./icons/rowBack-16.png', ID_RowBack,
                                         wx.Point(4, 180), u'Row Backward ()') 
        
        self._rowForwardButton = ButtonMaker(u'./icons/rowForward-16.png', ID_RowForward,
                                         wx.Point(32, 180), u'Row Forward ()')  
    
        self._tileBackwardButton = ButtonMaker(u'./icons/tileBack-16.png', ID_TileBack,
                                         wx.Point(4, 208), u'Tile Backward (PgDn)')
        
        self._tileForwardButton = ButtonMaker(u'./icons/tileForward-16.png', ID_TileForward,
                                         wx.Point(32, 208), u'Tile Forward ()')
    
        self._byteBackwardButton = ButtonMaker(u'./icons/byteBack-16.png', ID_ByteBack,
                                         wx.Point(4, 236), u'Byte Backward ()')
        
        self._byteForwardButton = ButtonMaker(u'./icons/byteForward-16.png', ID_ByteForward,
                                         wx.Point(32, 236), u'Byte Forward ()')

        #self._Button = ButtonMaker(u'./icons/zoom-16.png', ID_Zoom,
                                         #wx.Point(4, 32), u'Zoom (Z)')

        #self._drawLineButton = ButtonMaker(u'./icons/line-16.png', ID_DrawLine,
                                         #wx.Point(32, 60), u'Draw Line (O)')                                           
        
        self.Show()

    def OnToolEvt(self, event):
	buttonId = event.GetEventObject().GetId()
	print 'id: ', buttonId
	evt = ce.ToolEvt(ce.theEVT_TOOL, id=buttonId)
	self.GetEventHandler().ProcessEvent(evt)
	event.Skip()