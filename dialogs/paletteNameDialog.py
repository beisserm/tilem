import wx

class PaletteNameDialog(wx.Dialog):
    def __init__(self, prnt, name='No Name'):
        wx.Dialog.__init__(self, id=-1, name='NewFileDialog',
              parent=prnt, size=wx.Size(293, 139),
              style=wx.DEFAULT_DIALOG_STYLE, title='Change Palette Name')
        self.SetClientSize(wx.Size(285, 105))        
        
        self.nameLabel = wx.StaticText(id=-1,
              label='New Name', name='nameLabel', parent=self, pos=wx.Point(60, 28),
              size=wx.Size(50, 13), style=0)

        self.nameField = wx.TextCtrl(self, -1, name, size=(96, -1), pos=wx.Point(128,24))

        self.okButton = wx.Button(id=wx.ID_OK, label='OK',
              name='okButton', parent=self, pos=wx.Point(56, 64),
              size=wx.Size(75, 23), style=0)

        self.cancelButton = wx.Button(id=wx.ID_CANCEL,
              label='Cancel', name='cancelButton', parent=self,
              pos=wx.Point(152, 64), size=wx.Size(75, 23), style=0)
        
        self.Show(True)        

    def GetName(self):
        ''' 
        Returns the user entered size
        '''
        return self.nameField.GetValue()        
