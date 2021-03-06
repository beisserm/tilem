import wx
import wx.lib.intctrl

[wxID_CANVASSIZE, wxID_CANVASSIZECOLSFIELD, 
 wxID_CANVASSIZECOLUMNSLABEL, wxID_CANVASSIZEROWSFIELD, 
 wxID_CANVASSIZEROWSLABEL, 
] = [wx.NewId() for _init_ctrls in range(5)]

class CanvasSizeDialog(wx.Dialog):
    
    def __init__(self, prnt, rows=16, cols=16):
        '''
        Constructor
        @param rows
                 Number of rows to display in the dialog box. This is the
                 number of tile rows displayed on the canvas.                 
        @param columns
                 Number of columns to display in the dialog box. This is the
                 number of tile columns displayed on the canvas.
        '''
        wx.Dialog.__init__(self, id=wxID_CANVASSIZE, name='canvasSize',
              parent=prnt, size=wx.Size(260, 170),
              style=wx.DEFAULT_DIALOG_STYLE, title='Canvas Size')
        self.SetClientSize(wx.Size(252, 136))

        self.rowsField = wx.lib.intctrl.IntCtrl(allow_long=False,
              allow_none=False, default_color=wx.BLACK,
              id=wxID_CANVASSIZEROWSFIELD, limited=True, max=128, min=1,
              name='rowsField', oob_color=wx.RED, parent=self, pos=wx.Point(104,
              24), size=wx.Size(100, 21), style=0, value=rows)

        self.colsField = wx.lib.intctrl.IntCtrl(allow_long=False,
              allow_none=False, default_color=wx.BLACK,
              id=wxID_CANVASSIZECOLSFIELD, limited=True, max=128, min=1,
              name='colsField', oob_color=wx.RED, parent=self, pos=wx.Point(104,
              56), size=wx.Size(100, 21), style=0, value=cols)

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
        
    def GetCanvasSize(self):
        return [self.rowsField.GetValue(), self.colsField.GetValue()]        
