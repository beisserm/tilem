#Boa:Dialog:NewFileDialog

import wx

def create(parent):
    return NewFileDialog(parent)

[wxID_NEWFILEDIALOG, wxID_NEWFILEDIALOGCANCELBUTTON, 
 wxID_NEWFILEDIALOGFILESIZE, wxID_NEWFILEDIALOGOKBUTTON, 
 wxID_NEWFILEDIALOGTEXTCTRL1, 
] = [wx.NewId() for _init_ctrls in range(5)]

class NewFileDialog(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_NEWFILEDIALOG, name='NewFileDialog',
              parent=prnt, pos=wx.Point(462, 298), size=wx.Size(293, 139),
              style=wx.DEFAULT_DIALOG_STYLE, title='File Size (Bytes)')
        self.SetClientSize(wx.Size(285, 105))

        self.fileSize = wx.StaticText(id=wxID_NEWFILEDIALOGFILESIZE,
              label='File Size', name='fileSize', parent=self, pos=wx.Point(80,
              28), size=wx.Size(38, 13), style=0)

        self.textCtrl1 = wx.TextCtrl(id=wxID_NEWFILEDIALOGTEXTCTRL1,
              name='textCtrl1', parent=self, pos=wx.Point(128, 24),
              size=wx.Size(48, 21), style=0, value='1')

        self.okButton = wx.Button(id=wxID_NEWFILEDIALOGOKBUTTON, label='OK',
              name='okButton', parent=self, pos=wx.Point(56, 64),
              size=wx.Size(75, 23), style=0)

        self.cancelButton = wx.Button(id=wxID_NEWFILEDIALOGCANCELBUTTON,
              label='Cancel', name='cancelButton', parent=self,
              pos=wx.Point(152, 64), size=wx.Size(75, 23), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)
