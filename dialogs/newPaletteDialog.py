#Boa:Dialog:newPaletteDialog

import wx
import wx.lib.intctrl
from wx.lib.masked import NumCtrl

def create(parent):
    return NewPaletteDialog(parent)

[wxID_NEWPALETTEDIALOG, ID_CancelButton, 
 wxID_NEWPALETTEDIALOGCOMBOBOX1, wxID_NEWPALETTEDIALOGFORMATTEXT, 
 ID_OkButton, wxID_NEWPALETTEDIALOGSIZETXT, 
 wxID_NEWPALETTEDIALOGTEXTCTRL1, 
] = [wx.NewId() for _init_ctrls in range(7)]

bppSelections = ['4bpp CGA', '6bpp NES', '8bpp EGA', '9bpp RGB(333)', '15bpp RGB(555)', 
	                           '16bpp RGB(565)', '24bpp RGB(888)', '32bpp ARGB(8888)']

class NewPaletteDialog(wx.Dialog):
    def _init_ctrls(self, prnt):
        wx.Dialog.__init__(self, id=wxID_NEWPALETTEDIALOG,
              name='NewPaletteDialog', parent=prnt, pos=wx.Point(437, 238),
              size=wx.Size(273, 186), style=wx.DEFAULT_DIALOG_STYLE,
              title='Create New Palette')
        self.SetClientSize(wx.Size(265, 152))

        self.sizeField = wx.lib.intctrl.IntCtrl(allow_long=False,
              allow_none=False, default_color=wx.BLACK,
              id=-1, limited=False, max=512, min=1,
              name='heightField', oob_color=wx.RED, parent=self,
              pos=wx.Point(64, 24), size=wx.Size(100, 21), style=0, value=256)

        self.sizeTxt = wx.StaticText(id=wxID_NEWPALETTEDIALOGSIZETXT,
              label='Size', name='sizeTxt', parent=self, pos=wx.Point(16, 28),
              size=wx.Size(19, 13), style=0)

        self.formatText = wx.StaticText(id=wxID_NEWPALETTEDIALOGFORMATTEXT,
              label='Format', name='formatText', parent=self, pos=wx.Point(16,
              68), size=wx.Size(34, 13), style=0)

        self.colorEncoding = wx.ComboBox(choices=bppSelections,
              id=wxID_NEWPALETTEDIALOGCOMBOBOX1, name='colorEncoding', parent=self,
              pos=wx.Point(64, 64), size=wx.Size(130, 21), style=wx.CB_READONLY, value='colorEncoding')

        self.OkButton = wx.Button(id=wx.ID_OK, label='OK',
              name='OkButton', parent=self, pos=wx.Point(48, 112),
              size=wx.Size(75, 23), style=0)

        self.CancelButton = wx.Button(id=wx.ID_CANCEL,
              label='Cancel', name='CancelButton', parent=self,
              pos=wx.Point(144, 112), size=wx.Size(75, 23), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)


    def GetSize(self):
        ''' 
        Returns the user entered size
        '''
        return self.sizeField.GetValue()
    
    def GetColorEncoding(self):
        return self.colorEncoding.GetValue()