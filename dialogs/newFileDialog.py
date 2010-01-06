import wx

import wx.lib.intctrl

[wxID_NEWFILEDIALOG, 
 wxID_NEWFILEDIALOGFILESIZE,
 wxID_NEWFILEDIALOGTEXTCTRL1, 
] = [wx.NewId() for i in range(3)]

class NewFileDialog(wx.Dialog):
    def __init__(self, prnt):
        wx.Dialog.__init__(self, id=wxID_NEWFILEDIALOG, name='NewFileDialog',
              parent=prnt, pos=wx.Point(462, 298), size=wx.Size(293, 139),
              style=wx.DEFAULT_DIALOG_STYLE, title='File Size (Bytes) [Max: 134217728]')
        self.SetClientSize(wx.Size(285, 105))

        self.fileSizeLabel = wx.StaticText(id=wxID_NEWFILEDIALOGFILESIZE,
              label='File Size', name='fileSize', parent=self, pos=wx.Point(80,
              28), size=wx.Size(38, 13), style=0)

        self.fileSizeField = wx.lib.intctrl.IntCtrl(self, 
                value = 1, min = 1, max = 134217728,
                allow_long = True, pos = wx.Point(128, 24), size=(96, -1))

        self.okButton = wx.Button(id=wx.ID_OK, label='OK',
              name='okButton', parent=self, pos=wx.Point(56, 64),
              size=wx.Size(75, 23), style=0)

        self.cancelButton = wx.Button(id=wx.ID_CANCEL,
              label='Cancel', name='cancelButton', parent=self,
              pos=wx.Point(152, 64), size=wx.Size(75, 23), style=0)
        
        self.Show(True)        

    def GetSize(self):
        ''' 
        Returns the user entered size
        '''
        return self.fileSizeField.GetValue()        
