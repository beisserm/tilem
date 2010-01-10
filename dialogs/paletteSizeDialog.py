#Boa:Dialog:ChangePaletteDialog

import wx

def create(parent):
    return ChangePaletteDialog(parent)

[wxID_CHANGEPALETTEDIALOG, wxID_CHANGEPALETTEDIALOGCANCELBUTTON, 
 wxID_CHANGEPALETTEDIALOGOKBUTTON, wxID_CHANGEPALETTEDIALOGSIZEDIALOG, 
 wxID_CHANGEPALETTEDIALOGSIZELABEL, 
] = [wx.NewId() for _init_ctrls in range(5)]

class ChangePaletteDialog(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_CHANGEPALETTEDIALOG,
              name='ChangePaletteDialog', parent=prnt,
              size=wx.Size(226, 136), style=wx.DEFAULT_DIALOG_STYLE,
              title='Change Palette Size')
        self.SetClientSize(wx.Size(220, 104))
        self.SetToolTipString('')

        self.OKButton = wx.Button(id=wx.ID_OK, label='OK', name='OKButton',
              parent=self, pos=wx.Point(24, 64), size=wx.Size(75, 23), style=0)
        self.OKButton.SetToolTipString('')

        self.CancelButton = wx.Button(id=wx.ID_CANCEL, label='Cancel',
              name='CancelButton', parent=self, pos=wx.Point(112, 64),
              size=wx.Size(75, 23), style=0)
        self.CancelButton.SetToolTipString('')

        self.SizeLabel = wx.StaticText(id=wxID_CHANGEPALETTEDIALOGSIZELABEL,
              label='Size', name='SizeLabel', parent=self, pos=wx.Point(40, 27),
              size=wx.Size(32, 16), style=0)

        self.SizeDialog = wx.TextCtrl(id=wxID_CHANGEPALETTEDIALOGSIZEDIALOG,
              name='SizeDialog', parent=self, pos=wx.Point(104, 24),
              size=wx.Size(48, 21), style=0, value='0')
        self.SizeDialog.SetMaxLength(4)

    def __init__(self, parent):
        self._init_ctrls(parent)
