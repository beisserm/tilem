#Boa:Frame:SidePanel

import wx

def create(parent):
	return SidePanel(parent)

[wxID_SidePanel, wxID_SidePanelBITMAPBUTTON1, wxID_SidePanelBITMAPBUTTON10,
 wxID_SidePanelBITMAPBUTTON11, wxID_SidePanelBITMAPBUTTON12,
 wxID_SidePanelBITMAPBUTTON13, wxID_SidePanelBITMAPBUTTON14,
 wxID_SidePanelBITMAPBUTTON15, wxID_SidePanelBITMAPBUTTON16,
 wxID_SidePanelBITMAPBUTTON17, wxID_SidePanelBITMAPBUTTON18,
 wxID_SidePanelBITMAPBUTTON19, wxID_SidePanelBITMAPBUTTON2,
 wxID_SidePanelBITMAPBUTTON20, wxID_SidePanelBITMAPBUTTON3,
 wxID_SidePanelBITMAPBUTTON4, wxID_SidePanelBITMAPBUTTON5, wxID_SidePanelBITMAPBUTTON6,
 wxID_SidePanelBITMAPBUTTON7, wxID_SidePanelBITMAPBUTTON8, wxID_SidePanelBITMAPBUTTON9,
 wxID_SidePanelSIDEPANEL,
] = [wx.NewId() for _init_ctrls in range(22)]

