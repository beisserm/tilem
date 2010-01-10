#Boa:Dialog:canvasSize

import wx
import wx.lib.intctrl

def create(parent):
    return canvasSize(parent)

[wxID_CANVASSIZE, wxID_CANVASSIZECANCELBUTTON, wxID_CANVASSIZECOLSFIELD, 
 wxID_CANVASSIZECOLUMNSLABEL, wxID_CANVASSIZEOKBUTTON, 
 wxID_CANVASSIZEROWSFIELD, wxID_CANVASSIZEROWSLABEL, 
] = [wx.NewId() for _init_ctrls in range(7)]

class canvasSize(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=wxID_CANVASSIZE, name='canvasSize',
              parent=prnt, pos=wx.Point(827, 306), size=wx.Size(260, 170),
              style=wx.DEFAULT_DIALOG_STYLE, title='Canvas Size')
        self.SetClientSize(wx.Size(252, 136))

        self.rowsField = wx.lib.intctrl.IntCtrl(allow_long=False,
              allow_none=False, default_color=wx.BLACK,
              id=wxID_CANVASSIZEROWSFIELD, limited=True, max=128, min=1,
              name='rowsField', oob_color=wx.RED, parent=self, pos=wx.Point(104,
              24), size=wx.Size(100, 21), style=0, value=1)

        self.colsField = wx.lib.intctrl.IntCtrl(allow_long=False,
              allow_none=False, default_color=wx.BLACK,
              id=wxID_CANVASSIZECOLSFIELD, limited=True, max=128, min=1,
              name='colsField', oob_color=wx.RED, parent=self, pos=wx.Point(104,
              56), size=wx.Size(100, 21), style=0, value=1)

        self.rowsLabel = wx.StaticText(id=wxID_CANVASSIZEROWSLABEL,
              label='Rows', name='rowsLabel', parent=self, pos=wx.Point(48, 26),
              size=wx.Size(26, 13), style=0)

        self.columnsLabel = wx.StaticText(id=wxID_CANVASSIZECOLUMNSLABEL,
              label='Columns', name='columnsLabel', parent=self,
              pos=wx.Point(48, 58), size=wx.Size(40, 13), style=0)

        self.okButton = wx.Button(id=wx.ID_OK, label='OK', name='okButton',
              parent=self, pos=wx.Point(48, 96), size=wx.Size(75, 23), style=0)

        self.cancelButton = wx.Button(id=wx.ID_CANCEL, label='Cancel',
              name='cancelButton', parent=self, pos=wx.Point(128, 96),
              size=wx.Size(75, 23), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)
