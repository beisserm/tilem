import wx
import wx.lib.intctrl
from wx.lib.masked import NumCtrl

bppSelections = ['4bpp CGA', '6bpp NES', '8bpp EGA', '9bpp RGB(333)', '15bpp RGB(555)', 
	                           '16bpp RGB(565)', '24bpp RGB(888)', '32bpp ARGB(8888)']

class NewPaletteDialog(wx.Dialog):
    def __init__(self, prnt):
        """
        Initializes the dialog
        """
        wx.Dialog.__init__(self, id=-1,
              name='NewPaletteDialog', parent=prnt, pos=wx.Point(437, 238),
#              size=wx.Size(300, 225), 
              style=wx.DEFAULT_DIALOG_STYLE,
              title='Create New Palette')
        self.SetClientSize(wx.Size(265, 152))

        self.nameText = wx.StaticText(id=-1, label='Name', parent=self,
                                      pos=wx.Point(16, 16), size=wx.Size(35, 13))
        
        self.nameField = wx.TextCtrl(id=-1, parent=self, value="New Palette",
                                     size=wx.Size(150, 21), pos=wx.Point(64, 12))
        
        self.sizeTxt = wx.StaticText(id=-1,
              label='Size', name='sizeTxt', parent=self, pos=wx.Point(16, 48),
              size=wx.Size(19, 13), style=0)
        
        self.sizeField = wx.lib.intctrl.IntCtrl(id=-1, allow_long=False,
              allow_none=False, default_color=wx.BLACK,
              limited=False, max=512, min=1,
              name='heightField', oob_color=wx.RED, parent=self,
              pos=wx.Point(64, 44), size=wx.Size(100, 21), style=0, value=256)

        self.formatText = wx.StaticText(id=-1,
              label='Format', name='formatText', parent=self, pos=wx.Point(16,
              78), size=wx.Size(34, 13))

        self.colorEncoding = wx.ComboBox(choices=bppSelections,
              id=-1, name='colorEncoding', parent=self,
              pos=wx.Point(64, 74), size=wx.Size(130, 21), style=wx.CB_READONLY, value='4bpp CGA')

        self.OkButton = wx.Button(id=wx.ID_OK, label='OK',
              name='OkButton', parent=self, pos=wx.Point(48, 112),
              size=wx.Size(75, 23), style=0)

        self.CancelButton = wx.Button(id=wx.ID_CANCEL,
              label='Cancel', name='CancelButton', parent=self,
              pos=wx.Point(144, 112), size=wx.Size(75, 23), style=0)

    def GetSize(self):
        """ 
        Gets the user entered size
        """
        return self.sizeField.GetValue()
    
    def GetColorEncoding(self):
        """
        Gets the current color encoding scheme
        """
        return self.colorEncoding.GetValue()
    
    def GetName(self):
        """
        Gets what the name of this palette is going to be. Names do not have to
        be unique.
        """
        return self.nameField.GetValue()