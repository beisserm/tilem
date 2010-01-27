#Boa:Frame:SidePanel

import wx
import wx.lib.buttons as buttons

from pubsub import pub

ID_ScrollUp = wx.NewId()
ID_ScrollDown = wx.NewId()
ID_ShiftLeft = wx.NewId()
ID_ShiftRight = wx.NewId()
ID_ShiftUp = wx.NewId()
ID_ShiftDown = wx.NewId()
ID_RowBack = wx.NewId()
ID_RowForward = wx.NewId()
ID_TileBack = wx.NewId() 
ID_TileForward = wx.NewId()
ID_ByteBack = wx.NewId() 
ID_ByteForward = wx.NewId() 

ID_Selection = wx.NewId()
ID_MoveSelection = wx.NewId()
ID_ColorPicker = wx.NewId()
ID_PencilDraw = wx.NewId() 
ID_FloodFill = wx.NewId() 
ID_Recolor = wx.NewId()
#ID_Zoom = wx.NewId()
#ID_DrawLine = wx.NewId() 

FRAME_SIZE = wx.Size(72, 296)

class ToolPanel(wx.MiniFrame):
    def __init__(self, prnt):
        wx.MiniFrame.__init__(self, id=wx.ID_ANY, name='', parent=prnt,
                              pos=wx.DefaultPosition , size=FRAME_SIZE,
                              style=wx.FRAME_TOOL_WINDOW | wx.CLOSE_BOX | wx.DEFAULT_FRAME_STYLE,
                              title='Tools')

        self.pane = wx.Panel(id=wx.ID_ANY, name='panel1', parent=self, pos=wx.Point(0, 0),
                                    size=FRAME_SIZE, style=wx.TAB_TRAVERSAL)
    
        self.SetSizeHintsSz(FRAME_SIZE, FRAME_SIZE)
        
        def ButtonMaker(bitmapString, id, pos, toolTip, handler):
            button = wx.BitmapButton(
                bitmap=wx.Bitmap(bitmapString, wx.BITMAP_TYPE_PNG),
                id=id, parent=self.pane, pos=pos, size=wx.Size(28, 28),
                style=wx.BU_AUTODRAW)
            button.SetToolTipString(toolTip)
            self.Bind(wx.EVT_BUTTON, handler, button)
	    return button

	# Tools
        self._makeSelectionButton = ButtonMaker(u'./icons/select-16.png', ID_Selection,
                                         wx.Point(4, 4), u'Make Selection ()', self.OnCanvasTool)
    
        self._moveSelectionButton = ButtonMaker(u'./icons/moveSelection-16.png', ID_MoveSelection,
                                         wx.Point(32, 4), u'Move Selection (M)', self.OnCanvasTool)        
        
        self._drawPencilButton = ButtonMaker(u'./icons/pencil-16.png', ID_PencilDraw,
                                         wx.Point(4, 32), u'Pencil (P)', self.OnCanvasTool)
        
        self._colorPickerButton = ButtonMaker(u'./icons/dropper-16.png', ID_ColorPicker,
                                         wx.Point(32, 32), u'Color Picker (K)', self.OnCanvasTool)
    
        self._floodFillButton = ButtonMaker(u'./icons/fill-16.png', ID_FloodFill,
                                         wx.Point(4, 60), u'Flood Fill (F)', self.OnCanvasTool)
    
        self._reColorButton = ButtonMaker(u'./icons/color-replace-16.png', ID_Recolor,
                                         wx.Point(32, 60), u'Recolor (R)', self.OnCanvasTool)
    
	# Shifts
        self._shiftLeftButton = ButtonMaker(u'./icons/shift-left-16.png', ID_ShiftLeft,
                                         wx.Point(4, 92), u'Shift Left (Left)', self.OnCanvasShift)
    
        self._shiftRightButton = ButtonMaker(u'./icons/shift-right-16.png', ID_ShiftRight,
                                         wx.Point(32, 92), u'Shift Right (Right)', self.OnCanvasShift)
    
        self._shiftUpButton = ButtonMaker(u'./icons/shift-up-16.png', ID_ShiftUp,
                                         wx.Point(4, 120), u'Shift Up (Up)', self.OnCanvasShift)
        
        self._shiftDownButton = ButtonMaker(u'./icons/shift-down-16.png', ID_ShiftDown,
                                         wx.Point(32, 120), u'Shift Down (Down)', self.OnCanvasShift)

	# Arrangement
        self._scrollUpButton = ButtonMaker(u'./icons/page-up-16.png', ID_ScrollUp,
                                         wx.Point(4, 152), u'Scroll Up (PgUp)', self.OnCanvasArrangement)
    
        self._scrollDownButton = ButtonMaker(u'./icons/page-down-16.png', ID_ScrollDown,
                                         wx.Point(32, 152), u'Scroll Down (PgDn)', self.OnCanvasArrangement) 
        
        self._rowBackwardButton = ButtonMaker(u'./icons/rowBack-16.png', ID_RowBack,
                                         wx.Point(4, 180), u'Row Backward ()', self.OnCanvasArrangement) 
        
        self._rowForwardButton = ButtonMaker(u'./icons/rowForward-16.png', ID_RowForward,
                                         wx.Point(32, 180), u'Row Forward ()', self.OnCanvasArrangement)  
    
        self._tileBackwardButton = ButtonMaker(u'./icons/tileBack-16.png', ID_TileBack,
                                         wx.Point(4, 208), u'Tile Backward (PgDn)', self.OnCanvasArrangement)
        
        self._tileForwardButton = ButtonMaker(u'./icons/tileForward-16.png', ID_TileForward,
                                         wx.Point(32, 208), u'Tile Forward ()', self.OnCanvasArrangement)
    
        self._byteBackwardButton = ButtonMaker(u'./icons/byteBack-16.png', ID_ByteBack,
                                         wx.Point(4, 236), u'Byte Backward ()', self.OnCanvasArrangement)
        
        self._byteForwardButton = ButtonMaker(u'./icons/byteForward-16.png', ID_ByteForward,
                                         wx.Point(32, 236), u'Byte Forward ()', self.OnCanvasArrangement)

        #self._drawLineButton = ButtonMaker(u'./icons/line-16.png', ID_DrawLine,
                                         #wx.Point(32, 60), u'Draw Line (O)', self.OnCanvasArrangement)                                           
        
        self.Show()

    def OnCanvasTool(self, event):
	buttonId = event.GetEventObject().GetId()
	pub.sendMessage('canvasTool', toolId=buttonId)

    def OnCanvasShift(self, event):
	buttonId = event.GetEventObject().GetId()
	pub.sendMessage('canvasShift', shiftId=buttonId)

    def OnCanvasArrangement(self, event):
	buttonId = event.GetEventObject().GetId()
	pub.sendMessage('canvasArrangement', actionId=buttonId)
