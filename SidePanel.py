#Boa:Frame:Frame1

import wx

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1BITMAPBUTTON1, wxID_FRAME1BITMAPBUTTON10, 
 wxID_FRAME1BITMAPBUTTON11, wxID_FRAME1BITMAPBUTTON12, 
 wxID_FRAME1BITMAPBUTTON13, wxID_FRAME1BITMAPBUTTON14, 
 wxID_FRAME1BITMAPBUTTON15, wxID_FRAME1BITMAPBUTTON16, 
 wxID_FRAME1BITMAPBUTTON17, wxID_FRAME1BITMAPBUTTON18, 
 wxID_FRAME1BITMAPBUTTON19, wxID_FRAME1BITMAPBUTTON2, 
 wxID_FRAME1BITMAPBUTTON20, wxID_FRAME1BITMAPBUTTON3, 
 wxID_FRAME1BITMAPBUTTON4, wxID_FRAME1BITMAPBUTTON5, wxID_FRAME1BITMAPBUTTON6, 
 wxID_FRAME1BITMAPBUTTON7, wxID_FRAME1BITMAPBUTTON8, wxID_FRAME1BITMAPBUTTON9, 
 wxID_FRAME1SIDEPANEL, 
] = [wx.NewId() for _init_ctrls in range(22)]

