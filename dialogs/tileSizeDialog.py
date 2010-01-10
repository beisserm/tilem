import wx
import wx.lib.intctrl

[wxID_TILESIZE, wxID_TILESIZEHEIGHTFIELD, wxID_TILESIZEHEIGHTLABEL,
 wxID_TILESIZEWIDTHFIELD, wxID_TILESIZEWIDTHLABEL, 
] = [wx.NewId() for _init_ctrls in range(5)]

class TileSizeDialog(wx.Dialog):
    
    def __init__(self, prnt, width=8, height=8):
        wx.Dialog.__init__(self, id=wxID_TILESIZE, name='tileSize', parent=prnt,
              size=wx.Size(260, 170),
              style=wx.DEFAULT_DIALOG_STYLE, title='Tile Size')
        self.SetClientSize(wx.Size(252, 136))

        self.widthField = wx.lib.intctrl.IntCtrl(allow_long=False,
              allow_none=False, default_color=wx.BLACK,
              id=wxID_TILESIZEWIDTHFIELD, limited=True, max=128, min=1,
              name='widthField', oob_color=wx.RED, parent=self,
              pos=wx.Point(104, 24), size=wx.Size(100, 21), style=0, value=width)

        self.heightField = wx.lib.intctrl.IntCtrl(allow_long=False,
              allow_none=False, default_color=wx.BLACK,
              id=wxID_TILESIZEHEIGHTFIELD, limited=True, max=128, min=1,
              name='heightField', oob_color=wx.RED, parent=self,
              pos=wx.Point(104, 56), size=wx.Size(100, 21), style=0, value=height)

        self.widthLabel = wx.StaticText(id=wxID_TILESIZEWIDTHLABEL,
              label='Width', name='widthLabel', parent=self, pos=wx.Point(48,
              26), size=wx.Size(28, 13), style=0)

        self.heightLabel = wx.StaticText(id=wxID_TILESIZEHEIGHTLABEL,
              label='Height', name='heightLabel', parent=self, pos=wx.Point(48,
              58), size=wx.Size(31, 13), style=0)

        self.okButton = wx.Button(id=wx.ID_OK, label='OK', name='okButton',
              parent=self, pos=wx.Point(48, 96), size=wx.Size(75, 23), style=0)

        self.cancelButton = wx.Button(id=wx.ID_CANCEL, label='Cancel',
              name='cancelButton', parent=self, pos=wx.Point(128, 96),
              size=wx.Size(75, 23), style=0)

    def GetTileSize(self):
        return [self.widthField.GetValue(), self.heightField.GetValue()]            