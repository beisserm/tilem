#Boa:Dialog:Dialog1

import wx

def create(parent):
    return Dialog1(parent)

[wxID_DIALOG1, wxID_DIALOG1BUTTON2, wxID_DIALOG1OK_BUTTON, 
 wxID_DIALOG1RADIOBOX1, wxID_DIALOG1RADIOBOX2, wxID_DIALOG1STATICBOX1, 
 wxID_DIALOG1TEXTCTRL1, 
] = [wx.NewId() for _init_ctrls in range(7)]

class Dialog1(wx.Dialog):
    def _init_sizers(self):
        # generated method, don't edit
        self.flexGridSizer2 = wx.FlexGridSizer(cols=0, hgap=0, rows=1, vgap=0)


    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_DIALOG1, name='', parent=prnt,
              pos=wx.Point(494, 134), size=wx.Size(378, 180),
              style=wx.DEFAULT_DIALOG_STYLE, title='Goto')
        self.SetClientSize(wx.Size(370, 146))
        self.Enable(True)

        self.OK_Button = wx.Button(id=wxID_DIALOG1OK_BUTTON, label='OK',
              name='OK_Button', parent=self, pos=wx.Point(112, 112),
              size=wx.Size(75, 23), style=0)
        self.OK_Button.SetAutoLayout(False)
        self.OK_Button.SetToolTipString('')
        self.OK_Button.Bind(wx.EVT_BUTTON, self.OnOK_ButtonButton,
              id=wxID_DIALOG1OK_BUTTON)

        self.button2 = wx.Button(id=wxID_DIALOG1BUTTON2, label='Cancel',
              name='button2', parent=self, pos=wx.Point(200, 112),
              size=wx.Size(75, 23), style=0)
        self.button2.SetToolTipString('')
        self.button2.SetHelpText('')

        self.staticBox1 = wx.StaticBox(id=wxID_DIALOG1STATICBOX1,
              label='staticBox1', name='staticBox1', parent=self,
              pos=wx.Point(8, 24), size=wx.Size(128, 64), style=0)

        self.textCtrl1 = wx.TextCtrl(id=wxID_DIALOG1TEXTCTRL1, name='textCtrl1',
              parent=self, pos=wx.Point(16, 48), size=wx.Size(112, 21), style=0,
              value='textCtrl1')

        self.radioBox1 = wx.RadioBox(choices=['Hex (16)', 'Dec (10)'],
              id=wxID_DIALOG1RADIOBOX1, label='Radix', majorDimension=1,
              name='radioBox1', parent=self, pos=wx.Point(264, 24),
              size=wx.Size(96, 64), style=wx.RA_SPECIFY_COLS)

        self.radioBox2 = wx.RadioBox(choices=['Absolute', 'Relative'],
              id=wxID_DIALOG1RADIOBOX2, label='Offset', majorDimension=1,
              name='radioBox2', parent=self, pos=wx.Point(152, 24),
              size=wx.Size(96, 64), style=wx.RA_SPECIFY_COLS)
        self.radioBox2.Bind(wx.EVT_RADIOBOX, self.OnRadioBox2Radiobox,
              id=wxID_DIALOG1RADIOBOX2)

        self._init_sizers()

    def __init__(self, parent):
        self._init_ctrls(parent)

    def OnOK_ButtonButton(self, event):
        event.Skip()

    def OnRadioBox2Radiobox(self, event):
        event.Skip()