class Frame1(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(496, 285), size=wx.Size(227, 412),
              style=wx.DEFAULT_FRAME_STYLE, title='Frame1')
        self.SetClientSize(wx.Size(219, 378))

        self.SidePanel = wx.Panel(id=wxID_FRAME1SIDEPANEL, name='SidePanel',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(64, 304),
              style=wx.TAB_TRAVERSAL)

        self.bitmapButton1 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/select-16.png',
              wx.BITMAP_TYPE_PNG), id=wxID_FRAME1BITMAPBUTTON1,
              name='bitmapButton1', parent=self.SidePanel, pos=wx.Point(4, 4),
              size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
        self.bitmapButton1.SetToolTipString('Selection (S)')

        self.bitmapButton2 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/moveSelection-16.png',
              wx.BITMAP_TYPE_PNG), id=wxID_FRAME1BITMAPBUTTON2,
              name='bitmapButton2', parent=self.SidePanel, pos=wx.Point(32, 4),
              size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
        self.bitmapButton2.SetToolTipString('Move Selection (M)')

        self.bitmapButton3 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/zoom-16.png',
              wx.BITMAP_TYPE_PNG), id=wxID_FRAME1BITMAPBUTTON3,
              name='bitmapButton3', parent=self.SidePanel, pos=wx.Point(4, 32),
              size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
        self.bitmapButton3.SetToolTipString('Zoom (Z)')

        self.bitmapButton4 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/dropper-16.png',
              wx.BITMAP_TYPE_PNG), id=wxID_FRAME1BITMAPBUTTON4,
              name='bitmapButton4', parent=self.SidePanel, pos=wx.Point(32, 32),
              size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
        self.bitmapButton4.SetToolTipString('Color Picker (K)')

        self.bitmapButton5 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/pencil-16.png',
              wx.BITMAP_TYPE_PNG), id=wxID_FRAME1BITMAPBUTTON5,
              name='bitmapButton5', parent=self.SidePanel, pos=wx.Point(4, 60),
              size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
        self.bitmapButton5.SetToolTipString('Pencil (P)')

        self.bitmapButton6 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/line-16.png',
              wx.BITMAP_TYPE_PNG), id=wxID_FRAME1BITMAPBUTTON6,
              name='bitmapButton6', parent=self.SidePanel, pos=wx.Point(32, 60),
              size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
        self.bitmapButton6.SetToolTipString('Draw Line (O)')

        self.bitmapButton7 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/fill-16.png',
              wx.BITMAP_TYPE_PNG), id=wxID_FRAME1BITMAPBUTTON7,
              name='bitmapButton7', parent=self.SidePanel, pos=wx.Point(4, 88),
              size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
        self.bitmapButton7.SetToolTipString('Flood Fill (F)')

        self.bitmapButton8 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/color-replace-16.png',
              wx.BITMAP_TYPE_PNG), id=wxID_FRAME1BITMAPBUTTON8,
              name='bitmapButton8', parent=self.SidePanel, pos=wx.Point(32, 88),
              size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
        self.bitmapButton8.SetToolTipString('Recolor (R)')

        self.bitmapButton9 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/shift-left-16.png',
              wx.BITMAP_TYPE_PNG), id=wxID_FRAME1BITMAPBUTTON9,
              name='bitmapButton9', parent=self.SidePanel, pos=wx.Point(4, 120),
              size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
        self.bitmapButton9.SetToolTipString('Shift Left (Left)')

        self.bitmapButton10 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/shift-right-16.png',
              wx.BITMAP_TYPE_PNG), id=wxID_FRAME1BITMAPBUTTON10,
              name='bitmapButton10', parent=self.SidePanel, pos=wx.Point(32,
              120), size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
        self.bitmapButton10.SetToolTipString('Shift Right (Right)')

        self.bitmapButton11 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/shift-up-16.png',
              wx.BITMAP_TYPE_PNG), id=wxID_FRAME1BITMAPBUTTON11,
              name='bitmapButton11', parent=self.SidePanel, pos=wx.Point(4,
              148), size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
        self.bitmapButton11.SetToolTipString('Shift Up (Up)')

        self.bitmapButton12 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/shift-down-16.png',
              wx.BITMAP_TYPE_PNG), id=wxID_FRAME1BITMAPBUTTON12,
              name='bitmapButton12', parent=self.SidePanel, pos=wx.Point(32,
              148), size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
        self.bitmapButton12.SetToolTipString('Shift Down (Down)')

        self.bitmapButton13 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/page-up-16.png',
              wx.BITMAP_TYPE_PNG), id=wxID_FRAME1BITMAPBUTTON13,
              name='bitmapButton13', parent=self.SidePanel, pos=wx.Point(4,
              180), size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
        self.bitmapButton13.SetToolTipString('Scroll Up ()')
        self.bitmapButton13.Bind(wx.EVT_BUTTON, self.OnBitmapButton13Button,
              id=wxID_FRAME1BITMAPBUTTON13)

        self.bitmapButton14 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/page-down-16.png',
              wx.BITMAP_TYPE_PNG), id=wxID_FRAME1BITMAPBUTTON14,
              name='bitmapButton14', parent=self.SidePanel, pos=wx.Point(32,
              180), size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
        self.bitmapButton14.SetToolTipString('Scroll Down ()')

        self.bitmapButton15 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/rowBack-16.png',
              wx.BITMAP_TYPE_PNG), id=wxID_FRAME1BITMAPBUTTON15,
              name='bitmapButton15', parent=self.SidePanel, pos=wx.Point(4,
              208), size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
        self.bitmapButton15.SetToolTipString('Row Back ()')

        self.bitmapButton16 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/rowForward-16.png',
              wx.BITMAP_TYPE_PNG), id=wxID_FRAME1BITMAPBUTTON16,
              name='bitmapButton16', parent=self.SidePanel, pos=wx.Point(32,
              208), size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
        self.bitmapButton16.SetToolTipString('Row Forward ()')

        self.bitmapButton17 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/tileBack-16.png',
              wx.BITMAP_TYPE_PNG), id=wxID_FRAME1BITMAPBUTTON17,
              name='bitmapButton17', parent=self.SidePanel, pos=wx.Point(4,
              236), size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
        self.bitmapButton17.SetToolTipString('Tile Back ()')

        self.bitmapButton18 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/tileForward-16.png',
              wx.BITMAP_TYPE_PNG), id=wxID_FRAME1BITMAPBUTTON18,
              name='bitmapButton18', parent=self.SidePanel, pos=wx.Point(32,
              236), size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
        self.bitmapButton18.SetToolTipString('Tile Forward')

        self.bitmapButton19 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/byteBack-16.png',
              wx.BITMAP_TYPE_PNG), id=wxID_FRAME1BITMAPBUTTON19,
              name='bitmapButton19', parent=self.SidePanel, pos=wx.Point(4,
              264), size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
        self.bitmapButton19.SetToolTipString('Byte Back ()')

        self.bitmapButton20 = wx.BitmapButton(bitmap=wx.Bitmap(u'C:/tilemPy/icons/byteForward-16.png',
              wx.BITMAP_TYPE_PNG), id=wxID_FRAME1BITMAPBUTTON20,
              name='bitmapButton20', parent=self.SidePanel, pos=wx.Point(32,
              264), size=wx.Size(28, 28), style=wx.BU_AUTODRAW)
        self.bitmapButton20.SetToolTipString('Byte Forward ()')

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnBitmapButton13Button(self, event):
        event.Skip()
