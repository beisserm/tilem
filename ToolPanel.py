#Boa:Frame:SidePanel

import wx

[wxID_SidePanel, ID_Selection, ID_ShiftRight,
 ID_ShiftUp, ID_ShiftDown,
 ID_ScrollUp, ID_PageDown,
 ID_RowBack, ID_RowForward,
 ID_TileBack, ID_TileForward,
 ID_ByteBack, ID_MoveSelection,
 ID_ByteForward, ID_Zoom,
 ID_ColorPicker, ID_PencilDraw, ID_DrawLine,
 ID_FloodFill, ID_Recolor, ID_ShiftLeft,
 wxID_SidePanelSIDEPANEL,
] = [wx.NewId() for _init_ctrls in range(22)]

class ToolPanel(wx.MiniFrame):
	def __init__(self, prnt):
		wx.MiniFrame.__init__(self, id=-1, name='', parent=prnt,
		                      pos=wx.Point(512, 312), size=wx.Size(72, 320),
		                      style=wx.FRAME_TOOL_WINDOW | wx.CLOSE_BOX | wx.DEFAULT_FRAME_STYLE,
		                      title='Tools')

		self.pane = pane = wx.Panel(id=-1, name='panel1', parent=self, pos=wx.Point(0, 0),
		                            size=wx.Size(72, 320), style=wx.TAB_TRAVERSAL)
	
		self.bitmapButton1 = wx.BitmapButton(
		    bitmap=wx.Bitmap(u'C:/tilemPy/icons/select-16.png', wx.BITMAP_TYPE_PNG),
		    id=ID_Selection, 
		    name='bitmapButton1', 
		    parent=pane,
		    pos=wx.Point(4, 4),
		    size=wx.Size(28, 28),
		    style=wx.BU_AUTODRAW)
		self.bitmapButton1.SetToolTipString('Make Selection ()')		
		self.Bind(wx.EVT_TOOL, self.OnSelect, id=ID_Selection)
	
		self.bitmapButton2 = wx.BitmapButton(
		    bitmap=wx.Bitmap(u'C:/tilemPy/icons/moveSelection-16.png', wx.BITMAP_TYPE_PNG),
		    id=ID_MoveSelection,
		    name='bitmapButton2',
		    parent=pane,
		    pos=wx.Point(32, 4),
		    size=wx.Size(28, 28),
		    style=wx.BU_AUTODRAW)
		self.bitmapButton2.SetToolTipString('Move Selection (M)')
		self.Bind(wx.EVT_TOOL, self.OnMoveSelection, id=ID_MoveSelection)
	
		self.bitmapButton3 = wx.BitmapButton(
		    bitmap=wx.Bitmap(u'C:/tilemPy/icons/zoom-16.png', wx.BITMAP_TYPE_PNG), 
		    id=ID_Zoom,
		    name='bitmapButton3', 
		    parent=pane, 
		    pos=wx.Point(4, 32),
		    size=wx.Size(28, 28),
		    style=wx.BU_AUTODRAW)
		self.bitmapButton3.SetToolTipString('Zoom (Z)')
		self.Bind(wx.EVT_TOOL, self.OnZoom, id=ID_Zoom)		
	
		self.bitmapButton4 = wx.BitmapButton(
		    bitmap=wx.Bitmap(u'C:/tilemPy/icons/dropper-16.png', wx.BITMAP_TYPE_PNG), 
		    id=ID_ColorPicker,
		    name='bitmapButton4', 
		    parent=pane, 
		    pos=wx.Point(32, 32),
		    size=wx.Size(28, 28), 
		    style=wx.BU_AUTODRAW)
		self.bitmapButton4.SetToolTipString('Color Picker (K)')
		self.Bind(wx.EVT_TOOL, self.OnColorSelector, id=ID_ColorPicker)		
	
		self.bitmapButton5 = wx.BitmapButton(
		    bitmap=wx.Bitmap(u'C:/tilemPy/icons/pencil-16.png', wx.BITMAP_TYPE_PNG), 
		    id=ID_PencilDraw,
		    name='bitmapButton5', 
		    parent=pane, 
		    pos=wx.Point(4, 60),
		    size=wx.Size(28, 28), 
		    style=wx.BU_AUTODRAW)
		self.bitmapButton5.SetToolTipString('Pencil (P)')
		self.Bind(wx.EVT_TOOL, self.OnPencilDraw, id=ID_PencilDraw)		
	
		self.bitmapButton6 = wx.BitmapButton(
		    bitmap=wx.Bitmap(u'C:/tilemPy/icons/line-16.png', wx.BITMAP_TYPE_PNG), 
		    id=ID_DrawLine,
		    name='bitmapButton6',
		    parent=pane, pos=wx.Point(32, 60),
		    size=wx.Size(28, 28),
		    style=wx.BU_AUTODRAW)
		self.bitmapButton6.SetToolTipString('Draw Line (O)')
		self.Bind(wx.EVT_TOOL, self.OnDrawLine, id=ID_DrawLine)		
	
		self.bitmapButton7 = wx.BitmapButton(
		    bitmap=wx.Bitmap(u'C:/tilemPy/icons/fill-16.png', wx.BITMAP_TYPE_PNG), 
		    id=ID_FloodFill,
		    name='bitmapButton7',
		    parent=pane,
		    pos=wx.Point(4, 88),
		    size=wx.Size(28, 28),
		    style=wx.BU_AUTODRAW)
		self.bitmapButton7.SetToolTipString('Flood Fill (F)')
		self.Bind(wx.EVT_TOOL, self.OnFloodFill, id=ID_FloodFill)		
	
		self.bitmapButton8 = wx.BitmapButton(
		    bitmap=wx.Bitmap(u'C:/tilemPy/icons/color-replace-16.png', wx.BITMAP_TYPE_PNG),
		    id=ID_Recolor,
		    name='bitmapButton8', 
		    parent=pane,
		    pos=wx.Point(32, 88),
		    size=wx.Size(28, 28), 
		    style=wx.BU_AUTODRAW)
		self.bitmapButton8.SetToolTipString('Recolor (R)')
		self.Bind(wx.EVT_TOOL, self.OnColorReplace, id=ID_Recolor)		
	
		self.bitmapButton9 = wx.BitmapButton(
		    bitmap=wx.Bitmap(u'C:/tilemPy/icons/shift-left-16.png', wx.BITMAP_TYPE_PNG),
		    id=ID_ShiftLeft,
		    name='bitmapButton9',
		    parent=pane, 
		    pos=wx.Point(4, 120),
		    size=wx.Size(28, 28), 
		    style=wx.BU_AUTODRAW)
		self.bitmapButton9.SetToolTipString('Shift Left (Left)')
		self.Bind(wx.EVT_TOOL, self.OnShiftLeft, id=ID_ShiftLeft)		
	
		self.bitmapButton10 = wx.BitmapButton(
		    bitmap=wx.Bitmap(u'C:/tilemPy/icons/shift-right-16.png', wx.BITMAP_TYPE_PNG), 
		    id=ID_ShiftRight,
		    name='bitmapButton10', 
		    parent=pane, 
		    pos=wx.Point(32, 120), 
		    size=wx.Size(28, 28), 
		    style=wx.BU_AUTODRAW)
		self.bitmapButton10.SetToolTipString('Shift Right (Right)')
		self.Bind(wx.EVT_TOOL, self.OnShiftRight, id=ID_ShiftRight)		
	
		self.bitmapButton11 = wx.BitmapButton(
		    bitmap=wx.Bitmap(u'C:/tilemPy/icons/shift-up-16.png', wx.BITMAP_TYPE_PNG),
		    id=ID_ShiftUp,
		    name='bitmapButton11',
		    parent=pane,
		    pos=wx.Point(4, 148),
		    size=wx.Size(28, 28), 
		    style=wx.BU_AUTODRAW)
		self.bitmapButton11.SetToolTipString('Shift Up (Up)')
		self.Bind(wx.EVT_TOOL, self.OnShiftUp, id=ID_ShiftUp)		
	
		self.bitmapButton12 = wx.BitmapButton(
		    bitmap=wx.Bitmap(u'C:/tilemPy/icons/shift-down-16.png', wx.BITMAP_TYPE_PNG),
		    id=ID_ShiftDown,
		    name='bitmapButton12',
		    parent=pane,
		    pos=wx.Point(32, 148),
		    size=wx.Size(28, 28),
		    style=wx.BU_AUTODRAW)
		self.bitmapButton12.SetToolTipString('Shift Down (Down)')
		self.Bind(wx.EVT_TOOL, self.OnShiftDown, id=ID_ShiftDown)		
	
		self.bitmapButton13 = wx.BitmapButton(
		    bitmap=wx.Bitmap(u'C:/tilemPy/icons/page-up-16.png', wx.BITMAP_TYPE_PNG), 
		    id=ID_ScrollUp,
		    name='bitmapButton13',
		    parent=pane, 
		    pos=wx.Point(4, 180), 
		    size=wx.Size(28, 28), 
		    style=wx.BU_AUTODRAW)
		self.bitmapButton13.SetToolTipString('Scroll Up ()')
		self.Bind(wx.EVT_TOOL, self.OnPageUp, id=ID_ScrollUp)		
	
		self.bitmapButton14 = wx.BitmapButton(
		    bitmap=wx.Bitmap(u'C:/tilemPy/icons/page-down-16.png', wx.BITMAP_TYPE_PNG), 
		    id=ID_PageDown,
		    name='bitmapButton14', 
		    parent=pane, 
		    pos=wx.Point(32, 180),
		    size=wx.Size(28, 28), 
		    style=wx.BU_AUTODRAW)
		self.bitmapButton14.SetToolTipString('Scroll Down ()')
		self.Bind(wx.EVT_TOOL, self.OnPageDown, id=ID_PageDown)		
	
		self.bitmapButton15 = wx.BitmapButton(
		    bitmap=wx.Bitmap(u'C:/tilemPy/icons/rowBack-16.png', wx.BITMAP_TYPE_PNG), 
		    id=ID_RowBack,
		    name='bitmapButton15', 
		    parent=pane, 
		    pos=wx.Point(4, 208), 
		    size=wx.Size(28, 28),
		    style=wx.BU_AUTODRAW)
		self.bitmapButton15.SetToolTipString('Row Back ()')
		self.Bind(wx.EVT_TOOL, self.OnRowBackward, id=ID_RowBack)		
		
		self.bitmapButton16 = wx.BitmapButton(
		    bitmap=wx.Bitmap(u'C:/tilemPy/icons/rowForward-16.png', wx.BITMAP_TYPE_PNG),
		    id=ID_RowForward,
		    name='bitmapButton16', 
		    parent=pane,
		    pos=wx.Point(32, 208), 
		    size=wx.Size(28, 28),
		    style=wx.BU_AUTODRAW)
		self.bitmapButton16.SetToolTipString('Row Forward ()')
		self.Bind(wx.EVT_TOOL, self.OnRowForward, id=ID_RowForward)		
	
		self.bitmapButton17 = wx.BitmapButton(
		    bitmap=wx.Bitmap(u'C:/tilemPy/icons/tileBack-16.png', wx.BITMAP_TYPE_PNG),
		    id=ID_TileBack,
		    name='bitmapButton17', 
		    parent=pane, 
		    pos=wx.Point(4, 236), 
		    size=wx.Size(28, 28), 
		    style=wx.BU_AUTODRAW)
		self.bitmapButton17.SetToolTipString('Tile Back ()')
		self.Bind(wx.EVT_TOOL, self.OnTileBackward, id=ID_TileBack)		
	
		self.bitmapButton18 = wx.BitmapButton(
		    bitmap=wx.Bitmap(u'C:/tilemPy/icons/tileForward-16.png', wx.BITMAP_TYPE_PNG), 
		    id=ID_TileForward,
		    name='bitmapButton18', 
		    parent=pane, 
		    pos=wx.Point(32, 236),
		    size=wx.Size(28, 28), 
		    style=wx.BU_AUTODRAW)
		self.bitmapButton18.SetToolTipString('Tile Forward')
		self.Bind(wx.EVT_TOOL, self.OnTileForward, id=ID_TileForward)		
	
		self.bitmapButton19 = wx.BitmapButton(
		    bitmap=wx.Bitmap(u'C:/tilemPy/icons/byteBack-16.png', wx.BITMAP_TYPE_PNG),
		    id=ID_ByteBack,
		    name='bitmapButton19',
		    parent=pane,
		    pos=wx.Point(4, 264), 
		    size=wx.Size(28, 28), 
		    style=wx.BU_AUTODRAW)
		self.bitmapButton19.SetToolTipString('Byte Back ()')
		self.Bind(wx.EVT_TOOL, self.OnByteBackward, id=ID_ByteBack)		
	
		self.bitmapButton20 = wx.BitmapButton(
		    bitmap=wx.Bitmap(u'C:/tilemPy/icons/byteForward-16.png', wx.BITMAP_TYPE_PNG), 
		    id=ID_ByteForward,
		    name='bitmapButton20',
		    parent=pane,
		    pos=wx.Point(32, 264), 
		    size=wx.Size(28, 28),
		    style=wx.BU_AUTODRAW)
		self.bitmapButton20.SetToolTipString('Byte Forward ()')
		self.Bind(wx.EVT_TOOL, self.OnByteForward, id=ID_ByteForward)		
	
		self.Show()

#-----------------------------------------------------------------------------
	def OnSelect(self, evt):
		pass
	
	def OnMoveSelection(self, evt):
		pass
	
	def OnZoom(self, evt):
		pass
	
	def OnColorSelector(self, evt):
		pass	
	
	def OnPencilDraw(self, evt):
		pass
	
	def OnDrawLine(self, evt):
		pass
	
	def OnFloodFill(self, evt):
		pass
	
	def OnColorReplace(self, evt):
		pass
	
#------------------------------------------------------------------------------	
	def OnShiftLeft(self, evt):
		pass
	
	def OnShiftRight(self, evt):
		pass
	
	def OnShiftUp(self, evt):
		pass
	
	def OnShiftDown(self, evt):
		pass
	
#------------------------------------------------------------------------------	
	def OnPageUp(self, evt):
		pass
	
	def OnPageDown(self, evt):
		pass
	
	def OnRowBackward(self, evt):
		pass
	
	def OnRowForward(self, evt):
		pass
	
	def OnTileBackward(self, evt):
		pass
	
	def OnTileForward(self, evt):
		pass
	
	def OnByteBackward(self, evt):
		pass
	
	def OnByteForward(self, evt):
		pass	
# -----------------------------------------------------------------------------