class ToolPanel(wx.MiniFrame):
	def __init__(self, prnt):
		wx.MiniFrame.__init__(self, id=-1, name='', parent=prnt,
		    pos=wx.Point(512, 312), size=wx.Size(72, 320),
		    style=wx.FRAME_TOOL_WINDOW | wx.CLOSE_BOX | wx.STAY_ON_TOP | wx.DEFAULT_FRAME_STYLE, title='Tools')

		self.pane = pane = wx.Panel(id=-1, name='panel1',
		        parent=self, pos=wx.Point(0, 0), size=wx.Size(72, 320),
		        style=wx.TAB_TRAVERSAL)
	
		self.bitmapButton1 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/select-16.png',
			    wx.BITMAP_TYPE_PNG), id=wxID_SidePanelBITMAPBUTTON1,
			    name='bitmapButton1', parent=pane, pos=wx.Point(4, 4),
			    size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
	
		self.bitmapButton2 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/moveSelection-16.png',
			    wx.BITMAP_TYPE_PNG), id=wxID_SidePanelBITMAPBUTTON2,
			    name='bitmapButton2', parent=pane, pos=wx.Point(32, 4),
			    size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
		self.bitmapButton2.SetToolTipString('Move Selection (M)')
	
		self.bitmapButton3 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/zoom-16.png',
			    wx.BITMAP_TYPE_PNG), id=wxID_SidePanelBITMAPBUTTON3,
			    name='bitmapButton3', parent=pane, pos=wx.Point(4, 32),
			    size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
		self.bitmapButton3.SetToolTipString('Zoom (Z)')
	
		self.bitmapButton4 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/dropper-16.png',
			    wx.BITMAP_TYPE_PNG), id=wxID_SidePanelBITMAPBUTTON4,
			    name='bitmapButton4', parent=pane, pos=wx.Point(32, 32),
			    size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
		self.bitmapButton4.SetToolTipString('Color Picker (K)')
	
		self.bitmapButton5 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/pencil-16.png',
			    wx.BITMAP_TYPE_PNG), id=wxID_SidePanelBITMAPBUTTON5,
			    name='bitmapButton5', parent=pane, pos=wx.Point(4, 60),
			    size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
		self.bitmapButton5.SetToolTipString('Pencil (P)')
	
		self.bitmapButton6 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/line-16.png',
			    wx.BITMAP_TYPE_PNG), id=wxID_SidePanelBITMAPBUTTON6,
			    name='bitmapButton6', parent=pane, pos=wx.Point(32, 60),
			    size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
		self.bitmapButton6.SetToolTipString('Draw Line (O)')
	
		self.bitmapButton7 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/fill-16.png',
			    wx.BITMAP_TYPE_PNG), id=wxID_SidePanelBITMAPBUTTON7,
			    name='bitmapButton7', parent=pane, pos=wx.Point(4, 88),
			    size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
		self.bitmapButton7.SetToolTipString('Flood Fill (F)')
	
		self.bitmapButton8 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/color-replace-16.png',
			    wx.BITMAP_TYPE_PNG), id=wxID_SidePanelBITMAPBUTTON8,
			    name='bitmapButton8', parent=pane, pos=wx.Point(32, 88),
			    size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
		self.bitmapButton8.SetToolTipString('Recolor (R)')
	
		self.bitmapButton9 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/shift-left-16.png',
			    wx.BITMAP_TYPE_PNG), id=wxID_SidePanelBITMAPBUTTON9,
			    name='bitmapButton9', parent=pane, pos=wx.Point(4, 120),
			    size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
		self.bitmapButton9.SetToolTipString('Shift Left (Left)')
	
		self.bitmapButton10 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/shift-right-16.png',
			    wx.BITMAP_TYPE_PNG), id=wxID_SidePanelBITMAPBUTTON10,
			    name='bitmapButton10', parent=pane, pos=wx.Point(32,
			    120), size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
		self.bitmapButton10.SetToolTipString('Shift Right (Right)')
	
		self.bitmapButton11 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/shift-up-16.png',
			    wx.BITMAP_TYPE_PNG), id=wxID_SidePanelBITMAPBUTTON11,
			    name='bitmapButton11', parent=pane, pos=wx.Point(4,
			    148), size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
		self.bitmapButton11.SetToolTipString('Shift Up (Up)')
	
		self.bitmapButton12 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/shift-down-16.png',
			    wx.BITMAP_TYPE_PNG), id=wxID_SidePanelBITMAPBUTTON12,
			    name='bitmapButton12', parent=pane, pos=wx.Point(32,
			    148), size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
		self.bitmapButton12.SetToolTipString('Shift Down (Down)')
	
		self.bitmapButton13 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/page-up-16.png',
			    wx.BITMAP_TYPE_PNG), id=wxID_SidePanelBITMAPBUTTON13,
			    name='bitmapButton13', parent=pane, pos=wx.Point(4,
			    180), size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
		self.bitmapButton13.SetToolTipString('Scroll Up ()')
	
		self.bitmapButton14 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/page-down-16.png',
			    wx.BITMAP_TYPE_PNG), id=wxID_SidePanelBITMAPBUTTON14,
			    name='bitmapButton14', parent=pane, pos=wx.Point(32,
			    180), size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
		self.bitmapButton14.SetToolTipString('Scroll Down ()')
	
		self.bitmapButton15 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/rowBack-16.png',
			    wx.BITMAP_TYPE_PNG), id=wxID_SidePanelBITMAPBUTTON15,
			    name='bitmapButton15', parent=pane, pos=wx.Point(4,
			    208), size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
		self.bitmapButton15.SetToolTipString('Row Back ()')
	
		self.bitmapButton16 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/rowForward-16.png',
			    wx.BITMAP_TYPE_PNG), id=wxID_SidePanelBITMAPBUTTON16,
			    name='bitmapButton16', parent=pane, pos=wx.Point(32,
			    208), size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
		self.bitmapButton16.SetToolTipString('Row Forward ()')
	
		self.bitmapButton17 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/tileBack-16.png',
			    wx.BITMAP_TYPE_PNG), id=wxID_SidePanelBITMAPBUTTON17,
			    name='bitmapButton17', parent=pane, pos=wx.Point(4,
			    236), size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
		self.bitmapButton17.SetToolTipString('Tile Back ()')
	
		self.bitmapButton18 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/tileForward-16.png',
			    wx.BITMAP_TYPE_PNG), id=wxID_SidePanelBITMAPBUTTON18,
			    name='bitmapButton18', parent=pane, pos=wx.Point(32,
			    236), size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
		self.bitmapButton18.SetToolTipString('Tile Forward')
	
		self.bitmapButton19 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/byteBack-16.png',
			    wx.BITMAP_TYPE_PNG), id=wxID_SidePanelBITMAPBUTTON19,
			    name='bitmapButton19', parent=pane, pos=wx.Point(4,
			    264), size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
		self.bitmapButton19.SetToolTipString('Byte Back ()')
	
		self.bitmapButton20 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/byteForward-16.png',
			    wx.BITMAP_TYPE_PNG), id=wxID_SidePanelBITMAPBUTTON20,
			    name='bitmapButton20', parent=pane, pos=wx.Point(32,
			    264), size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
		self.bitmapButton20.SetToolTipString('Byte Forward ()')
	
		self.Show()